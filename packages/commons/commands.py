from dataclasses import dataclass


@dataclass
class movementMessage:
    left_motor_dir: bool
    left_motor_speed: int
    right_motor_dir: bool
    right_motor_speed: int


@dataclass
class servoMessage:
    servo_id: int
    servo_angle: int


@dataclass
class stopMessage:
    stop: int


@dataclass
class statusMessage:
    val: int


@dataclass
class honkMessage:
    val: int
