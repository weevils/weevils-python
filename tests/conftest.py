import os
from pathlib import Path

import pytest
from betamax import Betamax

from weevils import WeevilsClient

_API_TOKEN = os.environ.get("WEEVILS_CLIENT_TEST_TOKEN", "placeholder")

with Betamax.configure() as config:
    config.cassette_library_dir = Path(__file__).parent / "cassettes"

    record_mode = os.environ.get("WEEVILS_CLIENT_TEST_RECORD_MODE", "once")
    config.default_cassette_options["record_mode"] = record_mode

    config.define_cassette_placeholder("<API_TOKEN>", _API_TOKEN)


@pytest.fixture
def client(betamax_session) -> WeevilsClient:
    # use the token in the recorded betamax tests - or if using a local weevils installation
    token = _API_TOKEN
    # if we are running a weevils system locally, we can point at it when running tests instead of relying on
    # the Betamax mock responses
    api_url = os.environ.get("WEEVILS_CLIENT_TEST_API", "https://api.weevils.io")

    # use the betamax cassettes if we are not talking to a local weevils system
    # session = Session() if api_url else betamax_session

    yield WeevilsClient(token, api_url=api_url, session=betamax_session)
