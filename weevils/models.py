""" This module provides the object structures for entities in the weevils API, including methods to mutate
    or fetch related entities """

# modelled on github3.py
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Dict
from urllib.parse import urljoin
from uuid import UUID

import pkg_resources
from requests import Response

from .exceptions import WeevilsAPIException

VERSION = pkg_resources.get_distribution("weevils").version


Data = Dict[str, Any]


class WeevilsCore(ABC):
    def __init__(self, data: Data, parent_obj: "WeevilsCore" = None):
        self._session = parent_obj._session
        self._base_url = parent_obj._base_url
        self._from_dict(data)

    def _request(self, method: str, path: str, accept_status=(), *, query: Data = None, data: Data = None) -> Response:

        url = urljoin(self._base_url, path.lstrip("/"))
        resp = self._session.request(method, url, params=query, data=data)
        if resp.status_code not in accept_status:
            raise WeevilsAPIException(resp)
        return resp

    def _get(self, path: str, query: Data = None) -> Response:
        return self._request("GET", path, accept_status=(HTTPStatus.OK,), query=query)

    def _post(self, path: str, data: Data = None) -> Response:
        return self._request("POST", path, accept_status=(HTTPStatus.OK, HTTPStatus.CREATED), data=data)

    @abstractmethod
    def _from_dict(self, data: Data):
        ...


class GitHost(WeevilsCore):
    id: UUID
    name: str
    slug: str
    private: bool

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]
        self.private = data["private"]

    def repository(self, owner_name: str, name: str) -> "Repository":
        resp = self._get(f"{self.id}/repos/{owner_name}/{name}")
        return Repository(resp.json(), self)

    def repository_by_id(self, repository_id: UUID) -> "Repository":
        resp = self._get(f"{self.id}/repos/{repository_id}")
        return Repository(resp.json(), self)


class Account(WeevilsCore):
    id: UUID
    name: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]


class Repository(WeevilsCore):
    id: UUID
    owner: Account
    host: GitHost

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.owner = Account(data["owner"], self)
