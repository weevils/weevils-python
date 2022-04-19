import os
from pathlib import Path

import pytest
from betamax import Betamax
from requests import Session

from weevils import WeevilsClient

# set the cassettes directory globally
config = Betamax.configure()
config.cassette_library_dir = Path(__file__).parent / "cassettes"


@pytest.fixture
def client(betamax_session) -> WeevilsClient:

    # use the token in the recorded betamax tests, unless otherwise specified (if using a local weevils installation
    # to test against, set this environment variable)
    token = os.environ.get("WEEVILS_CLIENT_TEST_TOKEN", "fish")
    # if we are running a weevils system locally, we can point at it when running tests instead of relying on
    # the Betamax mock responses
    api_url = os.environ.get("WEEVILS_CLIENT_TEST_API")

    # use the betamax cassettes if we are not talking to a local weevils system
    session = Session() if api_url else betamax_session

    yield WeevilsClient(token, api_url=api_url, session=session)
