""" This module provides the object structures for entities in the weevils API, including methods to mutate
    or fetch related entities """

# modelled on github3.py
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin
from uuid import UUID

from requests import Response

from .exceptions import EntityNotFound, WeevilsAPIException

Data = Dict[str, Any]


class WeevilsCore(ABC):
    def __init__(self, data: Data, parent_obj: "WeevilsCore" = None):
        self._session = parent_obj._session
        self._base_url = parent_obj._base_url
        self._from_dict(data)
        self._data = data

    def _request(self, method: str, path: str, accept_status=(), *, query: Data = None, data: Data = None) -> Response:
        url = urljoin(self._base_url, path.lstrip("/"))
        resp = self._session.request(method, url, params=query, json=data)
        if resp.status_code not in accept_status:
            raise WeevilsAPIException(resp)
        return resp

    def _get(self, path: str, query: Data = None) -> Response:
        return self._request("GET", path, accept_status=(HTTPStatus.OK,), query=query)

    def _post(self, path: str, data: Data = None) -> Response:
        return self._request("POST", path, accept_status=(HTTPStatus.OK, HTTPStatus.CREATED), data=data)

    def _make_obj(self, model_cls, data: Union[Data, Response]) -> "WeevilsCore":
        if isinstance(data, Response):
            data = data.json()
        if not isinstance(data, dict):
            raise ValueError(f"Can't handle data structure {data}")
        return model_cls(data, self)

    @abstractmethod
    def _from_dict(self, data: Data):
        raise NotImplementedError

    @property
    def raw(self) -> Data:
        return self._data


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

    def _make_repository(self, path: str) -> "Repository":
        resp = self._get(path)
        if resp.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFound("Repository", path)
        return self._make_obj(Repository, resp)

    def repository(self, owner_name: str, name: str) -> "Repository":
        if None in (owner_name, name):
            raise ValueError("owner_name and name cannot be None")
        return self._make_repository(f"hosts/{self.slug}/repos/{owner_name}/{name}/")

    def repository_by_id(self, repository_id: UUID) -> "Repository":
        if repository_id is None:
            raise ValueError("reopsitory_id cannot be None")
        return self._make_repository(f"hosts/{self.slug}/repos/{repository_id}/")


class Job(WeevilsCore):
    id: UUID
    output: str
    status: Optional[str]

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.status = data["status"]
        self.output = data["output"]


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
        self.owner = self._make_obj(Account, data["owner"])
        self.host = self._make_obj(GitHost, data["host"])


class WeevilBase(WeevilsCore):
    id: UUID
    name: str
    slug: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]


class Weevil(WeevilsCore):
    id: UUID
    name: str
    slug: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]

    def run(self, repository: Union[UUID, Repository]) -> Job:
        if repository is None:
            raise ValueError("Repository cannot be None")

        repository_id = getattr(repository, "id", repository)
        return self._make_obj(Job, self._post(f"weevils/{self.id}/run/{repository_id}/"))

    def watch(self, repository_id: UUID):
        pass
