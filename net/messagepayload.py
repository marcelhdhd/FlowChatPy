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


class Incoming:

    def __init__(self, objectIn):
        self.objectIn = objectIn

    def json_to_messagepayload(self):
        paylaod = json.loads(self.objectIn)
        payload_type = paylaod['type']
        if payload_type == 'userMessage':
            ret = UserMessage()
            ret.message = paylaod["message"]
            ret.date = paylaod["date"]
            ret.ip = paylaod["ip"]
            ret.name = paylaod["name"]
            return ret
        elif payload_type == "customMessage":
            ret = CustomMessage()
            ret.message = paylaod["message"]
            return ret
        elif payload_type == "command":
            ret = Command()
            ret.command = paylaod["command"]
            ret.date = paylaod["date"]
            ret.ip = paylaod["ip"]
            return ret
        else:
            print(paylaod)
            raise TypeError("incoming no valid flowChat json")
