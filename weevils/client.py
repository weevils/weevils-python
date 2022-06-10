from typing import List, Union
from uuid import UUID

import pkg_resources
from requests.sessions import Session

from .models import GitHost, WeevilsCore

VERSION = pkg_resources.get_distribution("weevils").version


class WeevilsClient(WeevilsCore):
    def __init__(self, token: str, *, api_url: str = None, user_agent: str = None, session: Session = None):
        self._token = token

        api_url = api_url or self.api_url
        if not api_url.endswith("/"):
            api_url = f"{api_url}/"
        self._base_url = api_url

        self._session = session or Session()

        # set default headers including auth
        self._session.headers.update(
            {
                "User-Agent": user_agent or f"Weevils Client v{VERSION}",
                "Authorization": f"Token {self._token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # memoised shortcuts; will be loaded if needed
        self._github: GitHost = None
        self._bitbucket: GitHost = None

    def _from_dict(self, _):
        # nothing to implement here, just required for ABC compliance
        pass

    # ---
    # Host methods
    # ---

    def list_hosts(self) -> List[GitHost]:
        """
        List all hosts available to the Weevils user account - both publicly available hosts
        and any privately configured hosts

        :return:
            A list of all hosts with which the current Weevils account can interact
        """
        return [GitHost(host, self) for host in self._get("/hosts").json()]

    def get_host(self, slug_or_pk: Union[str, UUID]) -> GitHost:
        if not slug_or_pk:
            raise ValueError("Must specify a host ID or slug")
        data = self._get(f"/hosts/{slug_or_pk}").json()
        return GitHost(data, self)

    # shortcuts:

    @property
    def github(self) -> GitHost:
        if self._github is None:
            self._github = self.get_host("github")
        return self._github

    @property
    def bitbucket(self) -> GitHost:
        if self._bitbucket is None:
            self._bitbucket = self.get_host("bitbucket")
        return self._bitbucket

    # ---
    # Repository methods
    # ---

    # TODO: figure out a nicer way to do method overloading?
    #
    # def get_repository_by_id(self, repository_id: UUID) -> Repository:
    #     pass
    #
    # # TODO: make Repository and Weevil class with methods such as "watch"
    #
    # def get_repository_by_name(self, host: Union[str, UUID], owner_name: str, name: str) -> Repository:
    #     """
    #     Fetches the complete repository object on a given host by name and owner.
    #
    #     :param host:
    #         Which host this repository is on - either as the host ID or the short name for public hosts
    #         (eg 'github', 'bitbucket' etc)
    #     :param owner_name:
    #         The name of the user or organisation owning the repository
    #     :param name:
    #         The name of the repository
    #     :return:
    #         A Repository object containing all known information about the repository
    #     """
    #
    # def watch_repository_by_id(self, repo_id: UUID, *, weevil_id: UUID = None):
    #     pass
    #
    # def watch_repository_by_name(self, host: Union[str, UUID], owner_name: str, name: str, *, weevil_id: UUID = None):
    #     """
    #
    #     :param host:
    #         Which host this repository is on - either as the host ID or the short name for public hosts
    #         (eg 'github', 'bitbucket' etc)
    #     :param owner_name:
    #         The name of the user or organisation owning the repository
    #     :param name:
    #         The name of the repository
    #     :param weevil_id:
    #         The ID of the weevil to watch the repository - if `None`, this will use the organisation default
    #     :return:
    #     """
    #     repo = self.get_repository_by_name(host, owner_name, name, weevil_id=weevil_id)
    #     return self.watch_repository_by_id(repo.id)

    # ---
    # Weevil methods
    # ---

    # def get_weevil(self, weevil_id: UUID) -> Weevil:
    #     resp = self._get(f"weevils/{weevil_id}/")
    #     return Weevil(**resp.json())
    #
    # def get_weevils(self) -> Iterable[Weevil]:
    #     resp = self._get("weevils/")
    #     return [Weevil(**weev) for weev in resp.json()]
    #
    # def run(self, weevil_id: UUID, owner: str, name: str) -> Job:
    #     resp = self._post(f"weevils/{weevil_id}/run-once", data
    #     ={"host": "gitea", "owner": owner, "name": name})  # TODO
    #     return Job(**resp.json())
    #
    # # ----------------------
    # # TODO
    # def schedule(self, weevil_id: UUID):  # ...:
    #     pass

    # def watch(self. ###):
