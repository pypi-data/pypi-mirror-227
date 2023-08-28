"""
A basic HTTP server built upon code from the http.server module in 3.11.
"""

import datetime
import email.message
import email.parser
import email.policy
import email.utils
import http
import http.client
import http.server
import itertools
import os
import posixpath
import re
import shutil
import socketserver
import time
import urllib.parse

from typing import Match, Optional, Tuple

from plapperkastenserver.exceptions import HTTPError
from plapperkastenserver import config as plkconfig
from plapperkastenserver.request import Request, FieldEntry
from plapperkastenserver.response import Response

class HTTPRequestHandler(socketserver.StreamRequestHandler):
    """HTTP request handler base class.

    Attributes:
        close_connection: Indiciator whether to keep connection alive
            or not.
        rules: A set of rules for matching requests.
        config: Basic server configuration.

    """
    rules: list[Tuple[str, str, str]] = []

    #def __init__(self, *args, **kwargs) -> None:
    def __init__(self, request, client_address, server) -> None:
        # pylint: disable=super-init-not-called
        """Initialise.

        Args:
            server_config: A basic
        """
        self.close_connection: bool = True

        # define here instead of in `init()` so pylint stops complaining
        self.config: plkconfig.Config

        #super().__init__(*args, **kwargs)
        # from `BaseRequestHandler.__init__()` which we don't call
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()

    def init(self, config: plkconfig.Config) -> None:
        """Use this to initialise some variables.

        We cannot change `__init__` otherwise linting would complain.
        """
        self.config = config

        # from `BaseRequestHandler.__init__()` which we don't call
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def handle_one_request(self) -> None:
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        self.close_connection = True
        request: Request = Request()
        response: Response = Response(self.config.html_error_page)

        try:
            raw_requestline: bytes = self.rfile.readline(65537)
            request.set_requestline(raw_requestline)
            request.parse_requestline()
            self.log_request(request)
            request.parse_headers(self.read_headers())

            connection_type = request.headers.get('Connection', '')
            if connection_type.lower() == 'close':
                self.close_connection = True
            elif (connection_type.lower() == 'keep-alive' and
                  response.version >= (1, 1)):
                self.close_connection = False
            expect = request.headers.get('Expect', "")
            if (expect.lower() == "100-continue" and
                    response.version >= (1, 1) and
                    request.version >= (1, 1)):
                self.handle_expect_100(response)

            if request.version >= (1, 1) and response.version >= (1, 1):
                self.close_connection = False

            self.handle_method(request, response)
        except TimeoutError:
            # reading timed out
            self.log_error(request, 'request timed out')
            response.create_error_response(http.HTTPStatus.REQUEST_TIMEOUT)
        except HTTPError as error:
            self.log_error(request, str(error))
            response.create_error_response(error.status, error.message_short,
                                           error.message_long)

        try:
            if response.has_file():
                try:
                    with open(response.get_file(), 'rb') as filehandle:
                        self.wfile.write(response.compile(request.version))
                        shutil.copyfileobj(filehandle, self.wfile)
                except OSError:
                    # can't access the file anymore
                    response.create_error_response(http.HTTPStatus.NOT_FOUND)
                    self.log_error(request, f"file gone: \"{request.path}\"")
            else:
                self.wfile.write(response.compile(request.version))
            self.wfile.flush()
            self.log_response(response)

            if response.check_headers('Connection', 'close'):
                self.close_connection = True
            elif response.check_headers('Connection', 'keep-alive'):
                self.close_connection = False
        except TimeoutError:
            # writing timed out
            self.log_error(request, 'Request timed out')
            self.close_connection = True
            return

    def read_headers(self) -> list[bytes]:
        """Reads potential header lines into a list from a file pointer.

        Length of line is limited to 56636 bytes and number of
        headers is limited to 1000.

        Raises:
            HTTPHeaderTooLongError if a header surpasses 65536 bytes.
            HTTPTooManyHeadersError if there are more than 100 headers.
        """
        headers: list[bytes] = []
        while True:
            line: bytes = self.rfile.readline(65536 + 1)
            if len(line) > 65536:
                raise HTTPError('header line longer than 65536 bytes',
                                http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE)
            headers.append(line)
            if len(headers) > 100:
                raise HTTPError('got more than 100 headers',
                                http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE)
            if line in (b'\r\n', b'\n', b''):
                break
        return headers

    def handle_expect_100(self, response: Response) -> None:
        """Decide what to do with an "Expect: 100-continue" header.

        If the client is expecting a 100 Continue response, we must
        respond with either a 100 Continue or a final response before
        waiting for the request body. The default is to always respond
        with a 100 Continue. You can behave differently (for example,
        reject unauthorized requests) by overriding this method.

        Args:
            response: The response to build.
        """
        response.set_status(http.HTTPStatus.CONTINUE)

    def handle_regex_matched_paths(self, request: Request,
                                   response: Response,
                                   headers_only: bool = False) -> None:
        """
        Match the path againt regular expressions and call the
        corresponding function to build the response.

        Args:
            request: The request.
            response: The response to build.
            headers_only: Omit the body when building the response.
        """
        for command, rule, functionname in self.rules:
            if command != request.command:
                continue
            regex: str = self.convert_rule_to_regex(rule)
            match: Optional[Match] = re.match(regex, request.path_decoded)
            params: dict[str, str] = {}
            if match:
                params = match.groupdict()
                if not hasattr(self, functionname):
                    raise HTTPError(f"no function defined for rule \"{rule}\"",
                                    http.HTTPStatus.NOT_FOUND)
                getattr(self, functionname)(request, response, headers_only,
                                            **params)

    def convert_rule_to_regex(self, rule: str) -> str:
        # pylint: disable=anomalous-backslash-in-string
        """
        Convert a rule to match an URL to a regular expression.

        A rule might look like:
        "/name/{name}/age/{age}/"

        This will be converted to:
        r"^\/name\/(?P<name>[a-zA-Z0-9]+)\/age\/(?P<age>[a-zA-Z0-9]+)\/$"

        Args:
            rule: The rule to convert.
        """
        # create named groups from placeholders
        regex: str = rule.replace('{', '(?P<')
        regex = regex.replace('}', '>[a-zA-Z0-9]+)')
        # escape slashes
        regex = regex.replace('/', '\/')
        # require a full match
        regex = f"^{regex}$"
        return regex

    def handle_path(self, request: Request,
                    response: Response,
                    list_directory = True,
                    headers_only = False) -> None:
        # pylint: disable=too-many-branches
        """Common code for GET and HEAD commands.

        Tries to look up the path and:
        * redirects if a directory was requested but without a trailing
            slash.
        * lists the directory if `list_directory` is `True`.
        * sends NOT MODIFIED if a cached file with the same mtmime
            exists in the client.
        * prepares the headers for a file if the file is accessible.
        * prepares the file to be sent if `headers_only` is `False`.

        Args:
            request: The request.
            response: The response to build.
            list_directory: Allow listing of directories.
            headers_only: Omit the body when building the response.
        """
        path: str = self.translate_path(request.path_decoded)
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(request.path)
            if not parts.path.endswith('/'):
                # append a "/" to the originally requested path
                # and let the client run the request again
                # next time (with the "/") we will look if there's an
                # index file
                response.set_status(http.HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                response.add_header('Location', new_url)
                response.add_header('Content-Length', '0')
                return

            for index in 'index.html', 'index.htm':
                index = os.path.join(path, index)
                if os.path.isfile(index):
                    path = index
                    break
            else:
                if list_directory:
                    response.create_directory_listing_response(
                            path, str(self.config.path_www),
                            headers_only)
                    return
                raise HTTPError('directory requested, but listing disabled',
                                http.HTTPStatus.FORBIDDEN)

        if path.endswith("/"):
            raise HTTPError('non-directory path ends with slash',
                            http.HTTPStatus.NOT_FOUND)

        try:
            with open(path, 'rb') as filehandle:
                fstat: os.stat_result = os.fstat(filehandle.fileno())
                # Use browser cache if possible
                if ("If-Modified-Since" in request.headers
                        and "If-None-Match" not in request.headers):
                    try:
                        mtime_client: datetime.datetime = \
                                email.utils.parsedate_to_datetime(
                                        request.headers["If-Modified-Since"])
                    except (TypeError, IndexError, OverflowError, ValueError):
                        pass
                    else:
                        if mtime_client.tzinfo is None:
                            # obsolete format with no timezone, assume utc
                            mtime_client = mtime_client.replace(
                                    tzinfo=datetime.timezone.utc)
                        mtime_local = datetime.datetime.fromtimestamp(
                            fstat.st_mtime, tz=datetime.datetime.now(
                                datetime.timezone(
                                    datetime.timedelta(0))).astimezone().tzinfo)
                        # remove microseconds, like in If-Modified-Since
                        mtime_local = mtime_local.replace(microsecond=0)

                        if mtime_local <= mtime_client:
                            response.set_status(
                                    http.HTTPStatus.NOT_MODIFIED)
                            return
                response.create_file_response(path, filehandle, headers_only)
        except OSError as error:
            raise HTTPError(f"could not open requested file \"{path}\"",
                            http.HTTPStatus.NOT_FOUND) from error

    def translate_path(self, request_path: str) -> str:
        """Merge the requested path on top of the server base path.

        Components that mean special things to the local file system
        (e.g. drive or directory names, '.' and '..') are ignored.

        Args:
            request_path: The path from the request, with only one
                leading slash.
        """
        trailing_slash = request_path.rstrip().endswith('/')
        path = posixpath.normpath(request_path)
        parts: list[str] = path.split('/')
        parts = list(filter(None, parts))
        path = str(self.config.path_www)
        for part in parts:
            if os.path.dirname(part) or part in (os.curdir, os.pardir):
                # ignore parts that can in itself be translated to a path
                # or '.' and '..'
                continue
            path = os.path.join(path, part)
        if trailing_slash:
            path += '/'
        return path

    def handle_method(self, request: Request, response: Response) -> None:
        """Handle request depending on its HTTP command / method.

        Args:
            request: The request.
            response: The response to build.
        """
        if request.command not in ('HEAD', 'GET', 'POST', 'UPDATE', 'PUT',
                                   'DELETE'):
            # leave out: 'PATCH', 'CONNECT', 'TRACE'
            self.log_error(request, 'unsupported method')
            raise HTTPError(f"Unsupported method ({request.command})",
                            http.HTTPStatus.NOT_IMPLEMENTED)
        headers_only: bool = request.command == 'HEAD'
        try:
            if request.command != 'GET':
                request.data = self.handle_data(request)
            self.handle_regex_matched_paths(request, response,
                                            headers_only=headers_only)

            if not response.get_status():
                # no response has been built
                if request.command in ('GET', 'HEAD'):
                    self.handle_path(request, response,
                                     headers_only=headers_only)
                else:
                    raise HTTPError(f"not found: ({request.path_decoded})",
                                    http.HTTPStatus.NOT_FOUND)
        except TimeoutError as error:
            raise HTTPError('timed out reading post data',
                            http.HTTPStatus.REQUEST_TIMEOUT) from error

    def handle_data(self, request: Request) -> list[FieldEntry]:
        """Handle request bodys.

        Code built upon code from the Bottle project, so credits to:
        <https://github.com/bottlepy/bottle/>

        Args:
            request: The request.
        """
        data: list[FieldEntry] = []
        length: int = int(request.headers.get('Content-Length', 0))
        content_type: str = request.headers.get('Content-Type',
                                                'text/plain')
        message = email.message.Message()
        message.add_header('Content-Type', content_type)
        # try to get the contents encoding from the headers
        # if not set use the encoding used by this site (stored in html_config)
        # as the form data will be in the same encoding as the form
        # if something else is desired it must be specified in
        # `enctype="multipart/form-data; charset=ENCODING"`
        # or sent in the headers by the client (see first approach=:
        # `Content-Type: multipart/form-data; charset=ENCODING`
        # or
        # take the returned string encode it and decode it using the desired
        # encoding.
        charset: str = (message.get_content_charset() or
                        self.config.encoding_default)
        match message.get_content_type():
            case 'application/x-www-form-urlencoded':
                body: str = self.rfile.read(length).decode(charset)
                data = request.parse_query_string(body)
            case 'multipart/form-data':
                parser = email.parser.BytesFeedParser(
                        policy=email.policy.HTTP)
                parser.feed(
                        f"Content-Type: {content_type}\r\n".encode('utf-8'))
                parser.feed('\r\n'.encode('utf-8'))
                parser.feed(self.rfile.read(length))
                message = parser.close()
                del parser
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    name: str = email.utils.collapse_rfc2231_value(
                            part.get_param(
                                'name', header='content-disposition'))
                    filename: Optional[str] = part.get_filename(None)
                    mime_type: str = part.get_content_type()
                    # if filename is empty treat
                    data.append(FieldEntry(
                        name,
                        part.get_payload(decode=True) if filename else \
                                part.get_payload(decode=True).decode(charset),
                        filename,
                        mime_type))
            case parsed_content_type:
                body = self.rfile.read(length).decode(charset)
                data = [FieldEntry(parsed_content_type, body, None,
                                   parsed_content_type)]
        return data

    def log_request(self, request: Request) -> None:
        """Log an accepted request.

        Args:
            request: The request.
        """
        try:
            requestline: str = urllib.parse.unquote(
                    request.requestline, errors='surrogatepass')
        except UnicodeDecodeError:
            requestline = urllib.parse.unquote(request.requestline)
        self.log_message(requestline)

    def log_response(self, response: Response) -> None:
        """Log an response.

        Args:
            response: The response.
        """
        self.log_message(response.get_statusline())

    def log_error(self, request: Request,
                  message: str = '') -> None:
        """Log an error.

        Args:
            request: The request.
            message: A message what has gone wrong.
        """
        self.log_message(f"{request.requestline}: {message}")

    # https://en.wikipedia.org/wiki/List_of_Unicode_characters#Control_codes
    _control_char_table = str.maketrans(
            {c: fr'\x{c:02x}' for c in
             itertools.chain(range(0x20), range(0x7f,0xa0))})
    _control_char_table[ord('\\')] = r'\\'

    def log_message(self, message: str, *args: list[str]):
        """Log an arbitrary message.

        Args:
            message: The message to log, can be a format string.
            *args: Strings passed to the format string.
        """

        message = message % args
        print(f"{self.get_address_string()} - - "
              f"[{self.get_date_time_string()}] "
              f"{message.translate(self._control_char_table)}")

    def get_date_time_string(self) -> str:
        """Return the current time formatted for logging."""
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_address_string(self) -> str:
        """Return the client address."""
        return self.client_address[0]
