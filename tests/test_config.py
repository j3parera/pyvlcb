#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name


from json import dump, load

from pyvlcb.modules.config import Configuration, Mode, Event


class TestConfiguration:
    """
    Configuration tests
    """

    filename = "pyvlcb/config.json"

    def test_init(self):
        """
        Constructor test
        """
        config = Configuration(self.filename)
        assert config is not None

    def test_factory(self):
        """
        Factory settings test
        """
        # pylint: disable=R0201
        filename = "pyvlcb/config_factory.json"
        with open(filename, "rt", encoding="utf-8") as file:
            data = load(file)
        data["settings"]["MODE"] = 0xFF
        data["settings"]["NODE_NUMBER"] = 0xFFFF
        with open(filename, "wt", encoding="utf-8") as file:
            dump(data, file)
        config = Configuration(filename)
        assert config.mode == Mode.UNINITIALISED
        assert config.node_number == 0
        assert config.heartbeat is False

    def test_modes(self):
        """
        Module modes test.
        """
        # pylint: disable=R0201
        filename = "pyvlcb/config_factory.json"
        config = Configuration(filename)
        config.node_number = 123
        config.set_mode(Mode.UNINITIALISED)
        assert config.mode == Mode.UNINITIALISED
        assert config.node_number == 0
        config.set_mode(Mode.NORMAL, node_number=120)
        assert config.mode == Mode.NORMAL
        assert config.node_number == 120

    def test_events(self):
        """
        Event configuration handling test.
        """
        # pylint: disable=R0201
        filename = "pyvlcb/config_factory.json"
        config = Configuration(filename)
        assert config.num_events == 0
        assert config.find_event(12, 34) is None
        config.write_event(0, Event(100, 200, [10, 20, 30]))
        assert config.num_events == 1
        evt = config.read_event(0)
        assert evt.node_number == 100
        assert evt.event_number == 200
        assert evt.event_vars == [10, 20, 30]
        assert config.num_events == 1
        config.write_event(2, Event(102, 202, [12, 22, 32]))
        assert config.num_events == 2
        config.write_event(1, Event(101, 201, [11, 21]))
        assert config.num_events == 3
        evt = config.find_event(102, 202)
        assert evt is not None
        assert evt.node_number == 102
        assert evt.event_number == 202
        config.clear_event(2)
        assert config.num_events == 2
        assert config.find_event(102, 202) is None
        config.clear_all_events()
        assert config.num_events == 0
        assert config.read_event(3) is None
        assert config.clear_event(3) is None

    def test_node_vars(self):
        """
        Node variables configuration handling test.
        """
        # pylint: disable=R0201
        filename = "pyvlcb/config_factory.json"
        config = Configuration(filename)
        assert config.num_node_vars == 0
        config.write_node_var(0, 100)
        assert config.num_node_vars == 1
        assert config.read_node_var(0) == 100
        assert config.num_node_vars == 1
        config.write_node_var(2, 102)
        assert config.num_node_vars == 2
        config.write_node_var(1, 101)
        assert config.num_node_vars == 3
        config.clear_node_var(2)
        assert config.num_node_vars == 2
        config.clear_all_node_vars()
        assert config.num_node_vars == 0
        assert config.read_node_var(3) is None
        assert config.clear_node_var(3) is None


# class TestMinimumNodeService:
#     """
#     Minimum node service tests.
#     """

#     def test_unitialized(self):
#         pass

# testUninitializedRequestNodeNumber();
# testUninitializedRequestNodeNumberMissingSNN();
# testNormalRequestNodeNumber();
# testNormalRequestNodeNumberMissingSNN();
# testReleaseNodeNumberByUI();
# testRequestNodeNumberElsewhere();
# testSetNodeNumber();
# testSetNodeNumberNormal();
# testSetNodeNumberShort();
# testQueryNodeNumber();
# testReadNodeParametersNormalMode();
# testReadNodeParametersSetupMode();
# testReadNodeParameterCount();
# testReadNodeParameterModuleId();
# testReadNodeParameterInvalidIndex();
# testReadNodeParameterShortMessage();
# testModuleNameSetup();
# testModuleNameLearn();
# testModuleNameNormal();
# testHeartBeat();
# testServiceDiscovery();
# testServiceDiscoveryLongMessageSvc();
# testServiceDiscoveryIndexOutOfBand();
# testServiceDiscoveryIndexForUI();
# testServiceDiscoveryShortMessage();
# testModeUninitializedToSetup();
# testModeSetupToNormal();
# testModeSetupToUnininitialized();
# testModeNormalToSetup();
# testModeUninitializedToOtherThanSetup();
# testModeSetupToOtherThanNormal();
# testModeNormalToNormal();
# testModeShortMessage();
