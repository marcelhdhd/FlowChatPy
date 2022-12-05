import socket
import threading

import discovery_handler

sockets = []


class IncomingConnection(threading.Thread):

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 0))
        self.sock.listen(1)
        discovery_handler.discover_remoteport = self.sock.getsockname()[1]
        (client, address) = self.sock.accept()
        sockets.add = (client, address)


class OutgoingConnection:

    def send(socket, msg):
        socket.send(msg)