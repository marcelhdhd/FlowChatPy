import socket
import time
import threading

broadcast_ip = '255.255.255.255'
port_send = 24990
port_recv = 25000
broadcast_address = (broadcast_ip, port_recv)
msg_encoding = "utf-8"
msg_payload = "FlowChatDiscover says HELLO"
msg_broadcast = (msg_payload, msg_encoding)
message_queue = []


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
    # broadcast hello
    sock.sendto(bytes(msg_payload, msg_encoding), broadcast_address)

    return sock


# method for listening and handling of incoming messages
def listen_handle_messages():
    while True:
        # Thread will wait here until a packet on recv_socket is received
        # will write message and ip and port to variable
        msg_and_address = listen_sock.recvfrom(4096)
        # message will be utf-8 decoded
        message = msg_and_address[0].decode(msg_encoding)
        # also save ip addr to display in GUI
        addr = msg_and_address[1][0]
        # also save port for ?
        ip = msg_and_address[1][1]
        print("recieved message from: " + addr + ":" + message)
        message_queue.append((addr, message))
        # todo: send message and ip addr to GUI


# method for sending a message
def send_message(message):
    # also utf-8 encode that message
    send_sock.send(message.encode(msg_encoding))


# deamonize the listener so that one does not block the main thread
def main():
    listener_daemon = threading.Thread(target=listen_handle_messages(), daemon=True)
    listener_daemon.start()


hostname = ip_finder()
listen_sock = ready_listen_socket()
send_sock = ready_send_socket()
main()
