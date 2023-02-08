import json
import os
import threading
import time
import tkinter
from tkinter import *
from tkinter import messagebox

import customtkinter
from customtkinter import *

import Network.networkmanager


class NameChangeWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Change name")
        self.testname = StringVar()
        self.nameentrywidget = CTkEntry(self, textvariable=self.testname)
        self.changenameButton = CTkButton(self, command=self.changeName)
        self.nameentrywidget.pack()
        self.changenameButton.pack()

    def changeName(self):
        print("nameentrywidget.get() = " + self.nameentrywidget.get())
        Network.networkmanager.username = self.nameentrywidget.get()


# In-depth tutorial for tkinter
# https://tkdocs.com/tutorial/onepage.html
class Guimanager(CTk):

    # the following code defines the main chat window in its entirety##
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Chat Window
        self.gui = CTk()
        set_default_color_theme("dark-blue")  # themeeeeeeeeee
        ##################################
        # Here is the window initialized #
        ##################################
        # Title of the window
        self.gui.title("FlowChat")
        # Defines what the "X"-Button does
        self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)
        # disallow window tearing
        self.gui.option_add('*tearOFF', FALSE)
        self.gui.geometry("630x440")
        # frame widget on which other widgets are placed
        # Menu bar
        self.menu_bar_main = Menu(self.gui)
        # Menu bar Main tab
        self.menu_bar_start = Menu(self.menu_bar_main, tearoff=0)
        self.menu_bar_start.add_cascade(label="upper")
        self.menu_bar_start.add_separator()
        self.menu_bar_start.add_command(label="Close", command=self.on_closing)
        # Menu bar Settings tab
        self.menu_bar_settings = Menu(self.menu_bar_main, tearoff=0)
        self.menu_bar_settings.add_cascade(label="Change Name", command=self.open_namechange_window)
        self.menu_bar_settings.add_separator()
        self.menu_bar_settings.add_command(label="lower")
        # Menu bar Help tab
        self.menu_bar_help = Menu(self.menu_bar_main, tearoff=0)
        self.menu_bar_help.add_cascade(label='About')

        self.menu_bar_main.add_cascade(label="Start", menu=self.menu_bar_start)
        self.menu_bar_main.add_cascade(label="Settings", menu=self.menu_bar_settings)
        self.menu_bar_main.add_cascade(label="Help", menu=self.menu_bar_help)
        self.gui.config(menu=self.menu_bar_main)
        # Grid configuration
        self.gui.columnconfigure(0, weight=3)
        self.gui.columnconfigure(1, weight=0)
        self.gui.rowconfigure(0, weight=3)
        self.gui.rowconfigure(1, weight=0, uniform="column")
        # Widget initialization
        self.widget_msg_box = CTkTextbox(master=self.gui, height=15, width=50,
                                         state="disabled")  # disabled first, so one can't write in the box
        self.widget_msg_box.grid(row=0, rowspan=1, column=0, columnspan=3, sticky="nsew")
        self.my_msg = StringVar()
        self.widget_entry_box = CTkEntry(master=self.gui, width=45, textvariable=self.my_msg)
        self.widget_entry_box.bind("<Return>", self.send)
        self.widget_entry_box.grid(row=2, column=0, sticky="ew")
        self.widget_button_send = CTkButton(self.gui, text="Send", command=self.send)
        self.widget_button_send.grid(row=2, column=1, columnspan=2)

        self.message_poll_state = True
        self.namechange_window = None

        # Recieve new messages as a new thread
        self.recv = threading.Thread(target=self.poll_for_new_messages)
        self.recv.start()

        # TODO: This is for Debug only: Chat window always on top
        self.gui.wm_attributes("-topmost", 1)
        # Start mainloop
        self.gui.mainloop()

    # defines what happens when you close the window
    def on_closing(self, *args):
        # confirmation box
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # closes Window
            self.gui.destroy()
            # closes sockets
            Network.networkmanager.on_closing()
            # stops all threads and shuts down the application on close
            os._exit(0)

    def open_namechange_window(self):
        if self.namechange_window is None or not self.namechange_window.winfo_exists():
            self.namechange_window = NameChangeWindow(self)
        else:
            self.namechange_window.focus()

    # sends message to other users and empties send box
    def send(self, *args):
        # sends the message to network, is also sent to networkmanager message_queue
        Network.networkmanager.send_message(self.widget_entry_box.get())
        # Deletes what you wrote in the entry-box
        self.widget_entry_box.delete(0, "end")

    # poll for new messages in networkmanager and push them to Chat box
    def poll_for_new_messages(self):
        while True:
            time.sleep(0.1)
            # In case new messages are found in the message_queue:
            if Network.networkmanager.message_queue:
                for messagepayload in Network.networkmanager.message_queue:
                    # Get message payload
                    payload = json.loads(messagepayload)
                    payloadtype = payload["type"]
                    if payloadtype == "message":
                        # format the payload to print as a readable message format
                        message = payload["date"] + payload["name"] + " : " + payload["message"] + "\n"

                        # make message box "state" "normal" to be editable
                        self.widget_msg_box.configure(state="normal")
                        # Push message to message box
                        self.widget_msg_box.insert("end", message)
                        # make message box "disabled" again to prevent manual editing
                        self.widget_msg_box.configure(state="disabled")
                        # remove message from message_queue
                        Network.networkmanager.message_queue.remove(messagepayload)
                    if payloadtype == "command":
                        print("@TODO Command")
                    # Scrolled automatisch zu einer neuen Nachricht
                    self.widget_msg_box.see("end")


g = Guimanager()  # Window is created as a new Object
