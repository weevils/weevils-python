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


def test_bad_arguments_for_host(client: WeevilsClient):
    with pytest.raises(ValueError):
        client.get_host(None)
        client.get_host("")


def test_get_repository(client: WeevilsClient):
    repo = client.github.repository("carlio", "django-flows")
    assert repo is not None


def test_run_weevil(client: WeevilsClient):
    repo = client.github.repository("carlio", "django-flows")
    weevils = client.list_weevils()
    assert len(weevils) > 0
    for weevil in weevils:
        job = weevil.run(repo.id)
        assert job is not None

        ret_job = client.get_job(job.id)
        assert ret_job is not None
        assert ret_job.id == job.id


def test_list_weevils(client: WeevilsClient):
    weevils = client.list_weevils()
    assert len(weevils) > 0
    for weevil in weevils:
        assert client.get_weevil(weevil.id) is not None
