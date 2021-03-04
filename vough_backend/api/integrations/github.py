from typing import Union
from urllib.parse import urljoin

import requests
import requests_cache
from requests import Response

from vough_backend.settings import GITHUB_TOKEN, CACHE_TTL, GITHUB_API_URL

# Criação de cache para biblioteca requests
requests_cache.install_cache('github_cache', backend='sqlite', expire_after=CACHE_TTL)


class GithubApi:
    """
    Classe que representa a API do GitHub
    """

    def get_organization(self, login: str) -> Union[Response, None]:
        """
        Busca uma organização pelo login através da API do Github

        :login: login da organização no Github
        """
        url = urljoin(GITHUB_API_URL, f'/orgs/{login}')
        response = requests.get(url=url, headers={'Authorization': f'token {GITHUB_TOKEN}'})

        if response.ok:
            return response

        return None

    def get_organization_public_members(self, login: str) -> Union[Response, None]:
        """
        Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        url = urljoin(GITHUB_API_URL, f'/orgs/{login}/public_members')
        response = requests.get(url=url, headers={'Authorization': f'token {GITHUB_TOKEN}'})

        if response.ok:
            return response

        return None

    def get_name(self, org: dict) -> str:
        """
        Retorna o nome da organização

        :org: Dicionário Json da organização obtido da função get_organization()
        """
        name = org.get('name') or ""

        return name

    def get_score(self, org: dict, members: dict) -> int:
        """
        Retorna o cálculo da prioridade (score) através da soma de repositórios e a quantidade de membros públicos

        :org: Dicionário Json da organização obtido da função get_organization()
        :members: Dicionário Json dos membros da organização obtido da função get_organization_public_members()
        """
        public_repos = org.get('public_repos') or 0
        public_members = len(members)

        return public_members + public_repos
