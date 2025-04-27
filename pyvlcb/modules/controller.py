"""
TODO
"""

from abc import ABC, abstractmethod
from typing import List, Sequence
from os import PathLike
from json import load
from pyvlcb.services.service import Service
from .config import Configuration


class Controller(ABC):
    """
    Abstract Controller class.
    """

    def __init__(
        self, services: Sequence[Service], config_file: str | PathLike
    ) -> None:
        self._services: Sequence[Service] = services
        self._config = Configuration(config_file)
        with open(config_file, "rt", encoding="utf-8") as file:
            settings = load(file)["settings"]
        self._name = settings["MODULE_NAME"]
        self._manufacturer = settings["MANUFACTURER_ID"]
        self._module_id = settings["MODULE_ID"]
        self._version = settings["VERSION"]

    @property
    def name(self) -> str:
        """
        The name of the module.
        """
        return self._name

    @property
    def manufacturer_id(self) -> str:
        """
        The manufacturer id of the module.
        """
        return self._manufacturer

    @property
    def module_id(self) -> str:
        """
        The module id of the module.
        """
        return self._module_id

    @property
    def version(self) -> str:
        """
        The version of the module.
        """
        return self._version

    @property
    def can_id(self) -> int:
        """
        The CANID of the module.
        """
        return self._config.can_id

    @can_id.setter
    def can_id(self, can_id: int) -> None:
        self._config.can_id = can_id

    @property
    def services(self) -> Sequence[Service]:
        """
        The services that the module implements.
        """
        return self._services
