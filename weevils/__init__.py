import os

from .client import WeevilsAPI
from .client_base import WEEVILS_API
from .exceptions import WeevilsConfigurationError


def from_env() -> WeevilsAPI:
    token = os.environ.get("WEEVILS_API_TOKEN")
    if token is None:
        raise WeevilsConfigurationError(
            "When configuring from environment variables, WEEVILS_API_TOKEN "
            "must be set and contain a valid API token for weevils.io"
        )

    api_url = os.environ.get("WEEVILS_API_URL") or WEEVILS_API
    return WeevilsAPI(token, base_url=api_url)


__all__ = ("WeevilsAPI",)
