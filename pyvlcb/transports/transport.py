"""
TODO
"""

from abc import ABC, abstractmethod


class Transport(ABC):
    """
    Abstract Transport class.
    """

    def __init__(self) -> None:
        super().__init__()
        self._rx_count: int = 0
        self._tx_count: int = 0
        self._rx_error_count: int = 0
        self._tx_error_count: int = 0

    @abstractmethod
    def reset(self) -> None:
        """
        Resets transport.
        """
        raise NotImplementedError

    @property
    def rx_count(self) -> int:
        """
        Number of received messages.
        """
        return self._rx_count

    @property
    def tx_count(self) -> int:
        """
        Number of transmitted messages.
        """
        return self._tx_count

    @property
    def rx_error_count(self) -> int:
        """
        Number of receive errors.
        """
        return self._rx_error_count

    @property
    def tx_error_count(self) -> int:
        """
        Number of transmit errors.
        """
        return self._tx_error_count

    @abstractmethod
    def status(self) -> int:
        """
        Current status
        """
        raise NotImplementedError
