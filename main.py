import zmq
from commons.commands import movementMessage, stopMessage, servoMessage
from pynput import keyboard

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.197:5678")


def on_press(key):
    if key == keyboard.Key.esc:
        stop = True
    if key.char == "w":
        msg = movementMessage(1, 255, 1, 255)
    if key.char == "s":
        msg = movementMessage(0, 255, 0, 255)
    if key.char == "a":
        msg = movementMessage(0, 255, 1, 255)
    if key.char == "d":
        msg = movementMessage(1, 255, 0, 255)
    if key.char == "l":
        msg = servoMessage(1, 60)
    if key.char == "k":
        msg = servoMessage(1, 90)
        socket.send_pyobj(msg)
        _ = socket.recv_pyobj()
        msg = servoMessage(2, 90)
    if key.char == "j":
        msg = servoMessage(1, 120)
    if key.char == "o":
        msg = servoMessage(2, 60)
    if key.char == "m":
        msg = servoMessage(2, 120)
    if key.char == "q":
        msg = stopMessage(0)

    socket.send_pyobj(msg)
    _ = socket.recv_pyobj()


def on_release(key):
    socket.send_pyobj(stopMessage(0))
    _ = socket.recv_pyobj()


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()
