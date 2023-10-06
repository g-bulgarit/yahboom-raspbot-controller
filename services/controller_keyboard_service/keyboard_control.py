import zmq
import sys
import os
import time
from loguru import logger

sys.path.append(os.getcwd())
from packages.commons.commands import (
    movementMessage,
    stopMessage,
    servoMessage,
    honkMessage,
)
from pynput import keyboard


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.197:5678")

pressed_keys = set()
last_message = stopMessage(0)
tick_rate = 20


def on_press(key):
    try:
        if key.char in ["w", "a", "s", "d", "j", "k", "l", "o", "m", "h"]:
            pressed_keys.add(key.char)
    except AttributeError:
        pass


def on_release(key):
    try:
        if key.char in ["w", "a", "s", "d", "j", "k", "l", "o", "m", "h"]:
            pressed_keys.remove(key.char)
    except AttributeError:
        pass


def send_motion_command():
    global last_message
    # Single button combos
    if pressed_keys == {"w"}:
        msg = movementMessage(1, 200, 1, 200)
    elif pressed_keys == {"s"}:
        msg = movementMessage(0, 200, 0, 200)
    elif pressed_keys == {"a"}:
        msg = movementMessage(0, 200, 1, 200)
    elif pressed_keys == {"d"}:
        msg = movementMessage(1, 200, 0, 200)
    elif pressed_keys == {"j"}:
        msg = servoMessage(1, 120)
    elif pressed_keys == {"k"}:
        # Special case...
        msg = servoMessage(1, 90)
        socket.send_pyobj(msg)
        _ = socket.recv_pyobj()
        msg = servoMessage(2, 90)
    elif pressed_keys == {"l"}:
        msg = servoMessage(1, 60)
    elif pressed_keys == {"o"}:
        msg = servoMessage(2, 60)
    elif pressed_keys == {"m"}:
        msg = servoMessage(2, 120)
    elif pressed_keys == set():
        msg = stopMessage(0)
    elif pressed_keys == {"h"}:
        msg = honkMessage(0)

    # Mixed keys
    elif pressed_keys == {"w", "a"}:
        msg = movementMessage(1, 80, 1, 200)
    elif pressed_keys == {"w", "d"}:
        msg = movementMessage(1, 200, 1, 80)
    else:
        print(f"Exception case; pressed {pressed_keys}")
        msg = stopMessage(0)

    if not (isinstance(last_message, stopMessage) and isinstance(msg, stopMessage)):
        socket.send_pyobj(msg)
        _ = socket.recv_pyobj()
    last_message = msg


def launch_keyboard_listener():
    logger.debug("Keyboard listener running.")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        send_motion_command()
        time.sleep(1 / tick_rate)


if __name__ == "__main__":
    launch_keyboard_listener()
