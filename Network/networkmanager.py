import socket
import threading
import re

from datetime import datetime
from Core import messagepayload as payloads

# basic networking code that allows messages to be passed over broadcast to other users as bitstream
broadcast_ip = '255.255.255.255'
port_send = 24990
port_recv = 25000
broadcast_address = (broadcast_ip, port_recv)
msg_encoding = "utf-8"
message_queue = []
username = None


# method for finding local ip
def ip_finder():
    # Workaround needed to find a correct, working, local ip, because sometimes there are multiple interfaces
    # e.g. "Ethernet-Adapter VirtualBox Host-Only Network" and python selects the wrong one
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ipsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Connect to ipv4 from the internet
    ipsock.connect(('1.1.1.1', 53))
    # return local ip from which the connection was established
    ip = ipsock.getsockname()[0]
    ipsock.close()
    return ip


# method for readying incoming socket
def ready_listen_socket():
    # UDP socket for broadcast recv (ipv4, udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Allow broadcast on socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind socket to any ip and recv port
    sock.bind(("0.0.0.0", port_recv))
    return sock


# method for readying outgoing socket
def ready_send_socket():
    # UDP socket for broadcast send (ipv4, udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Allow broadcast on socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind socket to any ip and recv port
    sock.bind((hostname, port_send))
    return sock


# method for listening and handling of incoming messages
def listen_handle_messages():
    while True:
        # Thread will wait here until a packet on recv_socket is received
        # will write message and ip and port to variable
        msg_and_address = listen_sock.recvfrom(4096)
        # message will be utf-8 decoded
        json = msg_and_address[0].decode(msg_encoding)
        # also save ip addr to display in GUI
        # todo change displayed addr to chosen username to allow recognition of users
        # addr = msg_and_address[1][0]
        # also save port for ?
        # ip = msg_and_address[1][1]
        print("recieved message "+json)
        message_queue.append(json)


# method for sending a user specific message
def send_message(message):
    payloadmessage = payloads.UserMessage()
    if username == None:
         payloadmessage.name = hostname # TODO Change name
    else:
        payloadmessage.name = username
    payloadmessage.ip = hostname
    payloadmessage.message = check_emote(message)
    payloadmessage.date = datetime.now().strftime("[%H:%M:%S] ")
    # also utf-8 encode that message
    send_sock.sendto(payloadmessage.toJson().encode(msg_encoding), broadcast_address)

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
    send_sock.sendto(payloadMessage.toJson().encode(msg_encoding), broadcast_address)

# method for closing sockets and listeners
def on_closing():
    send_message("Bye")
    send_sock.close()
    listen_sock.close()


# daemonize the listener so that one does not block the main thread
def main():
    listener_daemon = threading.Thread(target=listen_handle_messages, daemon=True)
    listener_daemon.start()


hostname = ip_finder()
send_sock = ready_send_socket()
listen_sock = ready_listen_socket()
main()
