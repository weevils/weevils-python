from weevils import WeevilsClient


def test_get_repository(client: WeevilsClient):
    repo = client.github.repository("carlio", "django-flows")
    assert repo is not None
