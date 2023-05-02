from functools import cached_property
from typing import Union
from uuid import UUID

from .client_base import ClientBase, client_factory  # noqa
from .clients.account import AccountClient
from .clients.base_image import BaseImageClient
from .clients.host import GitHostInstanceClient, GitHostsClient
from .clients.host_app import GitHostAppClient
from .clients.job import JobClient
from .clients.repo import RepositoriesClient
from .dtos import WeevilsUser


class WeevilsClient(ClientBase):
    repos = client_factory(RepositoriesClient)
    # weevil = _make_client()
    apps = client_factory(GitHostAppClient)
    accounts = client_factory(AccountClient)
    hosts: GitHostsClient = client_factory(GitHostsClient)
    jobs: JobClient = client_factory(JobClient)
    bases: BaseImageClient = client_factory(BaseImageClient)

    def host(self, host_id_or_slug: Union[str, UUID]) -> GitHostInstanceClient:
        host = self.hosts.get(host_id_or_slug)
        return self._make_client(GitHostInstanceClient, dto=host)

    # shorthands:
    @property
    def me(self) -> WeevilsUser:
        return self._get("/account/me/", dto_class=WeevilsUser)

    @cached_property
    def github(self) -> GitHostInstanceClient:
        return self.host("github")
