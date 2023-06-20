import asyncio
import socket
import threading
import re
from asyncio import transports

from datetime import datetime
from typing import Any

import net.messagepayload
from net.userlist import UserList
from settings import settings
from net import messagepayload as payloads

# basic networking code that allows messages to be passed over broadcast to other users as bitstream
message_queue = []
listen_port = 25000
broadcast_address = ('255.255.255.255', listen_port)
msg_encoding = "utf-8"
mask = '255.255.255.0'
running = False
user_list = UserList()


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


def check_emote(message):
    emotes = re.findall(r":.*?:", message)
    for emote_ex in emotes:
        message = re.sub(emote_ex, check_which_emote(emote_ex), message)
    return message


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
    send(payloadmessage.toJson())


def send(message: 'This is a UDP message') -> None:
    print("SENT message: " + message)
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", 25000))
    # message_queue.append(message)
    sock.close()


# method for sending custom messages
def send_custom_message(message):
    payloadMessage = payloads.CustomMessage()
    payloadMessage.message = message
    # also utf-8 encode that message
    send(payloadMessage.toJson())


# method for closing sockets and listeners
def on_closing():
    net.networkmanager.running = False
    stop = net.messagepayload.Command()
    stop.test = "testing"
    send(stop.toJson())
    user_list.remove_user(net.messagepayload.UserMessage.__name__)
    send_message("Bye")

def send_message_usernameRemoval(message):
    payloadmessage = payloads.UserMessage()
    if settings.settingsInstance.user_name is None:
        payloadmessage.name = hostname
    else:
        payloadmessage.name = settings.settingsInstance.user_name
    payloadmessage.ip = hostname
    payloadmessage.message = check_emote(message)
    payloadmessage.date = datetime.now().strftime("[%H:%M:%S] ")
    user_list.remove_user(payloadmessage.name)

    # also utf-8 encode that message
    send(payloadmessage.toJson())

def on_closing_userlist():
    net.networkmanager.running = False
    stop = net.messagepayload.Command()
    stop.test = "testing"
    send(stop.toJson())
    user_list.remove_user(net.messagepayload.UserMessage.__name__)
    send_message_usernameRemoval("Bye")




# workaround method for receiving messages
def listen_loop():
    net.networkmanager.running = True
    # UDP socket for broadcast recv (ipv4, udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Allow broadcast on socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind socket to any ip and recv port
    sock.bind(("0.0.0.0", listen_port))
    while running:
        # Thread will wait here until a packet on recv_socket is received
        # will write message and ip and port to variable
        msg_and_address = sock.recvfrom(4096)
        # message will be utf-8 decoded
        json = msg_and_address[0].decode(msg_encoding)

        # todo change displayed addr to chosen username to allow recognition of users
        if isinstance(net.messagepayload.Incoming(json).json_to_messagepayload(),
                      (net.messagepayload.UserMessage, net.messagepayload.CustomMessage)):
            print("RECIEVED message " + json)

            message_queue.append(json)
        elif isinstance(net.messagepayload.Incoming(json).json_to_messagepayload(), net.messagepayload.Command):
            print("RECIEVED command: " + json)
            pass
        else:
            print("RECIEVED packet: " + json)
            pass
    sock.close()


def run_daemon():
    listener_daemon = threading.Thread(target=listen_loop, daemon=True)
    listener_daemon.start()


# todo: implement asyncio socket endpoint management
class Networkmanager():
    def __init__(self):
        super().__init__()
        self.run()

    class ListenProtocol(asyncio.DatagramProtocol):
        def __init__(self):
            super().__init__()

        def connection_made(self, transport: transports.DatagramTransport) -> None:
            print("connection made")
            self.transport = transport

        def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
            print(f"Recieved Message from: {addr}")
            print(f"With message: {data}")
            message_queue.append(data)

    def start(self):
        loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(loop)
        protocol = self.ListenProtocol()
        t = loop.create_datagram_endpoint(lambda: protocol, local_addr=(hostname, listen_port))
        loop.run_until_complete(t)
        loop.run_forever()

    def run(self):
        print("Network Thread started")

        threading.Thread(target=self.start).start()
