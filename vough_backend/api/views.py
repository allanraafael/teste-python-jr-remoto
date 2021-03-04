from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, views, viewsets

from vough_backend.settings import CACHE_TTL
from . import models, serializers
from .integrations.github import GithubApi


@extend_schema(tags=['orgs', ])
class OrganizationViewSet(viewsets.ModelViewSet):
    """ViewSet com as ações de listagem, recuperação e exclusão para organizações da API"""

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = []
    authentication_classes = []
    lookup_field = "login"

    @extend_schema(
        summary='Consulta clientes ordenados pela prioridade',
        description='Consulta clientes ordenados pela prioridade (score), da maior para a menor.',
    )
    def list(self, request, *args, **kwargs):
        """
        Retorna a lista de organizações ordenadas pela prioridade (score)
        que já foram consultadas na API
        """
        queryset = self.filter_queryset(self.get_queryset().order_by('-score'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return views.Response(serializer.data)

    @extend_schema(
        summary=_('Consulta um cliente específico'),
        description='Consulta um cliente específico através do nome (login)'
    )
    @method_decorator(cache.cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        """
        Faz uma consulta para API do GitHub através do login e retorna uma
        organização da API, se ela estiver salva no banco de dados seus
        dados são atualizados, se não, ela será criada com os dados
        retornados da API do GitHub.
        """

        api = GithubApi()
        # Login em minúsculo para evitar ambiguidade de dados
        login = self.kwargs.get(self.lookup_field).lower()
        # Armazena uma organização obtida da API do GitHub em uma variável
        organization = api.get_organization(login)
        # Armazena membros públicos de organização obtida da API do GitHub em uma variável
        public_members = api.get_organization_public_members(login)

        # Se o login informado não for válido, retornar com status 404
        if not organization or not public_members:
            return views.Response({'login': login, 'message': 'Não existe organização com este login'}, status=404)

        name = api.get_name(organization.json())
        score = api.get_score(organization.json(), public_members.json())
        status_retrieve = status.HTTP_200_OK

        try:
            # Atualiza os dados da organização, caso exista no banco de dados
            models.Organization.objects.filter(login=login).update(login=login, name=name, score=score)
            instance = generics.get_object_or_404(models.Organization, login=login)
        except Http404:
            # Armazena uma nova organização por meio dos dados consultados da API do GitHub
            instance = models.Organization.objects.create(login=login, name=name, score=score)
            status_retrieve = status.HTTP_201_CREATED

        serializer = self.get_serializer(instance)

        return views.Response(serializer.data, status_retrieve)

    @extend_schema(
        summary='Deleta um cliente específico',
        description='Deleta um cliente específico através do nome (login)'
    )
    def destroy(self, request, *args, **kwargs):
        """
        Deleta uma organização através da login
        """

        # Login em minúsculo para evitar ambiguidade de dados
        login = self.kwargs.get(self.lookup_field).lower()
        try:
            instance = generics.get_object_or_404(models.Organization, login=login)
        except Http404:
            return views.Response(
                {'login': login, 'message': 'Esta organização não existe ou ainda não foi consultada'},
                status=404
            )
        self.perform_destroy(instance)

        return views.Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Faz um override na função get_queryset() para atualizar os dados do
        cache da propriedade queryset da ViewSet após alguma mudança no
        banco, seja ao criar, atualizar ou excluir uma organização
        """
        queryset = models.Organization.objects.all()

        return queryset
