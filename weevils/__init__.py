import os

from .client import WeevilsClient, WeevilsSandboxClient
from .exceptions import WeevilsAPIException, WeevilsConfigurationError


def from_env() -> WeevilsClient:
    token = os.environ.get("WEEVILS_API_TOKEN")
    if token is None:
        raise WeevilsConfigurationError(
            "When configuring from environment variables, WEEVILS_API_TOKEN "
            "must be set and contain a valid API token for weevils.io"
        )

    api_url = os.environ.get("WEEVILS_API_URL")
    return WeevilsClient(token, api_url=api_url)


__all__ = (
    "WeevilsClient",
    "WeevilsSandboxClient",
    "WeevilsConfigurationError",
    "WeevilsAPIException",
    "from_env",
)
