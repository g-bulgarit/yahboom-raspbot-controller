from typing import List
from threading import Thread
import sys
import os

from services.controller_keyboard_service.keyboard_control import (
    launch_keyboard_listener,
)

from services.controller_camera_service.camera_stream import launch_camera_stream

sys.path.append(os.getcwd())

functions_to_run = [
    launch_keyboard_listener,
    launch_camera_stream,
]


if __name__ == "__main__":
    threads: List[Thread] = []
    for func in functions_to_run:
        thread = Thread(target=func)
        threads.append(thread)

    for thread in threads:
        thread.start()
