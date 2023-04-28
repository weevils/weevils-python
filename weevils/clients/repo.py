from uuid import UUID

from ..dtos import Job
from ._client_base import ClientBase


class RepoClient(ClientBase):
    def get_by_id(self, job_id: UUID, host_id: UUID = None) -> Job:
        pass

    def get_by_name(self, account_name: str, repo_name: str, host_id: UUID = None) -> Job:
        ...

    def get(self, *, job_id: UUID = None, account_name: str = None, repo_name: str = None, host_id: UUID = None) -> Job:
        if job_id is not None:
            return self.get_by_id(job_id, host_id=host_id)
