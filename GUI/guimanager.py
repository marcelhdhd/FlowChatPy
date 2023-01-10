import os
import threading
import time
from tkinter import *
from tkinter import messagebox
from datetime import datetime

import Network.networkmanager


# In-depth tutorial for tkinter
# https://tkdocs.com/tutorial/onepage.html


class Guimanager:

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
        # frame widget on which other widgets are placed
        self.messages_frame = Frame(self.gui)
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        # Here are all widgets defined#
        ###############################
        # scrollbar to scroll to past messages |TODO: autoscrolling
        self.scrollbar = Scrollbar(self.messages_frame)

        # message to be sent | StringVar() helps with entry | TODO: look into StringVar more
        self.my_msg = StringVar()
        # message-box
        self.msg_box = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        # entry-box. What you write there becomes my_msg
        self.entry_box = Entry(self.gui, width=45, textvariable=self.my_msg)
        # send-button
        self.send_button = Button(self.gui, text="Send", command=self.send)
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        # Here are all widgets placed #
        ###############################
        # Places the scrollbar to the right, stretching on the Y-axis
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # Places the messagebox to the left | TODO: look into stretching when making the window bigger
        self.msg_box.pack(side=LEFT)

        # Places the message-frame
        self.messages_frame.pack()

        # Binds send method to pressing enter
        self.entry_box.bind("<Return>", self.send)
        # Places the entry-box on the left
        self.entry_box.pack(side=LEFT)
        # Places send-button to the right
        self.send_button.pack(side=RIGHT)

        # Recieve new messages as a new thread
        recv = threading.Thread(target=self.poll_for_new_messages)
        recv.start()
        # Start mainloop
        self.gui.mainloop()

    # Manages pressing the "X"-Button
    def on_closing(self, *args):
        # Asks if you really want to quit TODO: send message, that the user is leaving
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close
            self.gui.destroy()
            Network.networkmanager.on_closing()
            os._exit(0)

    # sends message to other users and empties send box
    def send(self, *args):
        # sends the message to network, is also sent to networkmanager message_queue
        Network.networkmanager.send_message(self.my_msg.get())
        # Deletes what you wrote in the entry-box
        self.my_msg.set("")

    # poll for new messages in networkmanager and push them to Chat box
    def poll_for_new_messages(self):
        while True:
            time.sleep(0.1)
            if Network.networkmanager.message_queue:
                for tuplemsg in Network.networkmanager.message_queue:
                    self.ip, self.msg = tuplemsg
                    self.current_time = datetime.now().strftime("[%H:%M:%S] ")
                    self.message = self.current_time + self.ip + " : " + self.msg
                    self.msg_box.insert(END, self.message)
                    Network.networkmanager.message_queue.remove(tuplemsg)
                    # Scrolled automatisch zu einer neuen Nachricht
                    self.msg_box.see("end")


g = Guimanager()          # Window is created as a new Object
