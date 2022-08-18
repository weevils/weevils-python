from requests import Response


class WeevilsConfigurationError(Exception):
    pass


class WeevilsAPIException(Exception):
    def __init__(self, response: Response):
        super().__init__(
            f"Received unexpected response from Weevils API: status {response.status_code}\n" f"{response.content}"
        )
        self.status_code = response.status_code
        self.error = response.content


class EntityNotFound(Exception):
    def __init__(self, entity_type: str, criteria: str):
        super().__init__(f"Could not find entity of type {entity_type} with criteria {criteria}")
        self.entity_type = entity_type
        self.criteria = criteria


class EntityConflict(Exception):
    pass


class WeevilsAPIConnectionError(Exception):
    def __init__(self, api_url: str):
        super().__init__(f"Could not connect to the Weevils API at {api_url}")
