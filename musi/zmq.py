from __future__ import absolute_import

try:
    import zmq
except ImportError:
    raise Exception("Please install pyzmq to use components in this module.")


context = zmq.Context()

def ZmqSub(connect_str):
    socket = context.socket(zmq.SUB)
    socket.connect(connect_str)
    def zmq_sub(now):
        messages = []
        while True:
            try:
                messages.append(socket.recv_json(zmq.NOBLOCK))
            except zmq.ZMQError:
                break
        return messages
    return zmq_sub


def ZmqPub(bind_str, source_f):
    socket = context.bind(zmq.PUB)
    socket.bind(bind_str)
    def zmq_pub(now):
        values = source_f(now)
        for val in values:
            socket.send_json(val, zmq.NOBLOCK)
        return None
    return zmq_pub
