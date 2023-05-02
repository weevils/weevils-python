from typing import List
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import GitHostApp


class GitHostAppClient(ClientBase):
    DTO_CLASS = GitHostApp

    def create(self, host_id: UUID, name: str, client_id: str, client_secret: str):
        data = {"host_id": str(host_id), "name": name, "client_id": client_id, "client_secret": client_secret}
        return self._create("/host_app/", data)

    def list(self) -> List[GitHostApp]:
        return self._list("/host_app/")

    def get(self, app_id: UUID) -> List[GitHostApp]:
        return self._get(f"/host_app/{app_id}/")
