"""Class hierarchy for HTML templates."""
from __future__ import annotations

import pathlib
import string

from plapperkastenserver import config as plkconfig

class HTMLTemplate:
    # pylint: disable=too-many-instance-attributes
    """Base class to derive templates from.

    Attributes:
        title: The page title.
        encoding: The charset.
        language: The language used.
        content_type: The content_type
        css: A list of stylesheets to use.
        javascript: A list of javascript sheets to use.
        template: A template string.
        variables: A dicitionary of variables to insert into the
            template.
        path_templates: Path to the templates.
        path_public: Path to the public directory (base for links).
    """

    def __init__(self, config: plkconfig.Config, **kwargs) -> None:
        """Contructor."""
        self.title: str = config.site_title
        self.encoding: str = config.encoding_default
        self.language: str = config.language_default
        self.css: list[str] = config.html_css_default.copy()
        self.javascript: list[str] = config.html_javascript_default.copy()
        self.template: str = ''
        self.variables: dict[str, str] = kwargs
        self.content_type: str = 'text/html'
        # this can be redefined for each template without changing the
        # "global" value in `server_config`
        self.path_templates: pathlib.Path = config.path_templates

    def compile(self) -> str:
        """Render the template and return it as a string."""
        page: str = self._compile_head()
        page += self._compile_body()
        return f"<!DOCTYPE HTML><html lang=\"{self.language}\">{page}</html>"

    def _compile_head(self) -> str:
        """Compile the head section"""
        head: str = '<head>'
        head += f"<meta charset=\"{self.encoding}\">"
        head += '<meta name="viewport" ' \
                'content="width=device-width, initial-scale=1.0"/>'
        head += f"<title>{self.title}</title>"
        for sheet in self.css:
            head += f"<link rel=\"stylesheet\" href=\"{sheet}\"/>"
        for script in self.javascript:
            head += f"<script src=\"{script}\"></script>"
        head += '</head>'
        return head

    def _compile_body(self) -> str:
        """Compile the body.

        Basically wraps the content in `<body></body>` tags.
        """
        return f"<body>{self._compile_content()}</body>"

    def _compile_content(self) -> str:
        """Compile the content."""
        return string.Template(self.template).safe_substitute(self.variables)

    def _compile_list(self, items: list[str], listtype = 'ul') -> str:
        """Compile a HTML list from a list.

        Args:
            items: A list of items.
        """
        html: str = f"<{listtype}>"
        for item in items:
            html += f"<li>{item}</li>"
        return f"{html}</{listtype}>"

    def set_template_file(self, name: str) -> None:
        """Check if the file exists and read it.

        Args:
            name: The name of the file in `path_templates`.
        """
        file: pathlib.Path = pathlib.Path(self.path_templates / name).resolve()
        self.template = file.read_text(encoding='utf-8')

class ErrorPage(HTMLTemplate):
    """A default error page.
    """

    def __init__(self, config: plkconfig.Config, status: str = '',
                 message: str = '', explanation: str = '') -> None:
        # pylint: disable=too-many-arguments
        """Contructor."""
        super().__init__(config,
                         **{'status': status, 'message': message,
                            'explanation': explanation})
        self.set_template_file('error.html')
