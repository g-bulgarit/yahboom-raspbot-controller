import sys
import os

sys.path.append(os.getcwd())

from smbus2 import SMBus
from packages.commons.exceptions import ConnectionLost
from packages.commons.commands import movementMessage, servoMessage, stopMessage
from typing import Union
from loguru import logger
from datetime import datetime


class Robot:
    address = 0x16

    def __init__(self) -> None:
        self.robot = self.i2c_connect()
        pass

    def i2c_connect(self):
        return SMBus(1)

    def _write_byte(self, register: int, data: int) -> None:
        try:
            self.robot.write_byte_data(self.address, register, data)
        except:
            raise ConnectionLost()

    def _write_byte_array(self, register: int, data: int) -> None:
        try:
            self.robot.write_i2c_block_data(self.address, register, data)
        except:
            raise ConnectionLost()

    def triage(self, msg: Union[stopMessage, servoMessage, movementMessage]) -> bool:
        time_now = datetime.now().strftime("%H:%M:%S")
        if isinstance(msg, stopMessage):
            logger.debug(f"{time_now} | Recieved stop command")
            self._write_byte(0x02, 0x00)
            return True

        elif isinstance(msg, servoMessage):
            logger.debug(f"{time_now} | Recieved servo command")
            data = [msg.servo_id, msg.servo_angle]
            self._write_byte_array(0x03, data)

        elif isinstance(msg, movementMessage):
            logger.debug(f"{time_now} | Recieved move command")
            data = [
                msg.left_motor_dir,
                msg.left_motor_speed,
                msg.right_motor_dir,
                msg.right_motor_speed,
            ]
            self._write_byte_array(0x01, data)
            return True

        else:
            return False
