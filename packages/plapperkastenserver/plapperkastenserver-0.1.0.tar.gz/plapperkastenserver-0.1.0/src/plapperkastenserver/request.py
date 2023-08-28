"""
A basic HTTP server built upon code from the http.server module in 3.11.
"""

import collections
import http
import pathlib
import re
import urllib.parse

from typing import Optional, Pattern, Tuple

from plapperkastenserver.exceptions import HTTPError
#from plapperkastenserver.exceptions import HTTPBadRequestError, \
#        HTTPRequestTooLongError, HTTPVersionNotSupportedError

FieldEntry: tuple[str, Optional[str|bytes], Optional[str], Optional[str]] = \
        collections.namedtuple('FieldEntry', 'name value filename mime_type')

class Request():
    # pylint: disable=too-many-instance-attributes
    """A simple HTTP request.

    Attributes:
        requestline: The request sent by the client if valid or "".
        version: The HTTP version used by the client for the request.
        command: The command sent by the client
            [HEAD|GET|POST|UPDATE|PUT|DELETE|PATCH|CONNECT|TRACE|...].
        original_path: The original path from the request.
        path: The path without the query or fragment.
        path_decoded: The path decoded from html encoding.
        query: Everything after an eventual "?" and before "#".
        fragment: Everything after "#".
        headers: A dictionary of headers recieved from the client.
        data: The request's body. Parsed in case of multipart/form-data
            or application/x-www-form-urlencoded or stored with
            `FieldEntry.name = 'data'`
    """

    def __init__(self) -> None:
        """Initialise attributes."""
        self.requestline: str = ''
        # the default request version in case of a malformed request
        self.version: Tuple[int, int] = (0, 9)
        self.command: str = ''
        self.original_path: str = ''
        self.path: str = ''
        self.path_decoded: str = ''
        self.query: list[FieldEntry] = []
        self.fragment: str = ''
        self.headers: dict[str, str] = {}
        self.data: list[FieldEntry] = []

    def set_requestline(self, raw: bytes) -> None:
        """Add a raw request and perform very basic checks.

        Args:
            raw: String of bytes read from the request.

        Raises:
            HTTPRequestTooLongError on too long requests.
            HTTPBadRequestError on bad requests.
        """
        if len(raw) > 65536:
            raise HTTPError("request too long",
                            http.HTTPStatus.REQUEST_URI_TOO_LONG)

        if not raw:
            # nothing before first "\r\n"
            raise HTTPError("empty request",
                            http.HTTPStatus.BAD_REQUEST)

        self.requestline = raw.decode('iso-8859-1').rstrip('\r\n')

    def parse_requestline(self) -> None:
        """Parse the request line.

        It should be sructured like:
        COMMAND PATH HTTP/X.X\r\n

        Raises:
            HTTPBadRequestError on bad requests.
            HTTPVersionNotSupportedError if the requested version is not
                supported.
        """
        words: list[str] = self.requestline.split()

        if len(words) == 0:
            raise HTTPError("malformed request",
                            http.HTTPStatus.BAD_REQUEST)

        if len(words) >= 3:  # Enough to determine protocol version
            if not words[-1].startswith('HTTP/'):
                raise HTTPError(f"bad request version \"{words[-1]}\"",
                                http.HTTPStatus.BAD_REQUEST)

            base_version_number: str = words[-1].split('/', 1)[1]

            # RFC 2145 section 3.1 says there can be only one "." and
            #   - major and minor numbers MUST be treated as
            #      separate integers;
            #   - HTTP/2.4 is a lower version than HTTP/2.13, which in
            #      turn is lower than HTTP/12.3;
            #   - Leading zeros MUST be ignored by recipients.
            if base_version_number.count('.') != 1:
                raise HTTPError(f"bad request version \"{words[-1]}\"",
                                http.HTTPStatus.BAD_REQUEST)

            version_parts: list[str] = base_version_number.split('.')

            if (any(not part.isdigit() for part in version_parts) or
                any(len(part) > 10 for part in version_parts)):
                raise HTTPError(f"bad version \"{words[-1][0:30]}\"",
                                http.HTTPStatus.BAD_REQUEST)
            version_number = (int(version_parts[0]), int(version_parts[1]))

            if version_number >= (2, 0):
                raise HTTPError(
                        f"HTTP version not supported \"{base_version_number}\"",
                                http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED)
            self.version = version_number

        if not 2 <= len(words) <= 3:
            raise HTTPError(f"bad syntax \"{self.requestline}\"",
                            http.HTTPStatus.BAD_REQUEST)

        command, path = words[:2]

        if len(words) == 2:
            # HTTTP/0.9 request without version number
            if command != 'GET':
                raise HTTPError(f"bad HTTP/0.9 request \"{command}\"",
                                http.HTTPStatus.BAD_REQUEST)
        self.command, self.original_path = command, path

        # gh-87389: The purpose of replacing '//' with '/' is to protect
        # against open redirect attacks possibly triggered if the path starts
        # with '//' because http clients treat //path as an absolute URI
        # without scheme (similar to http://path) rather than a path.
        # reduce to a single /
        self.path = '/' + self.original_path.lstrip('/')
        parts: list[str]
        if '#' in self.path:
            parts = self.path.split('#', 1)
            self.path = parts[0]
            self.fragment = parts[1]
        if '?' in self.path:
            parts = self.path.split('?', 1)
            self.query = self.parse_query_string(parts[0])
        try:
            self.path_decoded = urllib.parse.unquote(
                    self.path, errors='surrogatepass')
        except UnicodeDecodeError:
            self.path_decoded = urllib.parse.unquote(self.path)

    def parse_headers(self, raw_headers: list[bytes]) -> None:
        """Parse the request headers.

        Args:
            request: The raw bytestream as recieved from the client.
        """
        for raw_header in raw_headers:
            header: str = raw_header.decode('iso-8859-1').strip()
            if header == '':
                continue
            if ':' not in header:
                continue
            key, value = header.split(':', 1)
            self.headers[key] = value.strip()

    def parse_query_string(self, raw: str) -> list[FieldEntry]:
        """Parse a query string.

        Taken from: <https://discuss.python.org/t/21960/6>

        Args:
            raw: The string to parse.
        """
        pattern_split: Pattern = re.compile(r'(?:^|&)([^&]*)')
        pattern_param: Pattern = re.compile(r'^(.*?)(?:=(.*))?$', re.DOTALL)
        result: list[FieldEntry] = []
        for param in (match.group(1) for match in pattern_split.finditer(raw)):
            param_matched = pattern_param.match(param)
            if param_matched:
                key, value = param_matched.groups()
                key = urllib.parse.unquote_plus(key)
                if value is not None:
                    value = value.replace('+', ' ')
                    value = urllib.parse.unquote(value)
                result.append(FieldEntry(key, value, None, None))
        return result

    def get_field_entry(self, name: str,
                        entry_list: list[FieldEntry]) -> FieldEntry:
        """Return the field entry with `name` from the list.

        Returns an empty FieldEntry with only the name if no matching
        entry is found.

        Args:
            name: The name of the field entry.
            entry_list: The list to search.
        """
        return next((entry for entry in entry_list if entry.name == name),
                    FieldEntry(name, None, None, None))

    def save_file(self, name: str, destination: pathlib.Path) -> pathlib.Path:
        """Save the file from the field entry with `name` to disk.

        Args:
            name: The name of the field entry.
            destination: Path where to store the file, a name will be
                appended if the path is a directory

        Raises:
            ValueError: If the field entry `name` does not hold a file.
            OSError: In case of failing to save the file.
            FileExistsError: If a file exists at the destination.

        Returns:
        The path to the stored file.
        """
        entry: FieldEntry = self.get_field_entry(name, self.data)
        if not entry.value or not entry.filename:
            raise ValueError(f"FieldEntry \"{name}\" does not contain a file.")
        if destination.is_dir():
            destination = destination / entry.filename
        if destination.exists():
            raise FileExistsError(f"file \"{entry.filename}\" already exists")

        destination.write_bytes(entry.value)

        return destination
