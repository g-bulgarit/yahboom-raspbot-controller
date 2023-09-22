import RPi.GPIO as GPIO
import time
from threading import Thread

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)


def honk():
    GPIO.output(32, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(32, GPIO.LOW)


def honk_in_thread():
    thread = Thread(target=honk)
    thread.start()
