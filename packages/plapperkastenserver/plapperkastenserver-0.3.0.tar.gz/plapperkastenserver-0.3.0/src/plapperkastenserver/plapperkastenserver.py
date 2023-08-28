"""Server for Plapperkasten."""

import http
import pathlib

from plapperkastenserver import config as plkconfig
from plapperkastenserver.httprequesthandler import HTTPRequestHandler

HOSTNAME = "localhost"
PORT = 8080

class PlapperkastenServer(http.server.HTTPServer):
    """A basic file server.

    This is a rather ugly workaroud since we can neither override
    `socketserver.StreamRequestHandler.__init__()` nor
    `http.server.Server.__init__()`.
    `HTTPRequestHandler` and `PlapperkastenServer` both have an `init()`
    function which needs to be called manually.

    `PlapperkastenServer` will call `HTTPRequestHandler`'s ``init()``
    but every script running `PlapperkastenServer` will need to call
    `init()` on it.
    """

    def init(self, config: plkconfig.Config) -> None:
        """Setup some important variables.

        We cannot override `__init__()` as clearly stated in the source.
        """
        # pylint: disable=attribute-defined-outside-init
        self.config: plkconfig.Config = config

    #def finish_request(self, request, client_address):
    #    """Finish one request by instantiating RequestHandlerClass."""
    #    request_handler: HTTPRequestHandler = self.RequestHandlerClass(
    #            request, client_address, self)
    #    request_handler.init(self.config)

def main() -> None:
    cfg: plkconfig.Config = plkconfig.Config()

    server: PlapperkastenServer = PlapperkastenServer((HOSTNAME, PORT),
                                                      HTTPRequestHandler)
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
