import json


class Message:

    def __init__(self):
        self.type = "message"
        self.message = None
        self.date = None
        self.ip = None
        self.name = None

    def toJson(self):
        return json.dumps(self.__dict__)


class Command:

    def __init__(self):
        self.type = "command"
        self.command = None
        self.date = None
        self.ip = None

    def toJson(self):
        return json.dumps(self.__dict__)
