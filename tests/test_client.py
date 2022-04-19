from weevils import WeevilsClient


def test_list_weevils(client: WeevilsClient):
    client.get_weevils()
