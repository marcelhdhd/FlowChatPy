import tkinter as tk
from tkinter import messagebox


def on_closing():           #What happens when pressing the "X"-Button
    if messagebox.askokcancel("Quit", "Do you want to quit?"):  #Asks if you really want to quit TODO: send meesege, that the user is leaving
        gui.destroy()   #Close

def send(event=None):               #For later: sends message to other users
    msg_box.insert(tk.END, my_msg.get())      #For now: places your message into the end of the message-box
    my_msg.set("")                            #Deletes what you wrote in the entry-box


gui = tk.Tk()   #Window is created as an instance of tk
gui.title("FlowChat")   #Titel of the window

gui.protocol("WM_DELETE_WINDOW", on_closing) #Defines what the "X"-Button does
#gui.mainloop()

messages_frame = tk.Frame(gui)  #Creates frame widget
my_msg = tk.StringVar()     #My message to be sent | StringVar() helps with entry | TODO: look into StringVar more

scrollbar = tk.Scrollbar(messages_frame)  #Creates a scrollbar to see past messages |TODO: autoscrolling
msg_box = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)    # Creates a box that contains the messeges
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    #Places the scrollbar to the right, stretching on the Y-axis
msg_box.pack(side=tk.LEFT)   #Places the messagebox to the left | TODO: look into stretching when making the window bigger

messages_frame.pack()       #Places the message-frame

entry_box = tk.Entry(gui, width=45, textvariable=my_msg)      #Creats a entry-box. What you write there becomes my_msg
entry_box.bind("<Return>", send)           #Starts send method when pressing enter
entry_box.pack(side=tk.LEFT)     #Places the entry-box on the left

send_button = tk.Button(gui,                #Creates send-button
                        text="Send",
                        command=send)
send_button.pack(side=tk.RIGHT)      #Places send-button to the right

gui.mainloop()      #Start
