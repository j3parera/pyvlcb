"""Prueba."""

from time import sleep

from pyvlcb.modules.controller import Controller
from pyvlcb.services.serialui import ConsoleUIService


class KK(Controller):
    """
    _summary_

    Args:
        Controller (_type_): _description_
    """

    def __init__(self):
        super().__init__([ConsoleUIService()], "pyvlcb/config.json")


if __name__ == "__main__":
    kk = KK()
    while True:
        kk.services[0].process(None)
        sleep(0.1)
