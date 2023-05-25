import asyncio
import os
import random
import socket

HOST, PORT = 'localhost', 25000

def send_test_message(message: 'This is a UDP message') -> None:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM) #UDP
    sock.sendto(message.encode(), (HOST, PORT))

async def write_message() -> 'Continuously write messages to UDP port 25000':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fp = open(os.path.join(dir_path, "listenserver.py"))
    print("writing")
    for line in fp.readlines():
        await asyncio.sleep(random.uniform(0.1, 0.3))
        send_test_message(line)


class ListenProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport) -> "Used by asyncio":
        self.transport = transport

    def datagram_received(self, data, addr) -> "Main entrypoint for processing message":
        # Here is where you would push message to whatever methods/class you want
        print(f"Recieved Syslog message: {data}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(ListenProtocol, local_addr=('0.0.0.0', PORT))
    loop.run_until_complete(t) # Server starts listening
    loop.run_until_complete(write_message()) # Start writing messages (or running tests)
    loop.run_forever()