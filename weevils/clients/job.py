from typing import List
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import Job


class JobClient(ClientBase):
    DTO_CLASS = Job

    def create(self, weevil_id: UUID, repository_id: UUID) -> Job:
        pass

    def get(self, *, job_id: UUID) -> Job:
        return self._get(f"/job/{job_id}/")

    def list(self, offset: int = 0, limit: int = 100, *, weevil_id: UUID, repository_id: UUID) -> List[Job]:
        pass
