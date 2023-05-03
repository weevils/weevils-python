from typing import List, Union
from uuid import UUID

from ..client_base import ClientBase, InstanceClient
from ..dtos import BaseImage, Weevil
from ._utils import is_uuid
from .jobs import WeevilJobsClient


class WeevilsClient(ClientBase):
    DTO_CLASS = Weevil

    def get(self, weevil_id: UUID) -> Weevil:
        return self._get(f"/weevils/{weevil_id}/")

    def list(self) -> List[Weevil]:
        return self._list("/weevils/")

    def update(self, weevil_id: Union[str, UUID], script: str) -> Weevil:
        return super()._update(f"/weevils/{weevil_id}/", data={"script": script})

    def create(self, base: Union[str, UUID, BaseImage], name: str, script: str, *, slug: str = None) -> Weevil:
        base_id = base.id if isinstance(base, BaseImage) else base
        if not is_uuid(base_id):
            # this is a lookup by name, cannot do that here
            raise ValueError(f"Must specify a base by ID or a BaseImage object, not {base_id}")

        data = {"name": name, "base_id": str(base_id), "script": script}
        if slug:
            data["slug"] = slug

        return self._create("/weevils/", data)


class WeevilInstanceClient(InstanceClient):
    DTO_CLASS = Weevil

    @property
    def jobs(self):
        return self._make_client(WeevilJobsClient, weevil_id=self.id)
