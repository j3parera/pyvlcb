#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name


from pyvlcb.modules.controller import Controller
from pyvlcb.modules.params import Params, ModuleFlags
from pyvlcb.services.mns import MinimumNodeService
from pyvlcb.vlcbdefs import (
    MANU_DEV,
    CPUM_ARM,
    ARMCortex_A72,
    PB_CAN,
    PF_VLCB,
    PAR_NUM,
    PAR_MANU,
    PAR_MTYP,
    PAR_MAJVER,
    PAR_MINVER,
    PAR_BETA,
    PAR_EVTNUM,
    PAR_EVNUM,
    PAR_NVNUM,
    PAR_FLAGS,
    PAR_BUSTYPE,
    PAR_CPUID,
    PAR_CPUMAN,
    PAR_CPUMID,
    PAR_LOAD,
)


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


class TestParams:
    """
    Module's parameter set test.
    """

    def test_properties(self) -> None:
        """
        Properties test.
        """
        p = Params()
        assert p.num_params == 20
        assert p.get_param(PAR_NUM) == 20
        assert p.manufacturer_id == MANU_DEV
        assert p.get_param(PAR_MANU) == MANU_DEV
        assert p.module_id == 0
        assert p.get_param(PAR_MTYP) == 0
        assert p.version == "0.a.0"
        assert p.get_param(PAR_MAJVER) == 0
        assert p.get_param(PAR_MINVER) == "a"
        assert p.get_param(PAR_BETA) == 0
        assert p.num_evts == 0
        assert p.get_param(PAR_EVTNUM) == 0
        assert p.num_evs == 0
        assert p.get_param(PAR_EVNUM) == 0
        assert p.num_nvs == 0
        assert p.get_param(PAR_NVNUM) == 0
        assert p.flags.as_byte == PF_VLCB
        flags = p.get_param(PAR_FLAGS)
        assert isinstance(flags, ModuleFlags)
        assert flags.as_byte == PF_VLCB
        assert p.protocol == PB_CAN
        assert p.get_param(PAR_BUSTYPE) == PB_CAN
        assert p.cpu_id == CPUM_ARM
        assert p.get_param(PAR_CPUID) == CPUM_ARM
        assert p.cpu_code == ARMCortex_A72
        assert p.get_param(PAR_CPUMAN) == ARMCortex_A72
        assert p.cpu_name == "P4B "
        assert p.get_param(PAR_CPUMID) == "P4B "
        assert p.load_addr == 0
        assert p.get_param(PAR_LOAD) == 0
        assert p.to_bytes() == bytes(
            b"\x14\x0da\x00\x00\x00\x00\x00\x40\x03\x01\x00\x00\x00\x00P4B \x04\00"
        )
        assert p.num_params == len(p.to_bytes()) - 1
        p.num_evts = 10
        p.module_id = 1
        assert p.to_bytes() == bytes(
            b"\x14\x0da\x01\x0a\x00\x00\x00\x40\x03\x01\x00\x00\x00\x00P4B \x04\00"
        )
        p.version = "1.b.3"
        assert p.version_major == 1
        assert p.version_minor == "b"
        assert p.version_beta == 3
        assert not p.is_normal_mode
        p.is_normal_mode = True
        assert p.is_normal_mode
        assert not p.is_learn_mode
        p.is_learn_mode = True
        assert p.is_learn_mode
