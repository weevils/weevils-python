from weevils import WeevilsClient


def test_list_weevils(client: WeevilsClient):
    weevils = client.get_weevils()
    assert len(weevils) > 0
    assert weevils[0].name == client.get_weevil(weevils[0].id).name


def test_create_oneoff_job(client: WeevilsClient):

    client.run()
