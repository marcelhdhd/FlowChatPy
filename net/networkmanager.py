import asyncio
import encodings
import socket
import threading
import re
import time

from datetime import datetime

from net.listenserver import ListenProtocol
from settings import settings
from net import messagepayload as payloads

# basic networking code that allows messages to be passed over broadcast to other users as bitstream
message_queue = []
port = 25000
broadcast_address = ('255.255.255.255', port)
msg_encoding = "utf-8"


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
    print("hostname: " + hostname)
    sock.sendto(bytes(message, "utf-8"), ("255.255.255.255", 2490))
    message_queue.append(message)
    sock.close()


# method for sending custom messages
def send_custom_message(message):
    payloadMessage = payloads.CustomMessage()
    payloadMessage.message = message
    # also utf-8 encode that message
    send(payloadMessage.toJson())


# method for closing sockets and listeners
def on_closing():
    send_message("Bye")


class Networkmanager():
    def __init__(self):
        super().__init__()
        self.run()

    class ListenProtocol(asyncio.DatagramProtocol):
        def __init__(self):
            super().__init__()

        def connection_made(self, transport) -> "Used by asyncio":
            self.transport = transport

        def datagram_received(self, data, addr) -> "Main entrypoint for processing message":
            print(f"Recieved Message from: {addr}")
            print(f"With message: {data}")
            message_queue.append(data)

    def start(self):
        loop = asyncio.new_event_loop()
        t = loop.create_datagram_endpoint(ListenProtocol, local_addr=(hostname, port))
        print("Loop starting")
        loop.run_until_complete(t)
        loop.run_forever()

    def run(self):
        print("Network Thread started")
        threading.Thread(target=self.start).start()
