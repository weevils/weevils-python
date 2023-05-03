from functools import cached_property
from typing import Union
from uuid import UUID

from .client_base import ClientBase, client_factory  # noqa
from .clients.accounts import AccountsClient
from .clients.base_image import BaseImagesClient
from .clients.host import GitHostInstanceClient, GitHostsClient
from .clients.host_app import GitHostAppClient
from .clients.jobs import JobsClient
from .clients.repo import RepositoriesClient
from .clients.weevils import WeevilInstanceClient, WeevilsClient
from .dtos import WeevilsUser


class WeevilsAPI(ClientBase):
    # GitHost entities:
    hosts: GitHostsClient = client_factory(GitHostsClient)
    accounts: AccountsClient = client_factory(AccountsClient)
    repos: RepositoriesClient = client_factory(RepositoriesClient)

    # Weevil runners:
    bases: BaseImagesClient = client_factory(BaseImagesClient)
    weevils: WeevilsClient = client_factory(WeevilsClient)
    jobs: JobsClient = client_factory(JobsClient)

    # Other weevils plumbing:
    apps: GitHostAppClient = client_factory(GitHostAppClient)

    def weevil(self, weevil_id: UUID) -> WeevilInstanceClient:
        weevil = self.weevils.get(weevil_id)
        return self._make_client(WeevilInstanceClient, dto=weevil)

    def host(self, host_id_or_slug: Union[str, UUID]) -> GitHostInstanceClient:
        host = self.hosts.get(host_id_or_slug)
        return self._make_client(GitHostInstanceClient, dto=host)

    # shorthands:
    @property
    def me(self) -> WeevilsUser:
        return self._get("/accounts/me/", dto_class=WeevilsUser)

    @cached_property
    def github(self) -> GitHostInstanceClient:
        return self.host("github")
