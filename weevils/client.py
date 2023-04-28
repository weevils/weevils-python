from functools import cached_property

from .clients._client_base import ClientBase, client_factory  # noqa
from .clients.account import AccountClient
from .clients.base_image import BaseImageClient
from .clients.host import GitHostClient
from .clients.job import JobClient
from .dtos import WeevilUser


class WeevilsClient(ClientBase):
    # repo = _make_client()
    # host_app = _make_client()
    # weevil = _make_client()
    account = client_factory(AccountClient)
    host: GitHostClient = client_factory(GitHostClient)
    job: JobClient = client_factory(JobClient)
    base: BaseImageClient = client_factory(BaseImageClient)

    # shorthands:
    @property
    def me(self) -> WeevilUser:
        return self._get("/account/me/", dto_class=WeevilUser)

    @cached_property
    def github(self):
        return self.host.get("github")
