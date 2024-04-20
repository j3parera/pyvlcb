"""
TODO
"""

from typing import Any
from .service import Service
from ..transports.transport import Transport


class CanService(Service):
    """
    Handles CAN communication
    """

    def __init__(self, transport: Transport, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._transport = transport
