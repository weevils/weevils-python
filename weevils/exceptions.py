from requests import Response


class WeevilsConfigurationError(Exception):
    pass


class WeevilsAPIException(Exception):
    def __init__(self, response: Response):
        super().__init__(
            f"Received unexpected response from Weevils API: status {response.status_code}\n" f"{response.content}"
        )


class EntityNotFound(Exception):
    def __init__(self, entity_type: str, criteria: str):
        super().__init__(f"Could not find entity of type {entity_type} with criteria {criteria}")
