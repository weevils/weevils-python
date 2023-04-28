from typing import List
from uuid import UUID

from ..dtos import GitHost
from ._client_base import ClientBase


class GitHostClient(ClientBase):
    DTO_CLASS = GitHost

    def create(self, name: str, api_url: str, clone_url: str) -> GitHost:
        data = {
            "name": name,
            "api_url": api_url,
            "clone_url": clone_url,
        }
        return self._create("/host/", data)

    def get(self, host_id_or_slug: str | UUID) -> GitHost:
        return self._get(f"/host/{host_id_or_slug}/")

    def list(self, offset: int = 0, limit: int = 100) -> List[GitHost]:
        query = {"limit": limit, "offset": offset}
        return self._list("/host/", query)
