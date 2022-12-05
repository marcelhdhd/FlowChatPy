from tkinter import *
from tkinter import messagebox
from datetime import datetime


# In-depth tutorial for tkinter
# https://tkdocs.com/tutorial/onepage.html


class Guimanager:

    def __init__(self, gui):

        ##################################
        # Here is the window initialized #
        ##################################
        # Titel of the window
        gui.title("FlowChat")
        # Defines what the "X"-Button does
        gui.protocol("WM_DELETE_WINDOW", self.on_closing)
        # frame widget on which other widgets are placed
        self.messages_frame = Frame(gui)
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
        self.entry_box = Entry(gui, width=45, textvariable=self.my_msg)
        # send-button
        self.send_button = Button(gui, text="Send", command=self.send)
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
        self.entry_box.bind("<Return>", gui.send)
        # Places the entry-box on the left
        self.entry_box.pack(side=LEFT)
        # Places send-button to the right
        self.send_button.pack(side=RIGHT)

    # Manages pressing the "X"-Button
    def on_closing(self, *args):
        # Asks if you really want to quit TODO: send meesege, that the user is leaving
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close
            gui.destroy()

    # For later: sends message to other users
    # For now: places your message into the end of the message-box
    def send(self, *args):
        # Get a datetime object to retrieve current time from
        now = datetime.now()
        # Ready the String to be put into the msg_box TODO: also add username
        current_time = now.strftime("[%H:%M:%S]: ")
        message = current_time + self.my_msg.get()
        # Insert the message into the box
        self.msg_box.insert(END, message)
        # Deletes what you wrote in the entry-box
        self.my_msg.set("")


gui = Tk()          # Window is created as an instance of tk
Guimanager(gui)     # Encapsulated main code into a class
gui.mainloop()      # Start
