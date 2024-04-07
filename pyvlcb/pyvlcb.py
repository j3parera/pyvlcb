"""
Main module.
"""

from abc import ABC, abstractmethod
from ctypes import LittleEndianStructure, Union, c_uint8
from enum import Enum
from json import dump, load
from os import PathLike
from typing import Any


class Modes(Enum):
    """
    Modes.
    """

    # Exclusive modes
    MODE_UNINITIALISED = 0xFF  # Uninitialised / factory settings
    MODE_SETUP = 0  # Set up mode
    MODE_NORMAL = 1  # Normal operation mode
    # Event Teaching Service modes
    MODE_LEARN_ON = 0x08  # Turn on learn mode
    MODE_LEARN_OFF = 0x09  # Turn off learn mode
    # Event Acknowledgment Service modes
    MODE_EVENT_ACK_ON = 0x0A  # Turn on event acknowledgements
    MODE_EVENT_ACK_OFF = 0x0B  # Turn off event acknowledgements
    # Minimum Node Service modes
    MODE_HEARTBEAT_ON = 0x0C  # Turn on heartbeat
    MODE_HEARTBEAT_OFF = 0x0D  # Turn off heartbeat
    # Boot modes
    MODE_BOOT = 0x0E  # PIC Boot loader mode


class NodeFlagsBits(LittleEndianStructure):
    """Node flags bits."""

    _fields_ = [("heartbeat", c_uint8, 1), ("event_ack", c_uint8, 1)]


class NodeFlags(Union):
    """Node flags."""

    _anonymous_ = ("bit",)
    _fields_ = [("bit", NodeFlagsBits), ("as_byte", c_uint8)]


class Configuration(ABC):
    """
    Abstract Configuration class.
    """

    def __init__(self, filename: str | PathLike) -> None:
        self._nv_filename: str | PathLike = filename
        self._nv_mem: dict[str, dict[str, Any]]
        # self.node_flags: NodeFlags

    def _load_nvmem(self) -> dict[str, dict[str, Any]]:
        with open(self._nv_filename, "rt", encoding="utf-8") as file:
            return load(file)

    def _save_nvmem(self) -> None:
        with open(self._nv_filename, "wt", encoding="utf-8") as file:
            dump(self._nv_mem, file, indent=4)

    @property
    def current_mode(self) -> Modes:
        """Current operating mode."""
        return Modes(self._nv_mem["settings"]["MODE"])

    @current_mode.setter
    def current_mode(self, mode: Modes) -> None:
        self._nv_mem["settings"]["MODE"] = mode.value
        self._save_nvmem()

    @property
    def can_id(self) -> int:
        """CAN identifier."""
        return self._nv_mem["settings"]["CAN_ID"]

    @can_id.setter
    def can_id(self, can_id: int):
        self._nv_mem["settings"]["CAN_ID"] = can_id
        self._save_nvmem()

    @property
    def node_number(self) -> int:
        """Node number."""
        return self._nv_mem["settings"]["NODE_NUMBER"]

    @node_number.setter
    def node_number(self, node_number: int):
        self._nv_mem["settings"]["NODE_NUMBER"] = node_number
        self._save_nvmem()

    @property
    def node_flags(self) -> NodeFlags:
        """Node flags."""
        flags = NodeFlags()
        # pylint: disable=W0201
        flags.as_byte = self._nv_mem["settings"]["NODE_FLAGS"]
        return flags

    @node_flags.setter
    def node_flags(self, flags: NodeFlags):
        self._nv_mem["settings"]["NODE_FLAGS"] = flags.value
        self._save_nvmem()

    @property
    def is_heartbeat(self) -> bool:
        """Is heartbeat active."""
        return bool(self.node_flags.heartbeat)

    @property
    def is_event_ack(self) -> bool:
        """Is event ackkonwledge active."""
        return bool(self.node_flags.event_ack)

    def clear_events(self):
        """Clear all event data."""
        self._nv_mem["events"] = {}
        self._save_nvmem()

    def clear_node_vars(self):
        """Clear all node vars data."""
        self._nv_mem["node_vars"] = {}
        self._save_nvmem()

    def begin(self) -> None:
        """
        Do any setup required at the beginning.
        """
        self._nv_mem = self._load_nvmem()
        if self.current_mode == Modes.MODE_UNINITIALISED and self.node_number == 0xFFFF:
            # factory virgin state
            self.clear_node_vars()
            self.clear_events()
            self.current_mode = Modes.MODE_UNINITIALISED
            self.can_id = 0
            self.node_number = 0
            # pylint: disable=W0201
            self.node_flags.as_byte = 0


#  class Configuration
#  {
# public:

#   void begin();

#   byte findExistingEvent(unsigned int nn, unsigned int en);
#   byte findEventSpace();
#   byte findExistingEventByEv(byte evnum, byte evval);

#   void printEvHashTable(bool raw);
#   byte getEvTableEntry(byte tindex);
#   byte numEvents();
#   void updateEvHashEntry(byte idx);
#   void clearEvHashTable();
#   byte getEventEVval(byte idx, byte evnum);
#   void writeEventEV(byte idx, byte evnum, byte evval);

#   byte readNV(byte idx);
#   void writeNV(byte idx, byte val);

#   void readEvent(byte idx, byte tarr[EE_HASH_BYTES]);
#   void writeEvent(byte index, const byte data[EE_HASH_BYTES]);
#   void cleareventEEPROM(byte index);
#   void resetModule();

#   void setCANID(byte canid);
#   void setModuleUninitializedMode();
#   void setModuleNormalMode(unsigned int nodeNumber);
#   void setHeartbeat(bool beat);
#   void setNodeNum(unsigned int nn);
#   void setEventAck(bool ea);

#   void setResetFlag();
#   void clearResetFlag();
#   bool isResetFlagSet();

#   unsigned int EE_EVENTS_START;
#   byte EE_MAX_EVENTS;
#   byte EE_NUM_EVS;
#   byte EE_BYTES_PER_EVENT;
#   unsigned int EE_NVS_START;
#   byte EE_NUM_NVS;
#   byte EE_PRODUCED_EVENTS;

#   bool heartbeat;
#   bool eventAck;
#   byte CANID;
#   VlcbModeParams currentMode;
#   unsigned int nodeNum;

#   // These functions shouldn't be here. But keep them for now.
#   unsigned int freeSRAM();
#   void reboot();

#   static void setTwoBytes(byte *target, unsigned int value);
#   static unsigned int getTwoBytes(const byte *bytes);
#   static bool nnenEquals(const byte lhs[EE_HASH_BYTES], const byte rhs[EE_HASH_BYTES]);

# private:
#   Storage * storage;

#   void setModuleMode(VlcbModeParams m);
#   byte makeHash(byte tarr[EE_HASH_BYTES]);
#   void getEvArray(byte idx);
#   void makeEvHashTable();

#   void loadNVs();

#   unsigned int getEVAddress(byte idx, byte evnum);

#   byte *evhashtbl;
# };


class Service(ABC):
    """
    Abstract Service class.
    """

    def set_controller(self, _controller) -> None:
        """
        Set a reference to the controller object in the implementing class.

        Args:
            _controller (_type_): controlleer object.
        """

    def begin(self) -> None:
        """
        Do any setup required at the beginning.
        """

    @abstractmethod
    def get_service_id(self) -> bytes:
        """
        Return a unique ID for this service.

        Returns:
            bytes: the unique ID for this service.
        """
        raise NotImplementedError

    @abstractmethod
    def get_service_version_id(self) -> bytes:
        """
        Return the version of the implementation of this service.

        Returns:
            bytes: the version of the implementation of this service.
        """
        raise NotImplementedError

    @abstractmethod
    def process(self, _action) -> None:
        """
        Process an action.

        Args:
            _action (_type_): action to be performed. Could be None.
        """
        raise NotImplementedError


class MinimumNodeService(Service):
    """
    Handles the OP-codes for managing nodes.
    It is required for use in a VLCB module.
    """
