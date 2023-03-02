from tkinter import *
import Network.networkmanager
from customtkinter import CTkToplevel, CTkEntry, CTkButton


class NameChangeWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Change name")
        # title not showing due to window being to small
        # maybe disable window buttons and add close button to popup
        self.attributes('-topmost', True)

        self.testname = StringVar()
        self.nameentrywidget = CTkEntry(self, textvariable=self.testname)
        self.changenameButton = CTkButton(self, text="Change name", command=self.changeName)
        self.nameentrywidget.bind("<Return>", self.changeName)
        self.nameentrywidget.pack()
        self.changenameButton.pack()

    def changeName(self, *args):
        print("nameentrywidget.get() = " + self.nameentrywidget.get())
        Network.networkmanager.username = self.nameentrywidget.get()
        self.destroy()

