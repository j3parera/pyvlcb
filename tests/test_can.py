#!/usr/bin/env python
"""Tests for `pyvlcb` package."""
# pylint: disable=redefined-outer-name


import time
from can import Message
from pyvlcb.transports.can import CanTransportOverVirtual
from pyvlcb.services.can import CanService


class TestCan:
    """
    CAN tests
    """

    def test_can_transport(self) -> None:
        """
        Constructor test
        """
        transport = CanTransportOverVirtual()
        assert transport is not None
        msg_out = Message(arbitration_id=0x1234, data=list(range(8)))
        transport.send(msg_out)
        transport.send(msg_out)
        transport.send(msg_out)
        assert transport.tx_count == 3
        time.sleep(0.01)
        assert transport.rx_count == 3
        msg_in = transport.recv(None)
        assert msg_in is not None
        assert msg_in.arbitration_id == msg_out.arbitration_id
        assert msg_in.data == msg_out.data

    # pylint: disable=protected-access
    def test_can_service(self) -> None:
        """
        CAN Service test
        """
        transport = CanTransportOverVirtual()
        can_service = CanService(transport)
        assert can_service is not None
        header = can_service._make_header_id(0x12, 0b01, 0b10)
        assert header == (0b10 << 9) | (0b01 << 7) | 0x12
        empty_header = can_service._make_header_id(0x12)
        msg = can_service._make_empty_message(0x12)
        assert msg.arbitration_id == empty_header
        assert msg.is_extended_id is False
        assert msg.is_error_frame is False
        assert msg.is_remote_frame is False
        assert msg.data == bytearray()
