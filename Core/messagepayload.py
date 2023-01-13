import json


class Message:

    def __init__(self):
        self.message = None
        self.date = None
        self.ip = None
        self.name = None

    def toJson(self):
        return json.dumps(self.__dict__)


class Command:

    def __init__(self):
        self.command = None
        self.date = None
        self.ip = None

    def toJson(self):
        return json.dumps(self.__dict__)
