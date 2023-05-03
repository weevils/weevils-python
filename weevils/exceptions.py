from urllib.parse import urlparse

from requests import Response


class WeevilsConfigurationError(Exception):
    pass


# ---
# HTTP Exceptions
# ---


class BaseResponseException(Exception):
    """
    Common base exception
    """

    def __init__(self, response: Response, message=None):
        self.response = response

        if response is not None:
            if hasattr(response, "get") and response.get("Content-Type") != "application/json":
                self.detail = "path does not exist"
            else:
                data = response.json()
                if isinstance(data, dict):
                    self.detail = data.get("detail", "[no detail]")
                else:
                    self.detail = data

        message = message or self.detail
        super().__init__(message)


class UnhandledResponse(BaseResponseException):
    """
    This is the catchall exception to throw for any HTTP response which was not cleanly handled.

    (This eventually should not happen once the services and clients mature...)
    """

    def __init__(self, response: Response):
        super().__init__(response, f"Unhandled response: {response.status_code}")


class BadRequest(BaseResponseException):
    """
    If the data given to the client was not liked by the service
    """


class ServiceProcessingError(BaseResponseException):
    """
    This is raised from an HTTP 500 response where the server responded but did not handle the
    request correctly
    """


class ServiceUnavailable(BaseResponseException):
    """
    This is raised from an HTTP 502 or 504, when the service is not responding
    """


class ActionDisallowed(BaseResponseException):
    """
    If the caller is not allowed to do the given action. The authentication has worked correctly,
    but the action is not allowed for the authenticated user.
    """

    # TODO: this is both "you can't add an app to a host you do not own" and "your JWT is invalid" ...
    #       need to split "action not allowed" from "403 forbidden" due to lack of correct auth


class NotAuthenticated(BaseResponseException):
    """
    This means that the caller is not authenticated, either because there was no Authorization header passed
    or because the contents are not a valid JWT.
    """


class ImproperlyConfigured(Exception):
    """
    General exception to throw when missing some configuration value, for example the basic settings for
    service location
    """


class WriteConflict(BaseResponseException):
    """
    General exception for trying to create an object with some unique constraint which already exists
    """


class EntityNotFound(BaseResponseException):
    """
    Generic error message to throw when a service responds to a request to a resource with a 404
    """

    def __init__(self, dto_class, response=None, message: str = None):
        if response is not None:
            parsed = urlparse(response.url)
            message = f"{dto_class} {parsed.path}"
        super().__init__(response, message)


__all__ = (
    "WeevilsConfigurationError",
    "UnhandledResponse",
    "EntityNotFound",
    "ActionDisallowed",
    "BadRequest",
    "ImproperlyConfigured",
    "ServiceUnavailable",
    "NotAuthenticated",
    "ServiceProcessingError",
    "WriteConflict",
)
