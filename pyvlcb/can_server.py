"""
can_server bla bla

"""

import time
from threading import Thread
import random
from typing import Any
from can import (
    Bus,
    Notifier,
    SizedRotatingLogger,
    BufferedReader,
    Message,
    detect_available_configs,
)
from can.exceptions import CanOperationError
from can.interfaces.serial.serial_can import SerialBus
from zmq import Context, PUB, Poller, POLLIN


class Can2Vlcb(Thread):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._running = False
        self._can_bus = Bus(
            interface="socketcan", channel="vcan0", receive_own_messages=True
        )
        self._can_logger = SizedRotatingLogger(
            base_filename="vcan0.txt", max_bytes=10 * 1024**2, append="False"
        )
        # self._can_buf_reader = BufferedReader()
        # self._can_notifier = Notifier(
        #     bus=self._can_bus, listeners=[can_logger, self._can_buf_reader]
        # )
        self._can_fileno = self._can_bus.fileno()
        self._zmq_context = Context.instance()
        self._zmq_pub = self._zmq_context.socket(PUB)
        # TODO self._zmq_pub.bind("tcp://*:8100")
        self._zmq_poller = Poller()
        self._zmq_poller.register(self._can_fileno)

    def terminate(self):
        self._running = False
        # self._can_notifier.stop()
        self._can_bus.shutdown()

    def run(self):
        self._running = True
        self._can_bus.send(
            Message(arbitration_id=random.randint(1, 10000), is_extended_id=True)
        )
        while self._running:
            try:
                socks = dict(self._zmq_poller.poll())
            except CanOperationError:
                pass
            except KeyboardInterrupt:
                self.terminate()
                break
            if self._can_fileno in socks:
                msg = self._can_bus.recv()
                self._can_logger(msg)
                msg.arbitration_id = random.randint(0, 0x7FF)
                self._zmq_pub.send_pyobj(msg)
                # self._can_bus.send(msg)
                time.sleep(0.1)


class SquaredSumWorker(Thread):

    def __init__(self, n, **kwargs) -> None:
        super().__init__(**kwargs)
        self._n = n
        self.start()  # mejor que se llame desde fuera??

    def _calculate_sum_squares(self):
        sum_squares = 0
        for i in range(self._n):
            sum_squares += i**2
        print(sum_squares)

    def run(self):
        self._calculate_sum_squares()


class SleepyWorker(Thread):
    def __init__(self, seconds, **kwargs):
        super().__init__(**kwargs)
        self._seconds = seconds
        self.start()

    def _sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self._sleep_a_little()


def main():

    print(detect_available_configs())

    can_to_vlcb = Can2Vlcb(name="can_to_vlcb")
    can_to_vlcb.start()

    # cal_start_time = time.time()
    # current_workers = []
    # for i in range(5):
    #     max_value = (1 + i) * 1_000_000
    #     squared_sum_worker = SquaredSumWorker(n=max_value, name=f"SSW#{i}")
    #     current_workers.append(squared_sum_worker)
    # for i in enumerate(current_workers):
    #     current_workers[i].join()
    # print(f"Calculated ....took {round(time.time() - cal_start_time, 1)}")

    # sleep_start_time = time.time()
    # current_workers = []
    # for seconds in range(1, 6):
    #     sleepy_worker = SleepyWorker(seconds=seconds)
    #     current_workers.append(sleepy_worker)
    # for i in enumerate(current_workers):
    #     current_workers[i].join()
    # print(f"Sleeping ....took {round(time.time() - sleep_start_time, 1)}")

    time.sleep(3)

    can_to_vlcb.terminate()
    can_to_vlcb.join()


if __name__ == "__main__":
    main()
