from http import HTTPStatus
from typing import Any, Dict, Iterable
from urllib.parse import urljoin
from uuid import UUID

import pkg_resources
from requests import Response, Session

from .dtos import Job, Weevil
from .exceptions import WeevilsAPIException

VERSION = pkg_resources.get_distribution("weevils").version


class WeevilsClient:

    user_agent = f"Weevils Client v{VERSION}"
    api_url = "https://api.weevils.io/"

    def __init__(self, token: str, *, api_url: str = None, user_agent: str = None, session: Session = None):
        self._token = token

        api_url = api_url or self.api_url
        if not api_url.endswith("/"):
            api_url = f"{api_url}/"
        self._base_url = api_url

        self._session = session or Session()

        if user_agent:
            self.user_agent = user_agent

    def _request(
        self, method: str, path: str, accept_status=(), *, query: Dict[str, Any] = None, data: Dict[str, Any] = None
    ) -> Response:

        url = urljoin(self._base_url, path.lstrip("/"))
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": f"Token {self._token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        resp = self._session.request(method, url, params=query, data=data, headers=headers)
        if resp.status_code not in accept_status:
            raise WeevilsAPIException(resp)
        return resp

    def _get(self, path: str, query: Dict[str, Any] = None) -> Response:
        return self._request("GET", path, accept_status=(HTTPStatus.OK,), query=query)

    def _post(self, path: str, data: Dict[str, Any] = None) -> Response:
        return self._request("POST", path, accept_status=(HTTPStatus.OK, HTTPStatus.CREATED), data=data)

    def get_weevil(self, weevil_id: UUID) -> Weevil:
        resp = self._get(f"weevils/{weevil_id}/")
        return Weevil(**resp.json())

    def get_weevils(self) -> Iterable[Weevil]:
        resp = self._get("weevils/")
        return [Weevil(**weev) for weev in resp.json()]

    def run(self, weevil_id: UUID, owner: str, name: str) -> Job:
        resp = self._post(f"weevils/{weevil_id}/run-once", data={"host": "gitea", "owner": owner, "name": name})  # TODO
        return Job(**resp.json())

    # ----------------------
    # TODO
    def schedule(self, weevil_id: UUID):  # ...:
        pass

    # def watch(self. ###):
