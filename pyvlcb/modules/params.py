"""
TODO
"""

from ctypes import LittleEndianStructure, Union, c_uint8
from dataclasses import dataclass
from struct import pack
from ..vlcbdefs import (
    MANU_DEV,
    CPUM_ARM,
    ARMCortex_A72,
    PB_CAN,
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


class ModuleFlagsBits(LittleEndianStructure):
    """Module flags bits."""

    # pylint: disable=R0903
    _fields_ = [
        ("producer", c_uint8, 1),
        ("consumer", c_uint8, 1),
        ("normal", c_uint8, 1),
        ("bootable", c_uint8, 1),
        ("self_consumer", c_uint8, 1),
        ("learn", c_uint8, 1),
        ("vlcb", c_uint8, 1),
    ]


# pylint: disable=too-few-public-methods
class ModuleFlags(Union):
    """Module flags."""

    def __init__(self) -> None:
        super().__init__()
        self.bit.producer = 0
        self.bit.consumer = 0
        self.bit.normal = 0
        self.bit.bootable = 0
        self.bit.self_consumer = 0
        self.bit.learn = 0
        self.bit.vlcb = 1

    # pylint: disable=R0903
    _anonymous_ = ("bit",)
    _fields_ = [("bit", ModuleFlagsBits), ("as_byte", c_uint8)]


# pylint: disable=too-many-instance-attributes
@dataclass(init=False)
class Params:
    """
    Class for holding module flags.
    """

    num_params: int = 20
    manufacturer_id: int = MANU_DEV
    module_id: int = 0
    version_major: int = 0
    version_minor: str = "a"
    version_beta: int = 0
    num_evts: int = 0
    num_evs: int = 0
    num_nvs: int = 0
    flags: ModuleFlags = ModuleFlags()
    load_addr: int = 0
    cpu_id: int = CPUM_ARM
    cpu_code: int = ARMCortex_A72
    cpu_name: str = "P4B "
    protocol: int = PB_CAN

    @property
    def version(self) -> str:
        """
        Module version as string.
        """
        return f"{self.version_major}.{self.version_minor}.{self.version_beta}"

    @version.setter
    def version(self, version: str) -> None:
        parts = version.split(".")
        self.version_major = int(parts[0])
        self.version_minor = parts[1][0]
        self.version_beta = int(parts[2])

    @property
    def is_normal_mode(self) -> bool:
        """
        Test if module is in normal mode.
        """
        return bool(self.flags.bit.normal)

    @is_normal_mode.setter
    def is_normal_mode(self, on: bool) -> None:
        self.flags.bit.normal = bool(on)

    @property
    def is_learn_mode(self) -> bool:
        """
        Test if module is in learning mode.
        """
        return bool(self.flags.bit.learn)

    @is_learn_mode.setter
    def is_learn_mode(self, on: bool) -> None:
        self.flags.bit.learn = bool(on)

    # pylint: disable=too-many-branches, too-many-return-statements
    def get_param(self, idx: int) -> int | str | ModuleFlags:
        """
        Get a parameter by index.

        Args:
            idx (int): parameter index

        Raises:
            IndexError: index is out of bounds

        Returns:
            int | str | ModuleFlags: parameter value
        """
        if idx == PAR_NUM:
            return self.num_params
        if idx == PAR_MANU:
            return self.manufacturer_id
        if idx == PAR_MTYP:
            return self.module_id
        if idx == PAR_MAJVER:
            return self.version_major
        if idx == PAR_MINVER:
            return self.version_minor
        if idx == PAR_BETA:
            return self.version_beta
        if idx == PAR_EVTNUM:
            return self.num_evts
        if idx == PAR_EVNUM:
            return self.num_evs
        if idx == PAR_NVNUM:
            return self.num_nvs
        if idx == PAR_FLAGS:
            return self.flags
        if idx == PAR_BUSTYPE:
            return self.protocol
        if idx == PAR_CPUID:
            return self.cpu_id
        if idx == PAR_CPUMID:
            return self.cpu_name
        if idx == PAR_CPUMAN:
            return self.cpu_code
        if idx == PAR_LOAD:
            return self.load_addr
        raise IndexError

    def to_bytes(self) -> bytes:
        """
        Binary version for messaging.

        Returns:
            bytes: the params object as binary.
        """
        return pack(
            ">11bl4s2b",
            self.num_params,
            self.manufacturer_id,
            ord(self.version_minor),
            self.module_id,
            self.num_evts,
            self.num_evs,
            self.num_nvs,
            self.version_major,
            self.flags.as_byte,
            self.cpu_id,
            self.protocol,
            self.load_addr,
            f"{self.cpu_name:<4}".encode("ascii"),
            self.cpu_code,
            self.version_beta,
        )
