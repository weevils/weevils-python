from dataclasses import dataclass
from typing import List, Optional
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
    name: str
    host: GitHost

    def __post_init__(self):
        super().__post_init__()
        self.host = GitHost(**self.host)


@dataclass(eq=False)
class GitHostApp(ResourceMixin):
    id: UUID
    name: str
    host: GitHost
    authorization_url: str

    def __post_init__(self):
        super().__post_init__()
        self.host = GitHost(**self.host)


@dataclass(eq=False)
class Repository(ResourceMixin):
    id: UUID
    owner: Account
    name: str
    host: GitHost
    private: bool
    url_on_host: str

    def __post_init__(self):
        super().__post_init__()
        self.owner = Account(**self.owner)
        self.host = GitHost(**self.host)


# ---
# Job and Weevil objects
# ---


@dataclass(eq=False)
class BaseImage(ResourceMixin):
    id: UUID
    name: str
    slug: str


@dataclass(eq=False)
class Weevil(ResourceMixin):
    id: UUID
    name: str
    slug: str
    script: str
    build_status: str


@dataclass(eq=False)
class Artifact(ResourceMixin):
    id: UUID
    path: str
    mimetype: str
    download_url: str


@dataclass(eq=False)
class Job(ResourceMixin):
    id: UUID
    number: int
    output: str
    artifacts: List[Artifact]
    repository: Repository
    status: Optional[str] = None
    failure_reason: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self.artifacts = [Artifact(**art) for art in self.artifacts]
        self.repository = Repository(**self.repository)


# ---
# Other Resources for weevils
# ---


@dataclass(eq=False)
class WeevilsUser(ResourceMixin):
    id: UUID
    display_name: str
    accounts: List[Account]

    def __post_init__(self):
        super().__post_init__()
        self.accounts = [Account(**acc) for acc in self.accounts]
