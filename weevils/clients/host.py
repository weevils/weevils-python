from typing import List, Union
from uuid import UUID

from ..client_base import ClientBase, InstanceClient
from ..dtos import GitHost
from .repo import HostRepositoriesClient


class GitHostsClient(ClientBase):
    DTO_CLASS = GitHost

    def create(self, name: str, api_url: str, clone_url: str) -> GitHost:
        data = {
            "name": name,
            "api_url": api_url,
            "clone_url": clone_url,
        }
        return self._create("/host/", data)

    def get(self, host_id_or_slug: Union[str, UUID]) -> GitHost:
        return self._get(f"/host/{host_id_or_slug}/")

    def list(self, offset: int = 0, limit: int = 100) -> List[GitHost]:
        query = {"limit": limit, "offset": offset}
        return self._list("/host/", query)


class GitHostInstanceClient(InstanceClient):
    """
    This represents an interface to the resources on a particular GitHost
    """

    DTO_CLASS = GitHost

    @property
    def repos(self):
        return self._make_client(HostRepositoriesClient, host_id=self.id)
