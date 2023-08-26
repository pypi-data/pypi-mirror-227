"""Docker handler."""

import json

import tornado

import docker

from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin

from ..._version import __version__


client = docker.from_env()


# pylint: disable=W0223
class ImagesHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for the docker images."""

    @tornado.web.authenticated
    def get(self):
        """Returns the docker images."""
        images = map(lambda image: image.attrs, client.images.list())
        res = json.dumps({
            "success": True,
            "message": "List of Docker images.",
            "images": list(images),
        }, default=str)
        self.finish(res)


# pylint: disable=W0223
class ContainersHandler(ExtensionHandlerMixin, APIHandler):
    """The handler for docker containers."""

    @tornado.web.authenticated
    def get(self):
        """Returns the docker containers."""
        containers = map(lambda container: container.attrs, client.containers.list())
        res = json.dumps({
            "success": True,
            "message": "List of Docker containers.",
            "containers": list(containers),
        }, default=str)
        self.finish(res)
