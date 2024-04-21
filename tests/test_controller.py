#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name


from pyvlcb.modules.controller import Controller
from pyvlcb.services.mns import MinimumNodeService


class TestConfiguration:
    """
    Configuration tests
    """

    filename = "pyvlcb/config.json"

    def test_init(self) -> None:
        """
        Constructor test
        """
        controller = Controller([MinimumNodeService()], self.filename)
        assert controller is not None

    def test_properties(self) -> None:
        """
        Properties test
        """
        services = [MinimumNodeService()]
        controller = Controller(services, self.filename)
        assert controller.name == ""
        assert controller.manufacturer_id == 0
        assert controller.module_id == 0
        assert controller.version == "0.0.0"
        assert controller.can_id == 0
        controller.can_id = 27
        assert controller.can_id == 27
        controller.can_id = 0
        assert controller.services == services
