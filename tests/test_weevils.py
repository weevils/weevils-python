from weevils import WeevilsClient


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
