from typing import List, Union
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import GitHost, Repository


class RepositoriesClient(ClientBase):
    DTO_CLASS = Repository

    def get(self, repo_id: UUID) -> Repository:
        return self._get(f"/repos/{repo_id}/")

    def get_by_name(self, host: Union[str, UUID, GitHost], owner_name: str, name: str) -> Repository:
        if isinstance(host, GitHost):
            host = host.id
        path = f"/hosts/{host}/repos/{owner_name}/{name}/"
        return self._get(path)

    def list(self, host: Union[str, UUID, GitHost] = None) -> List[Repository]:
        if isinstance(host, GitHost):
            host = host.id
        if host is not None:
            query = {"host_id": str(host)}
        else:
            query = {}
        return self._list("/repos/", query)


class HostRepositoriesClient(RepositoriesClient):
    # TODO: make 'user friendly' APIs with hierarchical structures

    def __init__(self, *args, host_id: UUID = None, **kwargs):
        super().__init__(*args, **kwargs)
        # if this is being used as part of a Host Instance Client, we will always filter based on host
        self._host_id = host_id

    def get_by_name(self, owner_name: str, name: str) -> Repository:
        return super().get_by_name(self._host_id, owner_name, name)

    def get(self, repo_id: UUID) -> Repository:
        return self._get(f"/repo/{repo_id}/", {"host_id": self._host_id})

    def list(self) -> List[Repository]:
        return super().list(self._host_id)
