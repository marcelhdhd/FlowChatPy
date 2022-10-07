import socket

broadcast_ip = '255.255.255.255'
discover_localport = 24990
discover_remoteport = 25000
broadcast_address = (broadcast_ip, discover_remoteport)
msg_encoding = "utf-8"
msg_payload = "FlowChatDiscover"
msg_broadcast = (msg_payload, msg_encoding)

# method for sending "FlowChatDiscover" broadcast packages
async def broadcast_discover():
    # UDP socket for broadcast (ipv4, udp(?), udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Allow broadcast on socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind socket to local ip
    sock.bind((ip_finder(), discover_localport))
    # sock.sendto(bytes(msg_payload, msg_encoding), broadcast_address)
    sock.sendto(bytes(msg_payload, msg_encoding), broadcast_address)

# method for finding local ip
def ip_finder():
    # Workaround needed to find a correct, working, local ip, because sometimes there are multiple interfaces
    # e.g. "Ethernet-Adapter VirtualBox Host-Only Network"
    # and python selects the wrong one
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ipsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Connect to ipv4 from the internet
    ipsock.connect(('1.1.1.1', 53))
    # return local ip from which the connection was established
    return ipsock.getsockname()[0]

# method for finding "FlowChatDiscover" packages
async def broadcast_listener():
    # UDP socket for broadcast (ipv4, udp(?), udp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind to all interfaces on broadcast port
    sock.bind(("0.0.0.0", 25000))
    # will wait until a packet was recieved
    returnmsg, returnip = sock.recvfrom(4096)
    # debug printing of ip:port = message
    print("recieved message from: " + str(returnip[0]) + ":" + str(returnip[1]) + " = " + str(returnmsg))


while True:
    broadcast_listener()



broadcast_discover()