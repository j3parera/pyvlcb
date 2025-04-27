"""
TODO
"""

from selectors import PollSelector, EVENT_READ
from sys import stdin
from .service import Service, Action


class ConsoleUIService(Service):
    """
    Console (stdin, stdout, stderr) based user interface service.
    """

    def __init__(self):
        self._stdin_selector = PollSelector()
        self._stdin_selector.register(fileobj=stdin, events=EVENT_READ)

    @property
    def service_id(self) -> int:
        return 0

    @property
    def service_version_id(self) -> int:
        return 1

    def begin(self) -> None:
        pass

    def _handle_action(self, action: Action | None) -> None:
        pass

    def _process_input(self) -> None:
        for key, _ in self._stdin_selector.select(timeout=0):
            s = key.fileobj.readline().strip("\n")
            print(s)

    def process(self, action: Action | None) -> None:
        self._handle_action(action)
        self._process_input()
