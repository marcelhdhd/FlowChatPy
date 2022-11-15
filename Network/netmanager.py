import discovery_handler

userlist = [] #evtl anders

# Starts the FlowChat discovery daemons
def flow_chat_discover():
    discovery_handler.discoveryStart()


# TODO: send Message
def send_message(message, user):
    return

# TODO: relay incoming messages recieved by recv.py to core
def recv_message():
    return

def get_users():
    bogo_userlist = ("192.168.12.23", "10.23.1.93")
    return bogo_userlist

# TODO: check if connections are still alive
def check_users():
    return

# TODO: remove user with id(?)
def remove_user(user):
    return

# add found connections to userlist
def add_user(user):
    if user not in userlist:
        userlist.append(user)
        print("DEBUG: " + user)
    return

