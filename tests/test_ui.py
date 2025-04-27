#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name

from pytest import fixture
from pyvlcb.services.serialui import ConsoleUIService


class TestConsoleUI:
    """
    Console UI tests.
    """

    @fixture
    def console_service(self) -> ConsoleUIService:
        """
        Creates the console service under test.
        """
        return ConsoleUIService()

    def test_no_request(self, console_service: ConsoleUIService, monkeypatch) -> None:
        """
        Request action tests.
        """
        monkeypatch.setattr("sys.stdin.readline", lambda: "")
        console_service.process(None)

    def test_request(self, console_service: ConsoleUIService, monkeypatch) -> None:
        """
        Request action tests.
        """
        monkeypatch.setattr("sys.stdin.readline", lambda: "s")
        console_service.process(None)
