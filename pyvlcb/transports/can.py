"""
CAN Transport based on python-can package.
"""

from typing import Any, Optional
from can import (
    Bus,
    Notifier,
    SizedRotatingLogger,
    BufferedReader,
    Message,
    Listener,
    BusABC,
)
from can.exceptions import CanOperationError
from can.interfaces.serial.serial_can import SerialBus
from .transport import Transport

BITRATE = 125000


class CanTransport(Transport):
    """
    CAN Transport.
    """

    class CanRxCounter(Listener):
        """
        RX counter
        """

        def __init__(self, transport: Transport) -> None:
            super().__init__()
            self._transport = transport

        def on_error(self, exc: Exception) -> None:
            self._transport._rx_error_count += 1

        def on_message_received(self, msg: Message) -> None:
            self._transport._rx_count += 1

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._bus: BusABC
        self._logger = SizedRotatingLogger(
            base_filename="canlog.txt", max_bytes=10 * 1024**2, append="True"
        )
        self._buf_reader = BufferedReader()
        self._rx_counter = self.CanRxCounter(self)
        self._notifier = Notifier(
            bus=self._bus, listeners=[self._logger, self._buf_reader, self._rx_counter]
        )

    def reset(self) -> None:
        """
        Resets CAN transport.
        """
        # remove tx messages
        self._bus.flush_tx_buffer()
        # remove rx messages
        while True:
            if self._buf_reader.get_message(0) is None:
                break
        # issue a bus reset (if exists)
        reset = getattr(self._bus, "reset")
        if reset and callable(reset):
            reset()

    def status(self) -> int:
        return self._bus.state.value

    def available(self) -> bool:
        """
        Check if there is at least one message in the RX queue.
        """
        return not self._buf_reader.buffer.empty()

    def recv(self, timeout: Optional[float] = 0.0) -> Optional[Message]:
        """
        Return the first message in the RX queue.
        """
        return self._buf_reader.get_message(timeout)  # type: ignore

    def send(self, msg: Message, timeout: int = 0) -> bool:
        """
        Sends a message.
        """
        try:
            self._bus.send(msg, timeout)
            self._tx_count += 1
            return True
        except CanOperationError:
            self._tx_error_count += 1
            return False


class CanTransportOverSerial(CanTransport):
    """
    Can transport using serial device (including serial to USB) a per MERG CANUSB4.
    """

    def __init__(self, device: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._bus = SerialBus(device, bitrate=BITRATE)


class CanTransportOverSocketcan(CanTransport):
    """
    Can transport using socketcan.
    """

    def __init__(self, channel: str, **kwargs: Any) -> None:
        self._bus: BusABC = Bus(
            interface="socketcan",
            channel=channel,
            bitrate=BITRATE,
        )
        super().__init__(**kwargs)


class CanTransportOverVirtual(CanTransport):
    """
    Can transport using socketcan.
    """

    def __init__(self, **kwargs: Any) -> None:
        self._bus: BusABC = Bus(
            "test", interface="virtual", bitrate=BITRATE, receive_own_messages=True
        )
        super().__init__(**kwargs)
