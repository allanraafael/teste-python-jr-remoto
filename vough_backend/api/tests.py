from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from . import models
from .serializers import OrganizationSerializer


class TestRankOrgsListAPI(TestCase):
    """
    Testa dados retornados e os status das respostas da listagem de
    organizações API
    """

    def setUp(self):
        """Inicializa a propriedade da requisição para os testes da classe"""

        self.client = APIClient()

    def test_request_response_with_data(self):
        """Testa a listagem da API com organizações salvas no banco de dados"""

        # Cria instâncias no banco de dados para o teste
        models.Organization.objects.create(login='docs', name='GitHub Docs', score=14)
        models.Organization.objects.create(login='prestcontas', name='PrestContas', score=3)
        # Consulta a listagem de organizações
        response = self.client.get('/api/orgs/')
        # Compara o status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_response_no_data(self):
        """Testa a listagem da API sem organizações salvas no banco de dados"""

        # Consulta a listagem de organizações
        response = self.client.get('/api/orgs/')
        # Compara o status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orgs(self):
        """
        Testa se todos os dados do banco de dados estão sendo exibidos na
        listagem da API
        """

        # Consulta a listagem de organizações
        response = self.client.get('/api/orgs/')
        # Consulta as organizações salvas no banco
        orgs = models.Organization.objects.all()
        # Serializa os dados em python para Json
        serializer = OrganizationSerializer(orgs, many=True)
        # Compara os dados que deve retornar
        self.assertEqual(response.data, serializer.data)


class TestRankOrgsRetrieveAPI(TestCase):
    """
    Testa a recuperação de uma organização, que pode criar (se for a primeira
    vez de consulta) ou atualizar (se for a partir da segunda consulta) uma organização
    """

    def setUp(self):
        """
        Inicializa a propriedade da requisição para os testes da classe e
        cria instâncias no banco de dados para o teste
        """

        self.client = APIClient()
        models.Organization.objects.create(login='docs', name='GitHub Docs', score=14)
        models.Organization.objects.create(login='prestcontas', name='PrestContas', score=3)

    def test_get_valid_login_org(self):
        """Testa se com um login valido a organizaçao e retornada corretamente"""

        # Consulta uma organizaçao
        response = self.client.get('/api/orgs/docs/')
        # Consulta a organizaçao no banco
        org = models.Organization.objects.get(login='docs')
        # Serializa os dados em python para Json
        serializer = OrganizationSerializer(org)
        # Compara os dados que deve retornar
        self.assertEqual(response.data, serializer.data)
        # Compara os status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_login_org(self):
        """Testa se com login invalido a organizaçao retorna o status nao encontrado"""

        response = self.client.get('/api/orgs/0sd8f4s8df04s8df4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_org_created_if_login_not_consulted(self):
        """
        Testa se e criado uma organizacao quando e a primeira consulta
        e com um login valido
        """

        # Consulta uma organizaçao
        response = self.client.get('/api/orgs/nubank/')
        # Compara os status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_org_updated_if_login_consulted(self):
        """
        Testa se e atualizado uma organizacao quando e a segunda consulta
        e com um login valido
        """

        # Consulta uma organizaçao
        response = self.client.get('/api/orgs/docs/')
        # Compara os status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRankOrgsDestroyAPI(TestCase):
    """Testa a exclusao de uma organizaçao"""

    def setUp(self):
        """
        Inicializa a propriedade da requisição para os testes da classe e
        cria instâncias no banco de dados para o teste
        """

        self.client = APIClient()
        models.Organization.objects.create(login='docs', name='GitHub Docs', score=14)
        models.Organization.objects.create(login='prestcontas', name='PrestContas', score=3)

    def test_delete_valid_login_org(self):
        """Testa se a oraganizacao e excluida quando o login e valido"""

        # Exclui uma organizaçao
        response = self.client.delete('/api/orgs/docs/')
        # Compara os status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_login_org(self):
        """Testa se e retornado um status nao encontrado quando o login e invalido"""

        # Tenta excluir uma organizaçao
        response = self.client.delete('/api/orgs/0sd8f4s8df04s8df4/')
        # Compara os status que deve retornar
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
