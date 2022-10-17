class FlowUser:                         # Constructor for the User Part
    id = 0

    def __init__(self, ip, name):
        self.id = id
        self.ip = ip
        self.name = name
        id += 1

    def sendMessage(self, message):
        self.placeholder = message      # TODO need network function to send message
                                        # TODO gui implemtation to display on the screen

    def receiveMessage(self, message):
        self.placeholder = message      # TODO need network function to receive message
                                        # TODO gui implemtation to display on the screen


flowuserlist = []


def getandcreateflowuser(ip):           # TODO needs to be testing to work
    for user in enumerate(flowuserlist):
        if user.ip == ip:
            return user
    flowuser = FlowUser(ip, "FlowUser#" + id)
    flowuserlist[id] = flowuser
    return flowuser
