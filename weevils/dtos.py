from dataclasses import dataclass
from typing import List
from uuid import UUID


class ResourceMixin:
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

    def __post_init__(self):
        self.id = UUID(self.id)


# ---
# Objects on GitHosts
# ---


@dataclass(eq=False)
class GitHost(ResourceMixin):
    id: UUID
    name: str
    slug: str
    private: bool


@dataclass(eq=False)
class Account(ResourceMixin):
    id: UUID
    display_name: str

    def __post_init__(self):
        super().__post_init__()
        self.host = GitHost(**self.host)


# ---
# Job and Weevil objects
# ---


@dataclass(eq=False)
class BaseImage(ResourceMixin):
    id: UUID
    name: str
    slug: str


class Job(ResourceMixin):
    pass


# ---
# Other Resources for weevils
# ---


@dataclass(eq=False)
class WeevilUser(ResourceMixin):
    id: UUID
    display_name: str
    accounts: List[Account]

    def __post_init__(self):
        super().__post_init__()
        self.accounts = [Account(**acc) for acc in self.accounts]
