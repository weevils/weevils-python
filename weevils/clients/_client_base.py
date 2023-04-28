import logging
import sys
from functools import cached_property
from http import HTTPStatus
from importlib.metadata import version
from typing import Generic, Type, TypeVar
from urllib.parse import urljoin

from requests import Response, Session

from ..exceptions import (
    ActionDisallowed,
    BadRequest,
    EntityNotFound,
    NotAuthenticated,
    ServiceProcessingError,
    ServiceUnavailable,
    UnhandledResponse,
    WriteConflict,
)
from ._typing import Data

Client = TypeVar("Client", bound="ClientBase")

VERSION = str(version("weevils"))

_python_version = ".".join(str(v) for v in sys.version_info[:2])
DEFAULT_USER_AGENT = f"Weevils Client v{VERSION} ({_python_version})"

WEEVILS_API = "https://api.weevils.io"
WEEVILS_SANDBOX_API = "https://api.sandbox.weevils.io"


def client_factory(client_cls: Type[Client], **kwargs) -> Client:
    def _make_cls(self):
        client = client_cls(
            self._api_token, base_url=self._base_url, session=self._session, user_agent=self._user_agent, **kwargs
        )
        if self._oauth_token:
            client.login(self._oauth_token)
        return client

    return cached_property(_make_cls)


class ClientBase(Generic[Client]):
    def __init__(
        self,
        api_token: str,
        base_url: str = WEEVILS_API,
        session: Session = None,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        """

        :param api_token:
            An API token created to allow programmatic access to view, edit and manage Weevils, Jobs and related
            configuration needed as a Weevils customer. This must always be provided, even if logging in as an
            individual user later.
        :param base_url:
            The root API url, which will default to https://api.weevils.io/
        :param user_agent:
            The User Agent to send along with requests.
        :param session:
            A requests.Session object which will be used to make calls to the Weevils API. Can be replaced for example
            if using a caching Session or a test Session object which mocks API results.
        """
        # we always
        self._api_token = api_token
        self._oauth_token = None
        self._user_agent = user_agent
        self._base_url = base_url
        self._session = session or Session()

    def login(self, oauth_token: str):
        """
        Using an OAuth token, login as a specific user. All endpoints will return data in the context of that user -
        that is to say, listing repositories will list only the repositories they can see.
        """
        self._log.debug("Authenticating as a user")
        self._oauth_token = oauth_token

    def logout(self):
        """
        Remove the current user context (if there is any) so that future calls will authenticate as the API user.
        """
        self._log.debug("No longer authenticating as a user")
        self._oauth_token = None

    @property
    def _log(self):
        return logging.getLogger("weevils_client")

    # ---
    # HTTP methods and wrappers
    # ---

    def _make_url(self, path: str) -> str:
        if not path.startswith("/"):
            raise ValueError("Path must start with /")
        return urljoin(self._base_url, path)

    def _request(self, method: str, path: str, *args, **kwargs) -> Response:
        headers = kwargs.pop("headers", {}) or {}  # need to do this to catch `kwargs['headers'] = None`

        # We have to explicitly set this here - setting session.headers gets overwritten and ignored
        headers["User-Agent"] = self._user_agent

        if self._oauth_token:
            headers["Authorization"] = f"Bearer {self._oauth_token}"
        else:
            headers["Authorization"] = f"Token {self._api_token}"

        return self._session.request(method, self._make_url(path), *args, headers=headers, **kwargs)

    def _http_get(self, path, *, allow_redirects: bool = True, headers: Data = None, query: Data = None) -> Response:
        return self._request("GET", path, allow_redirects=allow_redirects, params=query, headers=headers)

    def _http_post(self, path: str, data: Data) -> Response:
        return self._request("POST", path, json=data)

    def _http_patch(self, path: str, data: Data) -> Response:
        return self._request("PATCH", path, json=data)

    def _http_delete(self, path: str) -> Response:
        return self._request("DELETE", path)

    def _http_put(self, path: str, data: Data) -> Response:
        return self._request("PUT", path, json=data)

    def _handle_response(self, resp: Response, *, detail: bool = True, dto_class=None):
        dto_class = dto_class or self.DTO_CLASS
        if dto_class is None:
            raise ValueError("Must specify a DTO class")

        # TODO: would be nice to eventually replace this with a match/case statement
        #       when older python versions are dropped
        if resp.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            if detail:
                return dto_class(**resp.json())
            else:
                data = resp.json()
                if isinstance(data, dict):
                    data = data["results"]
                return [dto_class(**obj) for obj in data]

        elif resp.status_code == HTTPStatus.NO_CONTENT:
            # successful deletion
            return True

        # Error handling

        elif resp.status_code == HTTPStatus.CONFLICT:
            raise WriteConflict(resp)

        elif resp.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFound(dto_class, resp)

        elif resp.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequest(resp)

        elif resp.status_code == HTTPStatus.FORBIDDEN:
            # This happens if the caller is using a JWT on behalf of a user who is not allowed to perform
            # the required action - for example, trying to change a resource which they do not own or do
            # not have the correct scopes to change.
            raise ActionDisallowed(resp)

        elif resp.status_code == HTTPStatus.UNAUTHORIZED:
            # This happens when a bad JWT string is used to make calls and the service rejects it.
            raise NotAuthenticated(resp)

        elif resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ServiceProcessingError(resp)

        elif resp.status_code in (HTTPStatus.SERVICE_UNAVAILABLE, HTTPStatus.GATEWAY_TIMEOUT):
            raise ServiceUnavailable(resp)

        else:
            raise UnhandledResponse(resp)

    # ---
    # Shorthands for RESTful verbs
    # ---

    def _get(self, path: str, query=None, *, dto_class=None):
        """
        Gets a single resource
        """
        resp = self._http_get(path, query=query)
        return self._handle_response(resp, detail=True, dto_class=dto_class)

    def _list(self, path: str, query=None, *, dto_class=None):
        """
        Gets a list of resources
        """
        resp = self._http_get(path, query=query)
        return self._handle_response(resp, detail=False, dto_class=dto_class)

    def _create(self, path, data, *, dto_class=None):
        """
        Creates a brand-new resource
        """
        resp = self._http_post(path, data)
        return self._handle_response(resp, dto_class=dto_class)

    def _delete(self, path):
        """
        Deletes a resource entirely
        """
        resp = self._http_delete(path)
        return self._handle_response(resp)

    def _replace(self, path, data: Data):
        """
        Complete update of a resource
        """
        resp = self._http_put(path, data)
        return self._handle_response(resp, detail=True)

    def _update(self, path, data: Data):
        """
        Partial update of some properties of a resource
        """
        resp = self._http_patch(path, data)
        return self._handle_response(resp, detail=True)
