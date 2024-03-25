import os

from fastapi import FastAPI
from importlib import import_module

from .exceptions import MissingSetupFunction

class App(FastAPI):

    def __init__(self, title: str) -> None:
        super().__init__(title=title, redoc_url=None, root_path="/api/v1")
        self.add_event_handler("startup", self._startup)

    async def _startup(self) -> None:
        for root, _, files in os.walk("endpoints"):
            for file in files:
                if file.endswith(".py"):
                    self.addEndpoint(os.path.join(root, file).replace("\\", ".").replace("/", ".")[:-3])

    def addEndpoint(self, path: str) -> None:
        module = import_module(path)
        setup = getattr(module, "setup", None)
        if not setup:
            raise MissingSetupFunction
        endpoint = setup()
        self.add_api_route(endpoint.path, endpoint.callback, response_class=endpoint.responseClass, methods=[endpoint.method.name], name=endpoint.__class__.__qualname__)