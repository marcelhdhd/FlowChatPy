import json
import os
import threading
import time
from tkinter import *
from tkinter import messagebox

import Network.networkmanager


# In-depth tutorial for tkinter
# https://tkdocs.com/tutorial/onepage.html


class Guimanager:

    # the following code defines the chat window in its entirety# #
    def __init__(self):

        # Chat Window
        self.gui = Tk()
        ##################################
        # Here is the window initialized #
        ##################################
        # Title of the window
        self.gui.title("FlowChat")
        # Defines what the "X"-Button does
        self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)
        # disallow window tearing
        self.gui.option_add('*tearOFF', FALSE)
        self.gui.geometry("400x300")
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
        self.menu_bar_settings.add_cascade(label="Change Name")
        self.menu_bar_settings.add_separator()
        self.menu_bar_settings.add_command(label="lower")

        self.menu_bar_main.add_cascade(label="Start", menu=self.menu_bar_start)
        self.menu_bar_main.add_cascade(label="Settings", menu=self.menu_bar_settings)

        self.gui.config(menu=self.menu_bar_main)

        # Grid configuration
        self.gui.columnconfigure(0, weight=3)
        self.gui.columnconfigure(1, weight=0)
        self.gui.rowconfigure(0, weight=3)
        self.gui.rowconfigure(1, weight=0, uniform="column")
        # Widget initialization
        self.widget_msg_box = Listbox(self.gui, height=15, width=50)
        self.widget_msg_box.grid(row=0, rowspan=1, column=0, columnspan=1, sticky="nsew")
        self.widget_scrollbar = Scrollbar(self.gui, command=self.widget_msg_box.yview)
        self.widget_scrollbar.grid(row=0, column=1, sticky="nesw")
        self.widget_scrollbar_bottom = Scrollbar(self.gui, orient='horizontal', command=self.widget_msg_box.xview)
        self.widget_scrollbar_bottom.grid(row=1, column=0, sticky="nesw")
        self.widget_msg_box.config(yscrollcommand=self.widget_scrollbar.set,
                                   xscrollcommand=self.widget_scrollbar_bottom.set)

        self.widget_my_msg = StringVar()
        self.widget_entry_box = Entry(self.gui, width=45, textvariable=self.widget_my_msg)
        self.widget_entry_box.bind("<Return>", self.send)
        self.widget_entry_box.grid(row=2, column=0, sticky="ew")
        self.widget_button_send = Button(self.gui, text="Send", command=self.send)
        self.widget_button_send.grid(row=2, column=1, columnspan=2)

        self.message_poll_state = True

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

    # sends message to other users and empties send box
    def send(self, *args):
        # sends the message to network, is also sent to networkmanager message_queue
        Network.networkmanager.send_message(self.widget_my_msg.get())
        # Deletes what you wrote in the entry-box
        self.widget_my_msg.set("")

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
                        message = payload["date"] + payload["name"] + " : " + payload["message"]
                        # Push message to message box
                        self.widget_msg_box.insert(END, message)
                        # remove message from message_queue
                        Network.networkmanager.message_queue.remove(messagepayload)
                    if payloadtype == "command":
                        print("@TODO Command")
                    # Scrolled automatisch zu einer neuen Nachricht
                    self.widget_msg_box.see("end")


g = Guimanager()  # Window is created as a new Object
