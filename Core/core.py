import fuser
import os
import threading
import time

from tkinter import *
from tkinter import messagebox
from datetime import datetime

import Network.networkmanager

user = fuser.FlowUser(Network.networkmanager.ip_finder(), "FlowUser")  # Test Constructor for the 'FlowUser'

print(user.ip)
print(user.name)


class ChangeNameGui:

    def __init__(self):
        self.container = Tk()

        self.container.title("Change name")
        self.container.geometry("300x200")


class CoreTestUI:
    def __init__(self):
        # Create Container
        self.container = Tk()
        # Setup container configuration
        self.container.title("FlowChat")
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.container.option_add('*tearOFF', FALSE)
        self.container.geometry("400x300")
        # Menu bar
        self.menu_bar_main = Menu(self.container)
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
        # Menu bar Others tab
        self.menu_bar_test2 = Menu(self.menu_bar_main)
        self.menu_bar_test2.add_cascade(label="test")
        self.menu_bar_test2.add_command(label="test2")

        self.menu_bar_main.add_cascade(label="Start", menu=self.menu_bar_start)
        self.menu_bar_main.add_cascade(label="Settings", menu=self.menu_bar_settings)
        self.menu_bar_main.add_cascade(label="test2", menu=self.menu_bar_test2)
        self.menu_bar_main.add_command(label="Close", command=self.on_closing)

        self.container.config(menu=self.menu_bar_main)
        # Grid configuration
        self.container.columnconfigure(0, weight=3)
        self.container.columnconfigure(1, weight=0)
        self.container.rowconfigure(0, weight=3)
        self.container.rowconfigure(1, weight=0, uniform="column")
        # Widget initialization
        self.widget_scrollbar = Scrollbar(self.container)
        self.widget_scrollbar.grid(sticky="nesw")
        self.widget_msg_box = Listbox(self.container, height=15, width=50, yscrollcommand=self.widget_scrollbar.set)
        self.widget_msg_box.grid(row=0, rowspan=1, column=0, columnspan=1, sticky="nsew")

        self.widget_my_msg = StringVar()
        self.widget_entry_box = Entry(self.container, width=45, textvariable=self.widget_my_msg)
        self.widget_entry_box.bind("<Return>", self.do_send)
        self.widget_entry_box.grid(row=1, column=0, sticky="ew")
        self.widget_button_send = Button(self.container, text="Send", command=self.do_send)
        self.widget_button_send.grid(row=1, column=1)

        self.message_poll_state = True

        # Recieve new messages as a new thread
        self.recv = threading.Thread(target=self.poll_for_new_messages)
        self.recv.start()
        # Start mainloop
        self.container.mainloop()

    def on_closing(self, *args):
        # Asks if you really want to quit TODO: send message, that the user is leaving
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close
            self.container.destroy()
            self.message_poll_state = False
            Network.networkmanager.on_closing()
            os._exit(0)

    def do_send(self, *args):
        if len(args) == 0:
            return
        # Deletes what you wrote in the entry-box
        Network.networkmanager.send_message(self.widget_my_msg.get())
        self.widget_my_msg.set("")

    def poll_for_new_messages(self):
        while self.message_poll_state:
            if not self.message_poll_state:
                break
            time.sleep(0.1)
            if Network.networkmanager.message_queue:
                for tuplemsg in Network.networkmanager.message_queue:
                    ip, msg = tuplemsg
                    current_time = datetime.now().strftime("[%H:%M:%S] ")
                    message = current_time + ip + " : " + msg
                    self.widget_msg_box.insert(END, message)
                    Network.networkmanager.message_queue.remove(tuplemsg)
                    # Scrolled automatisch zu einer neuen Nachricht
                    self.widget_msg_box.see("end")


test = CoreTestUI()
