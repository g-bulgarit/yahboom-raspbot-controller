import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.bind("tcp://*:5678")

    while True:
        socket.send_pyobj()
