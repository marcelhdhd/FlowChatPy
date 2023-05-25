import os
import sys

import gui.main_chatWIndow
import net.networkmanager

# todo: make FlowChat run in cli mode when called with '-c' argument
if len(sys.argv) == 1:
    # sys.argv[0] should be the name of the script, main.py
    print("Starting FlowChatPy in gui mode")
    is_GUI = True
elif (len(sys.argv) == 2 and (sys.argv[1] == "--gui" or sys.argv[1] == "-g")):
    print("Starting FlowChatPy in gui mode")
    is_GUI = True
elif (len(sys.argv) == 2 and (sys.argv[1] == "--cli" or sys.argv[1] == "-c")):
    print("Starting FlowChatPy in CLI mode")
    is_GUI = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    net.networkmanager
    gui.main_chatWIndow