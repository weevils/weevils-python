import pytest

from tests.utils import random_string
from weevils import WeevilsClient
from weevils.exceptions import EntityConflict


def test_unique_names(client: WeevilsClient):
    script = "echo 'me again'"
    base = client.list_bases()[0]

    name = random_string()
    weevil = client.create_weevil(name, base, script)
    assert weevil is not None

    # can't have two with the same name...
    with pytest.raises(EntityConflict):
        client.create_weevil(name, base, script)


def test_create_and_run_weevil(client: WeevilsClient):
    script = "echo 'yo what is up'"
    base = client.list_bases()[0]
    weevil = client.create_weevil(random_string(), base, script)
    assert weevil.slug is not None

    repo = client.github.repository("carlio", "django-flows")
    assert repo is not None

    job = weevil.run(repo)
    assert job.status == "Queued"


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
