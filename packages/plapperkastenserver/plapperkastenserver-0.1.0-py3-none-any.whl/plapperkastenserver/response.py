"""
A basic HTTP server built upon code from the http.server module in 3.11.
"""
import email.utils
import html
import http
import http.client
import http.server
import mimetypes
import os
import posixpath
import sys
import time
import urllib.parse

from typing import BinaryIO, Optional, Tuple

from plapperkastenserver import htmltemplate

class Response():
    """A simple HTTP response.

    Attributes:
        _body: An encoded bytestream holding the body of the response.
        error_page: The error page to send on error.
        _extensions_map: Map extensions to MIME types.
        _file: Path to a file that should be sent with the response.
        _headers: A dicitionary of headers.
        version: The protocol version to use.
        _responses: Dictionary mapping HTTPStatus to short messages and
            slightly longer explanation.
        _server_version: The version if the server as sent to the
            client.
        _status: The status und short message for the response.
        _statusline: The statusline as sent to the client for logging
            purposes.
        _system_version: System version as sent to the client.
    """

    _system_version: str = "Python/" + sys.version.split()[0]
    # TODO
    _server_version: str = "PlapperkastenHTTP/0.1"
    _extensions_map: dict[str, str] = {
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
    }
    _responses: dict[str, Tuple[str, str]] = {
        str(value): (value.phrase, value.description)
        for value in http.HTTPStatus.__members__.values()
    }

    def __init__(self, error_page: htmltemplate.ErrorPage) -> None:
        """Initialise attributes."""
        self._status: Optional[Tuple[http.HTTPStatus, str]] = None
        self._statusline: str = ''
        self._headers: dict[str, str] = {}
        self._body: bytes = b''
        self._file: str = ''
        self.version: Tuple[int, int] = (1, 0)
        self.error_page: htmltemplate.ErrorPage = error_page

    def get_standard_message(self, status: http.HTTPStatus) -> Tuple[str, str]:
        """Returns a short and a long message associated with the status.

        Args:
            status: The HTTP status to look up.
        """
        try:
            message_short, message_long = self._responses[str(status)]
        except KeyError:
            message_short = '???'
            message_long = '???'
        return (message_short, message_long)

    def set_status(self, status: http.HTTPStatus, message: str = '') -> None:
        """Add information that will form the statusline."""
        if message == '':
            message = self.get_standard_message(status)[0]

        self._status = (status, message)

    def get_status(self) -> Optional[http.HTTPStatus]:
        """Return the status.

        Will return http.HTTPStatus.SERVICE_UNAVAILABLE as default.
        """
        if not self._status:
            return self._status
        return self._status[0]

    def get_statusline(self) -> str:
        """Return the statusline as string."""
        return self._statusline

    def add_header(self, key: str, value: str) -> None:
        """Add an header to the buffer."""
        self._headers[key] = value

    def add_standard_headers(self) -> None:
        """Adds standard headers like server info and date."""
        self.add_header('Server', self.get_version_string())
        self.add_header('Date', self.get_date_time_string())

    def set_body(self, content: str, content_type: str = 'text/html',
                 encoding = 'utf-8') -> None:
        """Set the response body (replaces previous content).

        Only use for text. If you want to send a file use `add_file()`.

        Args:
            content: The content.
            content_type: Content type, should be a valid MIME type.
            encoding: The encoding used.
        """
        self._body = content.encode(encoding, 'replace')
        self.add_header('Content-Type', f"{content_type}; charset={encoding}")
        self.add_header('Content-Length', str(len(self._body)))
        if not self._status:
            self.set_status(http.HTTPStatus.OK)

    def set_body_from_template(self,
                               template: htmltemplate.HTMLTemplate) -> None:
        """Set the body from template (replaces previous content).

        Only use for text. If you want to send a file use `add_file()`.

        Args:
            template: The template to use.
        """
        self._body = template.compile().encode(template.encoding, 'replace')
        self.add_header('Content-Type',
                        f"{template.content_type}; charset={template.encoding}")
        self.add_header('Content-Length', str(len(self._body)))
        if not self._status:
            self.set_status(http.HTTPStatus.OK)

    def get_version_string(self):
        """Return the server software version string."""
        return self._server_version + ' ' + self._system_version

    def get_date_time_string(self, timestamp: Optional[float] = None) -> str:
        """Return the current date and time formatted for a message header.

        Args:
            time: The time to format.
        """
        if timestamp:
            return email.utils.formatdate(timestamp, usegmt=True)
        return email.utils.formatdate(time.time(), usegmt=True)

    def check_headers(self, key: str, value: str) -> bool:
        """Is there a header with a certain value?

        Args:
            key: The key to look up.
            value: The value to compare.
        """
        if not key in self._headers:
            return False
        return self._headers[key] == value

    def has_file(self) -> bool:
        """Is there a file in the response?"""
        return self._file != ''

    def get_file(self) -> str:
        """Return the path of the file to send."""
        return self._file

    def compile(self, request_version: Tuple[int, int]) -> bytes:
        """Compile a complete response.

        Args:
            request_version: The version of the request, mainly to
                respond to old HTTP/0.9 requests
        """
        response: bytes = self.compile_status_line(request_version)
        response += self.compile_headers(request_version)
        if len(self._body) > 0:
            response += self._body
        return response

    def compile_status_line(self, request_version: Tuple[int, int]) -> bytes:
        """Compile the statusline.

        Args:
            request_version: The version of the request, mainly to
                respond to old HTTP/0.9 requests
        """
        if request_version == (0, 9):
            # HTML/0.9 did not have a statusline nor headers
            return b''
        if not self._status:
            self.set_status(http.HTTPStatus.SERVICE_UNAVAILABLE)

        if self._status:
            self._statusline = (f"HTTP/{self.version[0]}.{self.version[1]} "
                                f"{str(self._status[0].value)} "
                                f"{str(self._status[1])}")
        return f"{self._statusline}\r\n".encode('iso-8859-1', 'strict')

    def compile_headers(self, request_version: Tuple[int, int]) -> bytes:
        """Compile headers for sending.

        Args:
            request_version: The version of the request, mainly to
                respond to old HTTP/0.9 requests
        """
        if request_version == (0, 9):
            # HTML/0.9 did not have a statusline nor headers
            return b''

        if 'Server' not in self._headers or 'Date' not in self._headers:
            self.add_standard_headers()

        headers: bytes = b''
        for key, value in self._headers.items():
            headers += f"{key}: {value}\r\n".encode('iso-8859-1', 'strict')
        # emtpy line marks the end of headers
        headers += b'\r\n'
        return headers

    def create_error_response(self, status: http.HTTPStatus,
                              message: str = '', explanation: str = '',
                              headers_only: bool = False) -> None:
        """Create a standard error response.

        Args:
            status: An http status.
            message: Optional 1 line reason.
            explain: Optional more detailed error message.
            headers_only: Omit the body.
        """
        message_short, message_long = self.get_standard_message(status)

        if message == '':
            message = message_short
        if explanation == '':
            explanation = message_long

        self.set_status(status, message)
        self.add_header('Connection', 'close')

        # Message body is omitted for cases described in:
        #  - RFC7230: 3.3. 1xx, 204(No Content), 304(Not Modified)
        #  - RFC7231: 6.3.6. 205(Reset Content)
        if (not headers_only and int(status) >= 200 and status not in
            (http.HTTPStatus.NO_CONTENT, http.HTTPStatus.RESET_CONTENT,
             http.HTTPStatus.NOT_MODIFIED)):
            # HTML encode to prevent Cross Site Scripting attacks
            # (see bug #1100201)
            self.error_page.variables = {
                'status': str(status.value),
                'message': html.escape(message, quote=False),
                'explanation': html.escape(explanation, quote=False)}
            self.set_body_from_template(self.error_page)

    def create_directory_listing_response(self, directory: str,
                                          base_directory: str,
                                          headers_only: bool) -> None:
        """Create a directoy listing as response.

        Args:
            directory: The directory to list.
            headers_only: Prepare a response without a body.
        """
        self.set_status(http.HTTPStatus.OK)
        if headers_only:
            return

        try:
            dir_content: list[str] = os.listdir(directory)
        except OSError:
            self.create_error_response(http.HTTPStatus.FORBIDDEN, '',
                                       'No permission to list directory')
            return
        dir_content.sort(key=lambda a: a.lower())
        try:
            displaypath: str = urllib.parse.unquote(directory,
                                                    errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(directory)
        displaypath = displaypath.replace(base_directory, '')
        displaypath = html.escape(displaypath, quote=False)
        link_list: str = ''

        for name in dir_content:
            full_path: str = os.path.join(directory, name)
            link_path: str = os.path.join(displaypath, name)
            # Append / for directories or @ for symbolic links
            if os.path.isdir(full_path):
                link_name: str = name + '/'
                link_path = link_path + '/'
            if os.path.islink(full_path):
                link_name = name + '@'
                # Note: a link to a directory displays with @ and links with /
            link_path = urllib.parse.quote(link_path, errors='surrogatepass')
            link_name = html.escape(link_name, quote=False)
            link_list += f"<li><a href=\"{link_path}\">{link_name}</a></li>"
        title = displaypath
        self.set_body(
                (f"<html><head><title>{title}</title></head><body>"
                 f"<h1>{displaypath}</h1><hr/>"
                 f"<ul>{link_list}</ul>"
                 f"</body></html>"), 'text/html', 'utf-8')

    def create_file_response(self, path: str, filehandle: BinaryIO,
                             headers_only: bool) -> None:
        """Send a file as the response.

        Args:
            path: The filesystem path.
            filehandle: A file handle. Needs to be opened and closed by the
                caller!
            headers_only: Prepare a response without a body.
        """
        ctype: str = self.guess_mime_type(path)
        fstat: os.stat_result = os.fstat(filehandle.fileno())
        self.set_status(http.HTTPStatus.OK)
        self.add_header("Content-type", ctype)
        self.add_header("Content-Length", str(fstat.st_size))
        self.add_header("Last-Modified", self.get_date_time_string(
            fstat.st_mtime))
        if headers_only:
            return
        self._file = path

    def guess_mime_type(self, path: str) -> str:
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        _, ext = posixpath.splitext(path)
        if ext in self._extensions_map:
            return self._extensions_map[ext]
        ext = ext.lower()
        if ext in self._extensions_map:
            return self._extensions_map[ext]
        guess, _ = mimetypes.guess_type(path)
        if guess:
            return guess
        return 'application/octet-stream'
