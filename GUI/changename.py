from tkinter import *
import Network.networkmanager
from customtkinter import CTkToplevel, CTkEntry, CTkButton


class NameChangeWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Change name")
        self.attributes('-topmost', True)
        self.testname = StringVar()
        self.nameentrywidget = CTkEntry(self, textvariable=self.testname)
        self.changenameButton = CTkButton(self, text="Confirm", command=self.changeName)
        self.nameentrywidget.pack()
        self.changenameButton.pack()

    def changeName(self):
        print("nameentrywidget.get() = " + self.nameentrywidget.get())
        Network.networkmanager.username = self.nameentrywidget.get()
        self.destroy()