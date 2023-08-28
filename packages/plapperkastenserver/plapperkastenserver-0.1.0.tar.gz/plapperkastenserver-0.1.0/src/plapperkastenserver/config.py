"""A configuration for plapperkastenserver."""

#import dataclasses
import pathlib

from typing import Optional

from plapperkastenserver import htmltemplate

#@dataclasses.dataclass
#class Config:
#    # pylint: disable=too-many-instance-attributes
#    """Simple configuration for the server.
#
#    Attributes:
#        path_base: Base path, usually contains `path_www` and
#            `path_templates`.
#        path_templates: Path to the templates.
#        path_public: Path to the public directory (base for links).
#    """
#    path_base: pathlib.Path = pathlib.Path(__file__).parent.absolute()
#    path_www: pathlib.Path = path_base / 'wwww'
#    path_templates: pathlib.Path = path_base / 'templates'
#
#    site_title: str = 'Plapperkasten'
#    encoding_default: str = 'utf-8'
#    language_default: str = 'de'
#    html_css_default: list[str] = []
#    html_javascript_default: list[str] = []

class Config:
    # pylint: disable=too-many-instance-attributes
    """Simple configuration for the server.

    Attributes:
        path_base: Base path, usually contains `path_www` and
            `path_templates`.
        path_templates: Path to the templates.
        path_public: Path to the public directory (base for links).
    """

    __slots__: list[str] = ['path_base', 'path_www', 'path_templates',
                            'site_title', 'encoding_default',
                            'language_default',
                            'html_css_default', 'html_javascript_default',
                            'html_error_page']

    def __init__(self,
                 path_base: pathlib.Path = pathlib.Path(
                     __file__).parent.absolute(),
                 path_www: Optional[pathlib.Path] = None,
                 path_templates: Optional[pathlib.Path] = None,
                 site_title: str = 'Plapperkasten',
                 encoding_default: str = 'utf-8',
                 language_default: str = 'de',
                 error_page: Optional[htmltemplate.ErrorPage] = None
                 ) -> None:
        # pylint: disable=too-many-arguments
        """Constructor."""
        self.path_base: pathlib.Path = path_base
        self.path_www: pathlib.Path = path_www or path_base / 'www'
        self.path_templates: pathlib.Path = (path_templates or
                                             path_base / 'templates')

        self.site_title: str = site_title
        self.encoding_default: str = encoding_default
        self.language_default: str = language_default
        self.html_css_default: list[str] = []
        self.html_javascript_default: list[str] = []
        self.html_error_page: htmltemplate.ErrorPage = (error_page or
            htmltemplate.ErrorPage(self))

        #for attr in [a for a in dir(self) if \
        #        not a.startswith('__') and not callable(getattr(self, a))]:
        #    print(f"{attr}: {getattr(self, attr)}")
