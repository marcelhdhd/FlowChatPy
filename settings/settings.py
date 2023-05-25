import os
import json
import stat

directoryUser = os.path.expanduser("~")
directorySettings = 'C:\\Program Files (x86)\\FlowChat'


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
        if os.path.exists(directorySettings):
            # load if the file exists
            print("Loading File...")
            with open(directorySettings + "\\settings.json", "r") as readFile:
                print("Reading File...")
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
            print("Start Saving File...")
            if os.path.exists(directorySettings):
                with open(directorySettings, "w") as writeFile:
                    writeFile.write(self.toJson())
                    print("Saving Finished!")
            else:
                os.mkdir(directorySettings, stat.S_IWRITE)
                with open(directorySettings + "\\settings.json", "w") as writeFile:
                    writeFile.write(self.toJson())
                    print("Saving Finished!")
        except:
            print("No permission to create directory/file")


settingsInstance = Settings()
settingsInstance.load()
