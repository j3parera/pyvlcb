"""
TODO
"""

from typing import Any
from ctypes import c_uint16, LittleEndianStructure, Union
from can import Message
from .service import Service
from ..transports.can import CanTransport
from ..vlcbdefs import SERVICE_ID_CAN

SERVICE_VERSION_ID = 1
DEFAULT_MINOR_PRIORITY = 0b11
DEFAULT_MAJOR_PRIORITY = 0b10


class _CanHeaderIdBits(LittleEndianStructure):
    _fields_ = [
        ("can_id", c_uint16, 7),
        ("minor_priority", c_uint16, 2),
        ("major_priority", c_uint16, 2),
    ]


class CanHeaderId(Union):
    _anonymous_ = ("f",)
    _fields_ = [("f", _CanHeaderIdBits), ("as_word", c_uint16)]


class CanService(Service):
    """
    Handles CAN communication
    """

    def __init__(self, transport: CanTransport, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._transport = transport

    @property
    def service_id(self) -> int:
        return SERVICE_ID_CAN

    @property
    def service_version_id(self) -> int:
        return SERVICE_VERSION_ID

    def begin(self) -> None:
        pass

    def _make_header_id(
        self,
        can_id: int,
        minor_pri: int = DEFAULT_MINOR_PRIORITY,
        major_pri: int = DEFAULT_MAJOR_PRIORITY,
    ) -> int:
        header = CanHeaderId()
        header.f.can_id = can_id
        header.f.minor_priority = minor_pri
        header.f.major_priority = major_pri
        return header.as_word

    def _make_empty_message(self, can_id: int) -> Message:
        msg = Message()
        msg.arbitration_id = self._make_header_id(can_id)
        msg.is_remote_frame = False
        msg.is_extended_id = False
        return msg

    def _check_incoming_message(self) -> None:
        msg = self._transport.recv(0)
        if msg is None:
            return
        if msg.is_extended_id:
            return
        if msg.is_remote_frame:
            self._transport.send(self._make_empty_message(0x1234))
            return
        # controller->indicateActivity();
        # byte remoteCANID = getCANID(canFrame.id);
        # /// set flag if we find a CANID conflict with the frame's producer
        # /// doesn't apply to RTR or zero-length frames, so as not to trigger an enumeration loop
        # if (remoteCANID == controller->getModuleCANID() && canFrame.len > 0)
        # {
        #     // DEBUG_SERIAL << F("> CAN id clash, enumeration required") << endl;
        #     enumeration_required = true;
        # }

        # // are we enumerating CANIDs ?
        # if (bCANenum && canFrame.len == 0)
        # {
        #     // store this response in the responses array
        #     if (remoteCANID > 0)
        #     {
        #     // fix to correctly record the received CANID
        #     bitWrite(enum_responses[(remoteCANID / 8)], remoteCANID % 8, 1);
        #     // DEBUG_SERIAL << F("> stored CANID ") << remoteCANID << F(" at index = ") << (remoteCANID / 8) << F(", bit = ") << (remoteCANID % 8) << endl;
        #     }

        #     return;
        # }

        # // The incoming CAN frame is a VLCB message.
        # Action action = {ACT_MESSAGE_IN, {canFrame.len}};
        # memcpy(action.vlcbMessage.data, canFrame.data, canFrame.len);
        # controller->putAction(action);

    def process(self, action) -> None:
        self._check_incoming_message()
