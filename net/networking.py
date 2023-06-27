import asyncio as asyncio
import logging
from asyncio import transports
import socket
from datetime import datetime
from typing import Any
import re
import sys
from net.messagepayload import UserMessage, CustomMessage, Command
from net.userlist import UserList
from settings import settings

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# workaround method for finding local ip
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
user_list = UserList()

class ListenProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.transport = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 65432))

    def connection_made(self, transport: transports.DatagramTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        logging.info("Recieved Message from: {addr}")
        logging.info("With message: {data}")
        self.socket.sendall(bytes(data))


def send(message: 'This is a UDP message') -> None:
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info("SENT message: " + message)
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    for ip in allips:
        logging.info("SENT IP " + ip)
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, 0))
        sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", 25000))
        sock.close()

def send_message(message):
    payloadmessage = UserMessage()
    if settings.settingsInstance.user_name is None:
        payloadmessage.name = hostname
    else:
        payloadmessage.name = settings.settingsInstance.user_name
    payloadmessage.ip = hostname
    payloadmessage.message = check_emote(message)
    payloadmessage.date = datetime.now().strftime("[%H:%M:%S] ")
    # also utf-8 encode that message
    send(payloadmessage.toJson())

# method for sending custom messages
def send_custom_message(message):
    payloadMessage = CustomMessage()
    payloadMessage.message = message
    # also utf-8 encode that message
    send(payloadMessage.toJson())

# method for closing sockets and listeners
def on_closing():
    stop = Command()
    stop.test = "testing"
    send(stop.toJson())
    user_list.remove_user(UserMessage.__name__)
    send_message("__//Bye//__")

def send_message_usernameRemoval(message):
    payloadmessage = UserMessage()
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

def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    protocol = ListenProtocol()
    t = loop.create_datagram_endpoint(lambda: protocol, local_addr=(hostname, 25000))
    loop.run_until_complete(t)
    loop.run_forever()
    loop.close()