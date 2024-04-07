""" Prueba."""

from ctypes import c_uint8, LittleEndianStructure, Union
from pyvlcb.vlcbdefs import MANU_DEV


class Flags_bits(LittleEndianStructure):
    _fields_ = [
        ("logout", c_uint8, 1),  # asByte & 1
        ("userswitch", c_uint8, 1),  # asByte & 2
        ("suspend", c_uint8, 1),  # asByte & 4
        ("idle", c_uint8, 1),  # asByte & 8
    ]


class Flags(Union):
    _anonymous_ = ("bit",)
    _fields_ = [("bit", Flags_bits), ("as_byte", c_uint8)]


if __name__ == "__main__":

    print(MANU_DEV)

    flags = Flags()
    flags.as_byte = 0x6  # ->0010

    print(f"logout: {flags.bit.logout}")
    # `bit` is defined as anonymous field, so its fields can also be accessed directly:
    print(f"logout: {flags.logout}")
    print(f"userswitch: {flags.userswitch}")
    print(f"suspend   :  {flags.suspend}")
    print(f"idle  : {flags.idle}")
