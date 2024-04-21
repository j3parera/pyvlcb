"""
Main module.
"""

from abc import ABC
from ctypes import LittleEndianStructure, Union, c_uint8
from dataclasses import dataclass
from enum import Enum
from json import dump, load
from os import PathLike
from typing import Any, List


class Mode(Enum):
    """
    Module modes.
    """

    # Exclusive modes
    UNINITIALISED = 0xFF  # Uninitialised / factory settings
    SETUP = 0  # Set up mode
    NORMAL = 1  # Normal operation mode
    # Event Teaching Service modes
    LEARN_ON = 0x08  # Turn on learn mode
    LEARN_OFF = 0x09  # Turn off learn mode
    # Event Acknowledgment Service modes
    EVENT_ACK_ON = 0x0A  # Turn on event acknowledgements
    EVENT_ACK_OFF = 0x0B  # Turn off event acknowledgements
    # Minimum Node Service modes
    HEARTBEAT_ON = 0x0C  # Turn on heartbeat
    HEARTBEAT_OFF = 0x0D  # Turn off heartbeat
    # Boot modes
    BOOT = 0x0E  # PIC Boot loader mode


class NodeFlagsBits(LittleEndianStructure):
    """Node flags bits."""

    # pylint: disable=R0903
    _fields_ = [("heartbeat", c_uint8, 1), ("event_ack", c_uint8, 1)]


class NodeFlags(Union):
    """Node flags."""

    # pylint: disable=R0903
    _anonymous_ = ("bit",)
    _fields_ = [("bit", NodeFlagsBits), ("as_byte", c_uint8)]


@dataclass
class Event:
    """VLCB event."""

    node_number: int
    event_number: int
    event_vars: List[int]


class Configuration(ABC):
    """
    Abstract Configuration class.
    """

    def __init__(self, filename: str | PathLike) -> None:
        self._nonvolatile_filename: str | PathLike = filename
        self._nonvolatile_mem: dict[str, dict[str, Any]] = self._load_nonvolatile_mem()
        if self.mode == Mode.UNINITIALISED and self.node_number == 0xFFFF:
            # factory virgin state
            self.clear_all_node_vars()
            self.clear_all_events()
            self.set_mode(Mode.UNINITIALISED)
            self.can_id = 0
            # pylint: disable=W0201
            self.node_flags.as_byte = 0

    def _load_nonvolatile_mem(self) -> dict[str, dict[str, Any]]:
        with open(self._nonvolatile_filename, "rt", encoding="utf-8") as file:
            return load(file)

    def _save_nonvolatile_mem(self) -> None:
        with open(self._nonvolatile_filename, "wt", encoding="utf-8") as file:
            dump(self._nonvolatile_mem, file, indent=4)

    @property
    def mode(self) -> Mode:
        """Current operating mode."""
        return Mode(self._nonvolatile_mem["settings"]["MODE"])

    def set_mode(self, mode: Mode, node_number: int = 0) -> None:
        """Set module mode."""
        self._nonvolatile_mem["settings"]["MODE"] = mode.value
        if mode == Mode.UNINITIALISED:
            self.node_number = 0
        elif mode == Mode.NORMAL:
            self.node_number = node_number
        self._save_nonvolatile_mem()

    @property
    def can_id(self) -> int:
        """CAN identifier."""
        return self._nonvolatile_mem["settings"]["CAN_ID"]

    @can_id.setter
    def can_id(self, can_id: int):
        self._nonvolatile_mem["settings"]["CAN_ID"] = can_id
        self._save_nonvolatile_mem()

    @property
    def node_number(self) -> int:
        """Node number."""
        return self._nonvolatile_mem["settings"]["NODE_NUMBER"]

    @node_number.setter
    def node_number(self, node_number: int):
        self._nonvolatile_mem["settings"]["NODE_NUMBER"] = node_number
        self._save_nonvolatile_mem()

    @property
    def node_flags(self) -> NodeFlags:
        """Node flags."""
        flags = NodeFlags()
        # pylint: disable=W0201
        flags.as_byte = self._nonvolatile_mem["settings"]["NODE_FLAGS"]
        return flags

    @node_flags.setter
    def node_flags(self, flags: NodeFlags):
        self._nonvolatile_mem["settings"]["NODE_FLAGS"] = flags.value
        self._save_nonvolatile_mem()

    @property
    def heartbeat(self) -> bool:
        """Heartbeat."""
        return bool(self.node_flags.heartbeat)

    @heartbeat.setter
    def heartbeat(self, on: bool) -> None:
        # pylint: disable=C0103
        """Heartbeat."""
        self.node_flags.heartbeat = int(on)

    @property
    def event_ack(self) -> bool:
        """Event acknolwdege."""
        return bool(self.node_flags.event_ack)

    @event_ack.setter
    def event_ack(self, on: bool) -> None:
        # pylint: disable=C0103
        self.node_flags.heartbeat = int(on)

    def _event_key(self, idx: int) -> str:
        # pylint: disable=R0201
        return f"EVT{idx:03d}"

    @property
    def num_events(self) -> int:
        """Number of events."""
        return len(self._nonvolatile_mem["events"])

    def read_event(self, idx: int) -> Event | None:
        """Read a stored event."""
        try:
            evt_key = self._event_key(idx)
            data = self._nonvolatile_mem["events"][evt_key]
            evt = Event(data["NODE_NUMBER"], data["EVENT_NUMBER"], data["EVENT_VARS"])
            return evt
        except KeyError:
            return None

    def write_event(self, idx, event: Event) -> None:
        """Write an event."""
        evt_key = self._event_key(idx)
        if evt_key not in self._nonvolatile_mem["events"]:
            self._nonvolatile_mem["events"][evt_key] = {}
        self._nonvolatile_mem["events"][evt_key]["NODE_NUMBER"] = event.node_number
        self._nonvolatile_mem["events"][evt_key]["EVENT_NUMBER"] = event.event_number
        self._nonvolatile_mem["events"][evt_key]["EVENT_VARS"] = event.event_vars
        self._save_nonvolatile_mem()

    def clear_event(self, idx: int) -> None:
        """Clear an event."""
        evt_key = self._event_key(idx)
        try:
            del self._nonvolatile_mem["events"][evt_key]
            self._save_nonvolatile_mem()
        except KeyError:
            pass

    def find_event(self, node_number: int, event_number: int) -> Event | None:
        """Locate an event by contents."""
        for evt in self._nonvolatile_mem["events"].values():
            if (
                evt["NODE_NUMBER"] == node_number
                and evt["EVENT_NUMBER"] == event_number
            ):
                return Event(evt["NODE_NUMBER"], evt["EVENT_NUMBER"], evt["EVENT_VARS"])
        return None

    def clear_all_events(self):
        """Clear all event data."""
        self._nonvolatile_mem["events"] = {}
        self._save_nonvolatile_mem()

    def _node_var_key(self, idx: int) -> str:
        # pylint: disable=R0201
        return f"NV{idx:03d}"

    @property
    def num_node_vars(self) -> int:
        """Number of node_vars."""
        return len(self._nonvolatile_mem["node_vars"])

    def read_node_var(self, idx: int) -> int | None:
        """Read a stored node variable."""
        try:
            nv_key = self._node_var_key(idx)
            data = self._nonvolatile_mem["node_vars"][nv_key]
            return int(data)
        except KeyError:
            return None

    def write_node_var(self, idx: int, val: int) -> None:
        """Write a node variable."""
        nv_key = self._node_var_key(idx)
        self._nonvolatile_mem["node_vars"][nv_key] = val
        self._save_nonvolatile_mem()

    def clear_node_var(self, idx: int) -> None:
        """Clear a node variable."""
        nv_key = self._node_var_key(idx)
        try:
            del self._nonvolatile_mem["node_vars"][nv_key]
            self._save_nonvolatile_mem()
        except KeyError:
            pass

    def clear_all_node_vars(self):
        """Clear all node vars data."""
        self._nonvolatile_mem["node_vars"] = {}
        self._save_nonvolatile_mem()
