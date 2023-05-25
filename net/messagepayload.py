import json


# class constructor for the user message
class UserMessage:

    def __init__(self):
        self.type = "userMessage"
        self.message = None
        self.date = None
        self.ip = None
        self.name = None

    def toJson(self):
        return json.dumps(self.__dict__)


# class constructor for custom messages
class CustomMessage:

    def __init__(self):
        self.type = "customMessage"
        self.message = None

    def toJson(self):
        return json.dumps(self.__dict__)


# class constructor for custom user commands
class Command:

    def __init__(self):
        self.type = "command"
        self.command = None
        self.date = None
        self.ip = None

    def toJson(self):
        return json.dumps(self.__dict__)
