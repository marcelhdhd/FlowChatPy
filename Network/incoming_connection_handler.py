import socket
import sys

import netmanager

# See: https://github.com/zappala/python-networking-and-threading for further reading
class IncomingConnection:
    """ Connection that handles one client at a time. """
    def __init__(self, port):
        self.host = ""
        self.port = port
        self.size = 1024
        self.open_socket()

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
        except socket.error as (value, message):
            if self.server:
                self.server.close()
            print("Could not open socket: " + message)
            sys.exit(1)

    def run(self):
        while True:
            (client,adress) = self.server.accept()
            self.handleClient(client, adress)

    def handleClient(self, client, adress):
        """ Handle a client by storing ip,port and echoing data back """
        while True:
            data = client.recv(self.size)
            if data:
                netmanager.add_socket(client, adress)
                client.send(data)
            else:
                client.close()
                break