"""Config handler."""

import json

import tornado

from jupyter_server.base.handlers import APIHandler, JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin, ExtensionHandlerJinjaMixin

from .._version import __version__


class ConfigHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the configurations."""

    @tornado.web.authenticated
    def get(self):
        """Returns the configurations of the server extensions."""
        res = json.dumps({
            "extension": "clouder",
            "version": __version__,
        })
        self.finish(res)
