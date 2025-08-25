import logging
import time
from typing import Optional


class Device:
    def __init__(self, name: str) -> None:
        self.name = name


g_dut: Optional[Device] = None

def set_dut(device: Device) -> None:
    assert device is not None, "Device cannot be None"
    global g_dut
    g_dut = device

def get_dut() -> Device:
    assert g_dut is not None, "Device not initialized"
    return g_dut


def do_nothing():
    logging.info(f"Doing nothing in {get_dut().name}")
    return


def do_easy_thing():
    logging.info(f"Doing easy thing in {get_dut().name}")
    time.sleep(1)


def do_heavy_thing():
    logging.info(f"Doing heavy thing in {get_dut().name}")
    time.sleep(5)
