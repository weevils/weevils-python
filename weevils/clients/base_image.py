from typing import List, Union
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import BaseImage
from ._utils import is_uuid


class BaseImageClient(ClientBase):
    DTO_CLASS = BaseImage

    def get(self, id_or_slug: Union[str, UUID]) -> BaseImage:
        # If this is fetching by PK:
        if is_uuid(id_or_slug):
            return self._get(f"/base/{id_or_slug}/")
        # Otherwise this is fetching by slug
        bases = self._list(f"/base/?slug={id_or_slug}")
        if len(bases) == 0:
            return False  # TODO: NotFound
        return bases[0]

    def list(self) -> List[BaseImage]:
        return self._list("/base/")
