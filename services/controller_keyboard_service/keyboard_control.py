import zmq
import sys
import os
import time

sys.path.append(os.getcwd())
from packages.commons.commands import movementMessage, stopMessage, servoMessage
from pynput import keyboard


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.197:5678")

pressed_keys = set()
tick_rate = 20


def on_press(key):
    try:
        if key.char in ["w", "a", "s", "d", "j", "k", "l", "o", "m"]:
            pressed_keys.add(key.char)
    except AttributeError:
        pass


def on_release(key):
    try:
        if key.char in ["w", "a", "s", "d", "j", "k", "l", "o", "m"]:
            pressed_keys.remove(key.char)
    except AttributeError:
        pass


def send_motion_command():
    # Single button combos
    if pressed_keys == {"w"}:
        msg = movementMessage(1, 255, 1, 255)
    elif pressed_keys == {"s"}:
        msg = movementMessage(0, 255, 0, 255)
    elif pressed_keys == {"a"}:
        msg = movementMessage(0, 255, 1, 255)
    elif pressed_keys == {"d"}:
        msg = movementMessage(1, 255, 0, 255)
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

    # Mixed keys
    elif pressed_keys == {"w", "a"}:
        msg = movementMessage(1, 0, 1, 255)
    elif pressed_keys == {"w", "d"}:
        msg = movementMessage(1, 255, 1, 0)
    else:
        print(f"Exception case; pressed {pressed_keys}")
        msg = stopMessage(0)

    socket.send_pyobj(msg)
    _ = socket.recv_pyobj()


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        send_motion_command()
        time.sleep(1 / tick_rate)
