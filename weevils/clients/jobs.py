from typing import List
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import Job


class JobsClient(ClientBase):
    DTO_CLASS = Job

    def create(self, weevil_id: UUID, repository_id: UUID) -> Job:
        data = {"weevil_id": str(weevil_id), "repository_id": str(repository_id)}
        return self._create("/jobs/", data)

    def get(self, job_id: UUID) -> Job:
        return self._get(f"/jobs/{job_id}/")

    def list(
        self, offset: int = 0, limit: int = 100, *, weevil_id: UUID = None, repository_id: UUID = None
    ) -> List[Job]:
        query = {"offset": offset, "limit": limit}
        if weevil_id:
            query["weevil_id"] = str(weevil_id)
        if repository_id:
            query["repository_id"] = str(repository_id)
        return self._list("/jobs/", query)


class WeevilJobsClient(JobsClient):
    def __init__(self, *args, weevil_id: UUID, **kwargs):
        super().__init__(*args, **kwargs)
        self._weevil_id = weevil_id

    def create(self, repository_id: UUID) -> Job:
        return super().create(self._weevil_id, repository_id)

    def get(self, job_id: UUID) -> Job:
        return self._get(f"/jobs/{job_id}/", {"weevil_id": str(self._weevil_id)})

    def list(self, *args, **kwargs) -> List[Job]:
        return super().list(*args, weevil_id=self._weevil_id, **kwargs)
