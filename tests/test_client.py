import pytest

from weevils import WeevilsClient


def test_host_shortcuts(client: WeevilsClient):
    # test shorthands
    gh = client.github
    assert gh is not None
    assert gh.name == "GitHub"


def test_fetching_hosts(client: WeevilsClient):
    # test regular lookup by ID and slug
    for host in client.list_hosts():
        assert client.get_host(host.slug) is not None
        assert client.get_host(host.id) is not None


def test_bad_arguments(client: WeevilsClient):
    with pytest.raises(ValueError):
        client.get_host(None)
        client.get_host("")
