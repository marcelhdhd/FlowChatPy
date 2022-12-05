import socket
import threading
import time

import netmanager

broadcast_ip = '255.255.255.255'
hostname = ''
discover_localport = 24990
discover_remoteport = 25000
broadcast_address = (broadcast_ip, discover_remoteport)
msg_encoding = "utf-8"
msg_payload = "FlowChatDiscover"
msg_broadcast = (msg_payload, msg_encoding)


# method for sending "FlowChatDiscover" broadcast packages
def broadcast_discover():
    # find out local ip
    ip_finder()

    while True:
        # UDP socket for broadcast (ipv4, udp(?), udp)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow broadcast on socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Bind socket to local ip
        sock.bind((hostname, discover_localport))
        # vor every 10 seconds send broadcast packet
        sock.sendto(bytes(msg_payload, msg_encoding), broadcast_address)
        # Close socket so that if discover_remoteport changed, that change is sent instead
        sock.close()
        time.sleep(10)


# method for finding local ip
def ip_finder():
    # Workaround needed to find a correct, working, local ip, because sometimes there are multiple interfaces
    # e.g. "Ethernet-Adapter VirtualBox Host-Only Network" and python selects the wrong one
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ipsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Connect to ipv4 from the internet
    ipsock.connect(('1.1.1.1', 53))
    # return local ip from which the connection was established
    hostname = ipsock.getsockname()[0]
    ipsock.close()
    return hostname


# method for finding "FlowChatDiscover" packages
def broadcast_listener():
    print("DEBUG: broadcast_listener")
    # UDP socket for broadcast (ipv4, udp(?), udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind to all interfaces on broadcast port
    sock.bind(("0.0.0.0", 25000))
    print("DEBUG: broadcast_listener")
    while True:
        # will wait until a packet was recieved
        returnmsg, returnip = sock.recvfrom(4096)
        # decode returnmsg from bytes to string (utf-8)
        returnmsg = returnmsg.decode(msg_encoding)
        # debug printing of ip:port = message
        print("recieved message from: " + str(returnip[0]) + ":" + str(returnip[1]) + " = " + str(returnmsg))
        # if broadcast packet message content is "FlowChatDisover" add to netmanager user list
        if ( returnmsg == "FlowChatDiscover" ):
            print("DEBUG: calling add_user")
            netmanager.add_user(returnip[0])


# Start discovery and listener methods as own threads
def discoveryStart():
    # see: https://docs.python.org/3/library/threading.html
    listener_daemon = threading.Thread(target=broadcast_listener, daemon=True)
    broadcast_daemon = threading.Thread(target=broadcast_discover, daemon=True)
    print("DEBUG: discoveryStart")
    listener_daemon.start()
    broadcast_daemon.start()

discoveryStart()
time.sleep(30)