"""
TODO
"""

from .service import Service
from ..vlcbdefs import SERVICE_ID_MNS


class MinimumNodeService(Service):
    """
    Handles the OP-codes for managing nodes.
    It is required for use in a VLCB module.
    """

    def __init__(self) -> None:
        pass

    @property
    def service_id(self) -> int:
        return SERVICE_ID_MNS

    @property
    def service_version_id(self) -> int:
        return 1

    def begin(self) -> None:
        pass

    def process(self, _action) -> None:
        pass
