import os
import json

directoryUser = os.path.expanduser("~")
directorySettings = directoryUser + "\'flowchat\'settings.json"


class Settings:
    def __init__(self):
        self.file = None

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
        if os.path.exists(directorySettings):
            print("Loading File...")
            # load if the file exists
            self.file = open(directorySettings)
            try:
                print("Reading File...")
                jsonstring = self.file.read()
                if self.existJsonValue(jsonstring, "focus_window"):
                    self.focus_window = bool(jsonstring["focus_window"])
                if self.existJsonValue(jsonstring, "user_name"):
                    self.user_name = jsonstring["user_name"]
                if self.existJsonValue(jsonstring, "window_width"):
                    self.window_width = int(jsonstring["window_width"])
                if self.existJsonValue(jsonstring, "window_height"):
                    self.window_height = int(jsonstring["window_height"])
                if self.existJsonValue(jsonstring, "dark_mode"):
                    self.dark_mode = bool(jsonstring["dark_mode"])
                print("Reading Finished!")
            finally:
                self.file.close()
        else:
            # create a new settings file
            self.save()

    def save(self):
        print("Start Saving File...")
        self.file = open(directorySettings, "w")
        try:
            self.file.write(self.toJson())
        finally:
            self.file.close()
            print("Saving Finished")


settingsInstance = Settings();
