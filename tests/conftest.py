import json
import logging
import os
import time

import pytest
from filelock import FileLock


@pytest.fixture(scope="session", autouse=True)
def choose_dut(worker_id):
    while True:
        with FileLock("dut.lock"):
            logging.info("choose a dut")
            with open("dut.json", "r") as f:
                info = json.load(f)

            for i in info:
                if i["worker"] is None:
                    logging.info(f"choose dut[lock] {i['name']} for {worker_id}")
                    i["worker"] = worker_id

                    from tests.utils import Device, set_dut

                    set_dut(Device(i["name"]))

                    break
            else:
                logging.info("no available dut, wait for another round")
                time.sleep(1)
                continue

            with open("dut.json", "w") as f:
                json.dump(info, f, indent=4)
            break

    yield

    with FileLock("dut.lock"):
        with open("dut.json", "r") as f:
            info = json.load(f)
        for i in info:
            if i["worker"] == worker_id:
                i["worker"] = None
                logging.info(f"choose dut[release] {i['name']} for {worker_id}")
                break
        else:
            raise Exception("release dut not found")

        with open("dut.json", "w") as f:
            json.dump(info, f, indent=4)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    log_file = f"pytest_{worker_id}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=[logging.FileHandler(log_file, mode="w"), logging.StreamHandler()],
    )
