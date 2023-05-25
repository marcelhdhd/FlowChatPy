import os
import json
import stat

directoryUser = os.path.expanduser("~")
# Using "os.path.join" to make flowChat os independent (works on windows, linux, mac, ..)
# Also move settings folder to user home instead of "Program files", which required admin rights to write to
directoryFlowChat = os.path.join(directoryUser, ".flowChatPy")


class Settings:
    def __init__(self):
        self.focus_window = False
        self.user_name = None
        self.window_width = 660
        self.window_height = 480
        self.dark_mode = False

    def toJson(self):
        return json.dumps(self.__dict__)

    def existJsonValue(self, jsons, value):
        return value in jsons

    def load(self):
        if os.path.exists(os.path.join(directoryFlowChat, "settings.json")):
            # load if the file exists
            print("Found settings.json file")
            with open(os.path.join(directoryFlowChat, "settings.json"), "r") as readFile:
                print("Reading settings.json file")
                jsonString = json.loads(readFile.read())
                if self.existJsonValue(jsonString, "focus_window"):
                    self.focus_window = bool(jsonString["focus_window"])
                if self.existJsonValue(jsonString, "user_name"):
                    self.user_name = jsonString["user_name"]
                if self.existJsonValue(jsonString, "window_width"):
                    self.window_width = int(jsonString["window_width"])
                if self.existJsonValue(jsonString, "window_height"):
                    self.window_height = int(jsonString["window_height"])
                if self.existJsonValue(jsonString, "dark_mode"):
                    self.dark_mode = bool(jsonString["dark_mode"])
                print("Reading Finished!")
        else:
            # create a new settings file
            self.save()

    def save(self):
        try:
            print("Start saving settings.json file")
            if os.path.exists(directoryFlowChat):
                with open(os.path.join(directoryFlowChat, "settings.json"), "w") as writeFile:
                    writeFile.write(self.toJson())
                    print("Saving finished!")
            else:
                print("Did not found .flowChatPy directory, attempting to mkdir")
                os.mkdir(directoryFlowChat, stat.S_IWRITE)
                with open(os.path.join(directoryFlowChat, "settings.json"), "w") as writeFile:
                    print("Mkdir successful")
                    writeFile.write(self.toJson())
                    print("Saving Finished!")
        except:
            print("No permission to create directory/file")


settingsInstance = Settings()
settingsInstance.load()
