from typing import Dict, Any, Iterable
from urllib.parse import urljoin, urlencode
from uuid import UUID

from .dtos import Weevil, Job
import requests
from requests import Response
import pkg_resources
import sys


# TODO:
VERSION = pkg_resources.get_distribution("fss").version


class WeevilsClient:

    user_agent = f'Weevils Client version {VERSION} / Python {sys.version} / Requests {requests.__version__}'
    api_url = 'https://api.weevils.io/'

    def __init__(self, token: str, api_url: str=None, user_agent: str=None):
        self._token = token

        api_url = api_url or self.api_url
        if not api_url.endswith('/'):
            api_url = f"{api_url}/"
        self._base_url = api_url

        if user_agent:
            self.user_agent = user_agent

    def _request(self, method: str, path: str, *, query: Dict[str, Any]=None, data: Dict[str, Any]=None) -> Response:
        url = urljoin(self._base_url, path.lstrip('/'))
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': f'Bearer {self._token}'
        }
        return requests.request(method, url, params=query, data=data, headers=headers)

    def _get(self, path: str, query: Dict[str, Any]=None) -> Response:
        return self._request('GET', path, query=query)

    def _post(self, path: str, data: Dict[str, Any]=None) -> Response:
        return self._request('POST', path, data=data)

    def run(self, weevil_id: UUID, owner: str, name: str):
        resp = self._post(f"weevils/{weevil_id}/run-once", data={
            'host': 'gitea',  # TODO
            'owner': str,
            'name': str
        })
        return Job(**resp.json())

    # ----------------------
    # TODO
    def schedule(self, weevil_id: UUID): #...:
        pass

    # def watch(self. ###):

    def get_weevils(self) -> Iterable[Weevil]:
        resp = self._get('weevils')
        return [Weevil(**weev) for weev in resp.json()]

