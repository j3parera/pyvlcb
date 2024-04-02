"""
Main module.
"""

from abc import ABC, abstractmethod


class Service(ABC):
    """
    Abstract Service class.
    """

    def set_controller(self, _controller) -> None:
        """
        Set a reference to the controller object in the implementing class.

        Args:
            _controller (_type_): controlleer object.
        """

    def begin(self) -> None:
        """
        Do any setup required at the beginning.
        """

    @abstractmethod
    def get_service_id(self) -> bytes:
        """
        Return a unique ID for this service.

        Returns:
            bytes: the unique ID for this service.
        """
        return b"0"

    @abstractmethod
    def get_service_version_id(self) -> bytes:
        """
        Return the version of the implementation of this service.

        Returns:
            bytes: the version of the implementation of this service.
        """
        return b"0"

    @abstractmethod
    def process(self, _action) -> None:
        """
        Process an action.

        Args:
            _action (_type_): action to be performed. Could be None.
        """


class MinimumNodeService(Service):
    """
    Handles the OP-codes for managing nodes.
    It is required for use in a VLCB module.
    """
