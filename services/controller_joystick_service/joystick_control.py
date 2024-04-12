from enum import Enum, IntEnum
import numpy as np
from multiprocessing import Process, Array, Lock
import time
import zmq
import sys
import os

sys.path.append(os.getcwd())
from packages.commons.commands import (
    movementMessage,
    servoMessage,
)

DEFAULT_DELTA = 0.01
DEADBAND = 0.03
MAX_PAN_TILT_DELTA = 80


class EventTypes(Enum):
    JoystickMotion = 1536


class JoysticAxes(IntEnum):
    LeftX = 0
    LeftY = 1
    RightX = 2
    RightY = 3


lock = Lock()


class JoystickControl:
    def __init__(self) -> None:
        self.joystick_data = Array("d", [0.0, 0.0, 0.0, 0.0])
        self.joystick_process = Process(
            target=sample_joysticks_positions, args=(self.joystick_data,), daemon=True
        )

    def start_listener(self) -> None:
        self.joystick_process.start()

    def get_joystick_value(self) -> tuple[float, float, float, float]:
        return self.joystick_data


def lowpass_and_deadband(
    old_value: float, new_value: float, delta: float = DEFAULT_DELTA
) -> float:
    if np.abs(new_value) < DEADBAND:
        return 0.0

    delta_values = np.abs(new_value - old_value)
    if delta_values < delta:
        return old_value

    return new_value


def sample_joysticks_positions(joystick_data_array: Array):
    import pygame

    pygame.init()
    joysticks = []
    clock = pygame.time.Clock()
    keepPlaying = True

    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()

    left_x, left_y = 0.0, 0.0
    right_x, right_y = 0.0, 0.0
    while keepPlaying:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == EventTypes.JoystickMotion.value:
                if event.axis == JoysticAxes.LeftX:
                    left_x = lowpass_and_deadband(left_x, event.value)
                elif event.axis == JoysticAxes.LeftY:
                    left_y = lowpass_and_deadband(left_y, event.value)
                elif event.axis == JoysticAxes.RightX:
                    right_x = lowpass_and_deadband(right_x, event.value)
                elif event.axis == JoysticAxes.RightY:
                    right_y = lowpass_and_deadband(right_y, event.value)
                with lock:
                    joystick_data_array[0] = left_x
                    joystick_data_array[1] = left_y
                    joystick_data_array[2] = right_x
                    joystick_data_array[3] = right_y


MAX_MOTOR_VAL = 200


def set_drive_motor_vectors(x, y) -> None:
    l_val = -1 * MAX_MOTOR_VAL * (y - x) * 1.5
    r_val = -1 * MAX_MOTOR_VAL * (y + x) * 1.5
    l_sign, r_sign = False, False
    if l_val > 0:
        l_sign = True

    if r_val > 0:
        r_sign = True

    l_val = min(int(l_val), 255)
    r_val = min(int(r_val), 255)

    msg = movementMessage(l_sign, np.abs(l_val), r_sign, np.abs(r_val))
    socket.send_pyobj(msg)
    _ = socket.recv_pyobj()


def set_cam_motor_vectors(x, y) -> None:

    pan = 90 + int(-1 * x * MAX_PAN_TILT_DELTA)
    tilt = 90 + int(y * MAX_PAN_TILT_DELTA)

    msg = servoMessage(1, pan)
    socket.send_pyobj(msg)
    _ = socket.recv_pyobj()

    msg = servoMessage(2, tilt)
    socket.send_pyobj(msg)
    _ = socket.recv_pyobj()


if __name__ == "__main__":
    jc = JoystickControl()
    jc.start_listener()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.1.197:5678")

    while True:
        lx, ly, rx, ry = jc.get_joystick_value()
        set_drive_motor_vectors(lx, ly)
        set_cam_motor_vectors(rx, ry)

        # print(f"{msg.left_motor_speed:.2f}, {msg.right_motor_speed:.2f}")
        time.sleep(1 / 60)
