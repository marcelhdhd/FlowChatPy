import discovery_handler

userlist = []

# Starts the FlowChat discovery daemons
def flow_chat_discover():
    discovery_handler.discoveryStart()


# TODO: send Message
def send_message(message, user):
    return

# TODO: relay incoming messages recieved by recv.py to core
def recv_message():
    return


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

