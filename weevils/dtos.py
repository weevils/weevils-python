from dataclasses import dataclass
from uuid import UUID


@dataclass
class Host:
    pass


@dataclass
class Weevil:
    id: UUID
    name: str


@dataclass
class Repository:
    id: UUID
    host: Host
    name: str


@dataclass
class Job:
    id: UUID
    weevil_id: UUID

    results: str = None


__all__ = ("Host", "Job", "Repository", "Weevil")
