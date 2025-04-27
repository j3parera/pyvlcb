"""
TODO Service
"""

from abc import ABC, abstractmethod


class Action:
    """
    TODO
    """


class Service(ABC):
    """
    Abstract Service class.
    """

    @property
    @abstractmethod
    def service_id(self) -> int:
        """
        Return a unique ID for this service.

        Returns:
            bytes: the unique ID for this service.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def service_version_id(self) -> int:
        """
        Return the version of the implementation of this service.

        Returns:
            bytes: the version of the implementation of this service.
        """
        raise NotImplementedError

    @abstractmethod
    def begin(self) -> None:
        """
        Do any setup required at the beginning.
        """
        raise NotImplementedError

    @abstractmethod
    def process(self, action: Action | None) -> None:
        """
        Process an action.

        Args:
            _action (_type_): action to be performed. Could be None.
        """
        raise NotImplementedError
