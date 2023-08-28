"""
Custom exceptions for PlapperkastenServer.
"""

import http

class HTTPError(Exception):
    """Basic exception to derive HTTP-related exceptions from."""
    def __init__(self, message: str, status: http.HTTPStatus,
                 message_short: str = '', message_long: str = '') -> None:
        self.status = status
        self.message_short = message_short
        self.message_long = message_long
        super().__init__(message)
#
#class HTTPBadRequestError(HTTPError):
#    """Malformed request."""
#
#class HTTPRequestTooLongError(HTTPError):
#    """Request > 65536 bytes."""
#
#class HTTPVersionNotSupportedError(HTTPError):
#    """Requested HTTP version is not supported."""
#
#class HTTPHeaderTooLongError(HTTPError):
#    """Header line with > 65536 bytes."""
#
#class HTTPTooManyHeadersError(HTTPError):
#    """Too many HTTP headers."""
