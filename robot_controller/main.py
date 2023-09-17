import zmq
from commons.commands import statusMessage
from robot_controller.robot_interface import Robot

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5678")

    robot = Robot()

    while True:
        msg = socket.recv_pyobj()
        ret_code = robot.triage(msg)
        socket.send_pyobj(statusMessage(ret_code))
