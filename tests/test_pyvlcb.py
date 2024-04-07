#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name


from json import dump, load

from pyvlcb import pyvlcb as vlcb


class TestConfiguration:
    """
    Configuration tests
    """

    filename = "pyvlcb/config.json"

    def test_init(self):
        """
        Constructor test
        """
        config = vlcb.Configuration(self.filename)
        assert config is not None

    def test_factory(self):
        """
        Begin test
        """
        filename = "pyvlcb/config_factory.json"
        with open(filename, "rt", encoding="utf-8") as f:
            data = load(f)
        data["settings"]["MODE"] = 0xFF
        data["settings"]["NODE_NUMBER"] = 0xFFFF
        with open(filename, "wt", encoding="utf-8") as f:
            dump(data, f)
        config = vlcb.Configuration(filename)
        config.begin()
        assert config.current_mode == vlcb.Modes.MODE_UNINITIALISED
        assert config.node_number == 0
