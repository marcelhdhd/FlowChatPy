import asyncio
import socket
import threading
import re

from datetime import datetime

from settings import settings
from net import messagepayload as payloads

# basic networking code that allows messages to be passed over broadcast to other users as bitstream
broadcast_ip = '255.255.255.255'
port = 25000
broadcast_address = (broadcast_ip, port)
msg_encoding = "utf-8"
message_queue = []


# method for finding local ip
def ip_finder():
    # Workaround needed to find a correct, working, local ip, because sometimes there are multiple interfaces
    # e.g. "Ethernet-Adapter VirtualBox Host-Only net" and python selects the wrong one
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ipsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Connect to ipv4 from the internet
    ipsock.connect(('1.1.1.1', 53))
    # return local ip from which the connection was established
    ip = ipsock.getsockname()[0]
    ipsock.close()
    return ip


hostname = ip_finder()


# method for listening and handling of incoming messages
#def listen_handle_messages():
#    while True:
#        # Thread will wait here until a packet on recv_socket is received
#        # will write message and ip and port to variable
#        # listen_sock.setblocking(False)
#        msg_and_address = listen_sock.recvfrom(4096)
#        # message will be utf-8 decoded
#        json = msg_and_address[0].decode(msg_encoding)
#        # also save ip addr to display in gui
#        # todo change displayed addr to chosen username to allow recognition of users
#        # addr = msg_and_address[1][0]
#        # also save port for ?
#        # ip = msg_and_address[1][1]
#        print("recieved message " + json)
#        message_queue.append(json)


# method for sending a user specific message
def send_message(message):
    payloadmessage = payloads.UserMessage()
    if settings.settingsInstance.user_name is None:
        payloadmessage.name = hostname
    else:
        payloadmessage.name = settings.settingsInstance.user_name
    payloadmessage.ip = hostname
    payloadmessage.message = check_emote(message)
    payloadmessage.date = datetime.now().strftime("[%H:%M:%S] ")
    # also utf-8 encode that message
    print("Message send")
    send(payloadmessage.toJson())


def send(message: 'This is a UDP message') -> None:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode(msg_encoding), (hostname, port))


def check_emote(message):
    emotes = re.findall(r":.*?:", message)
    for emote_ex in emotes:
        message = re.sub(emote_ex, check_which_emote(emote_ex), message)
    return message


def check_which_emote(emote_ex):
    emote = re.sub(":", "", emote_ex)
    if emote == "smile":
        return "😊"
    elif emote == "crylaugh":
        return "😂"
    elif emote == "cool":
        return "😎"
    elif emote == "think":
        return "🤔"
    elif emote == "smirk":
        return "😏"
    elif emote == "sad":
        return "🙁"
    elif emote == "yawn":
        return "🥱"
    elif emote == "cry":
        return "😭"
    elif emote == "fear":
        return "😱"
    elif emote == "clown":
        return "🤡"
    else:
        return emote_ex


# method for sending custom messages
def send_custom_message(message):
    payloadMessage = payloads.CustomMessage()
    payloadMessage.message = message
    # also utf-8 encode that message
    send(payloadMessage.toJson())


# method for closing sockets and listeners
def on_closing():
    send_message("Bye")
    #send_sock.close()
    #listen_sock.close()


class ListenProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport) -> "Used by asyncio":
        self.transport = transport

    def datagram_received(self, data, addr) -> "Main entrypoint for processing message":
        print(f"Recieved Message from: {addr}")
        print(f"With message: {data}")
        message_queue.append(data)


# use asyncio such that one does not block the main thread
async def main():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(ListenProtocol, local_addr=(hostname, port))
    loop.run_until_complete(t)
    loop.run_forever()
    # listener_daemon = threading.Thread(target=listen_handle_messages, daemon=True)
    # print("Starting network listener daemon")
    # listener_daemon.start()
