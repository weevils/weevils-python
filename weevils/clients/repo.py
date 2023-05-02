from typing import List
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import Repository


class RepositoriesClient(ClientBase):
    DTO_CLASS = Repository

    def get(self, repo_id: UUID) -> Repository:
        return self._get(f"/repo/{repo_id}/")

    def list(self) -> List[Repository]:
        return self._list("/repo/")


class HostRepositoriesClient(RepositoriesClient):
    def __init__(self, *args, host_id: UUID = None, **kwargs):
        super().__init__(*args, **kwargs)
        # if this is being used as part of a Host Instance Client, we will always filter based on host
        self._host_id = host_id

    def get_by_name(self, owner_name: str, name: str) -> Repository:
        return self._get(f"/host/{self._host_id}/repo/{owner_name}/{name}/")

    def get(self, repo_id: UUID) -> Repository:
        return self._get(f"/repo/{repo_id}/", {"host_id": self._host_id})

    def list(self) -> List[Repository]:
        return self._list(f"/host/{self._host_id}/repo/")
