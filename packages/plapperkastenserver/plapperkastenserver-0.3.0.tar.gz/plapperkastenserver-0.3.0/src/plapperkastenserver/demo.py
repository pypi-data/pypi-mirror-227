"""Demonstrate the server."""

import http
import pathlib

from plapperkastenserver import plapperkastenserver
from plapperkastenserver import config as plkconfig
from plapperkastenserver import htmltemplate
from plapperkastenserver.httprequesthandler import HTTPRequestHandler
from plapperkastenserver.request import Request
from plapperkastenserver.response import Response
from plapperkastenserver.exceptions import HTTPError

HOSTNAME = "localhost"
PORT = 8080

class SimpleTemplatePage(htmltemplate.HTMLTemplate):
    """A demo page."""
    def __init__(self, config: plkconfig.Config, template: str) -> None:
        # pylint: disable=too-many-arguments
        """Contructor."""
        super().__init__(config)
        self.set_template_file(template)

class AnswerPage(htmltemplate.HTMLTemplate):
    """A demo answer page."""
    def __init__(self, config: plkconfig.Config, answer: str = '') -> None:
        # pylint: disable=too-many-arguments
        """Contructor."""
        super().__init__(config, answer=answer)
        self.template = '<h1>The answer to ALL questions is: $answer</h1>'

class DemoRequestHandler(HTTPRequestHandler):
    """A demo."""
    rules = [
        ('GET', '/answer/{answer}', 'check_answer'),
        ('GET', '/form', 'display_form'),
        ('POST', '/form', 'upload')
    ]

    def display_form(self,
                     request: Request,
                     response: Response,
                     headers_only: bool) -> None:
        """Display an upload form.

        Args:
            request: The request sent by the client.
            response: The response to build.
            headers_only: Omit the body?
        """
        if headers_only:
            response.set_status(http.HTTPStatus.OK)
            return
        response.set_body(
                SimpleTemplatePage(
                    self.config,
                    template='upload.html').compile())

    def upload(self,
                     request: Request,
                     response: Response,
                     headers_only: bool) -> None:
        """Store the uploaded file.

        Args:
            request: The request sent by the client.
            response: The response to build.
            headers_only: Omit the body?
        """
        template: SimpleTemplatePage = SimpleTemplatePage(
                    self.config,
                    template='result.html')
        path: pathlib.Path = request.save_file('file',
                                               self.config.path_www)
        template.variables = {
                'src': str(path)[len(str(self.config.path_www)):],
                'text': request.get_field_entry('text', request.data).value}

        if headers_only:
            response.set_status(http.HTTPStatus.OK)
            return
        response.set_body(template.compile())


    def check_answer(self,
                     request: Request,
                     response: Response,
                     headers_only: bool,
                     answer: str) -> None:
        """Reveal the answer.

        Args:
            request: The request sent by the client.
            response: The response to build.
            headers_only: Omit the body?
            answer: The answer
        """
        if answer != '42':
            raise HTTPError('wrong answer', http.HTTPStatus.CONFLICT, '',
                            f"{answer} is not the answer.")
        if headers_only:
            response.set_status(http.HTTPStatus.OK)
        else:
            response.set_body(
                    AnswerPage(
                        self.config,
                        answer=answer).compile())
def main() -> None:
    cfg: plkconfig.Config = plkconfig.Config()

    server: plapperkastenserver.PlapperkastenServer = \
            plapperkastenserver.PlapperkastenServer((HOSTNAME, PORT),
                                                    DemoRequestHandler)
    server.init(cfg)
    print(f"Server started http://{HOSTNAME}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    main()
