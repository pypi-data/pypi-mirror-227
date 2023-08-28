"""Index handler."""

import tornado

from jupyter_server.base.handlers import APIHandler, JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin, ExtensionHandlerJinjaMixin

from .base import BaseTemplateHandler

from .._version import __version__


class IndexHandler(BaseTemplateHandler):
    """The handler for the index."""

    @tornado.web.authenticated
    def get(self):
        """The index page."""
        self.write(self.render_template("index.html"))
