# Form implementation generated from reading ui file 'main_chatWIndow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import threading
import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLineEdit

import Network.networkmanager


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 675)
        MainWindow.setMinimumSize(QtCore.QSize(838, 0))
        MainWindow.setMaximumSize(QtCore.QSize(4048, 4048))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.userChat = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.userChat.setObjectName("userChat")
        self.gridLayout.addWidget(self.userChat, 1, 0, 1, 2)
        self.chatButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.chatButton.setAutoDefault(True)
        self.chatButton.setObjectName("chatButton")
        self.gridLayout.addWidget(self.chatButton, 1, 2, 1, 1)
        self.userList = QtWidgets.QListView(parent=self.centralwidget)
        self.userList.setObjectName("userList")
        self.gridLayout.addWidget(self.userList, 0, 1, 1, 2)
        self.chatBox = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.chatBox.setObjectName("chatBox")
        self.gridLayout.addWidget(self.chatBox, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1026, 26))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtWidgets.QMenu(parent=self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuEinstellung = QtWidgets.QMenu(parent=self.menubar)
        self.menuEinstellung.setObjectName("menuEinstellung")
        self.menuBeenden = QtWidgets.QMenu(parent=self.menubar)
        self.menuBeenden.setObjectName("menuBeenden")
        self.menuAnsicht = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnsicht.setObjectName("menuAnsicht")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.changeName = QtGui.QAction(parent=MainWindow)
        self.changeName.setObjectName("changeName")
        self.focusWindow = QtGui.QAction(parent=MainWindow)
        self.focusWindow.setCheckable(True)
        self.focusWindow.setObjectName("focusWindow")
        self.darkMode = QtGui.QAction(parent=MainWindow)
        self.darkMode.setCheckable(True)
        self.darkMode.setObjectName("darkMode")
        self.menuEinstellung.addAction(self.changeName)
        self.menuAnsicht.addAction(self.focusWindow)
        self.menuAnsicht.addAction(self.darkMode)
        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menubar.addAction(self.menuEinstellung.menuAction())
        self.menubar.addAction(self.menuBeenden.menuAction())
        self.chatButton.clicked.connect(self.send)
        self.userChat.returnPressed.connect(self.send)
        self.retranslateUi(MainWindow)
        self.recv = threading.Thread(target=self.poll_for_new_messages)
        self.recv.start()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FlowChatPy"))
        self.chatButton.setText(_translate("MainWindow", "Senden"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menuEinstellung.setTitle(_translate("MainWindow", "Einstellung"))
        self.menuBeenden.setTitle(_translate("MainWindow", "Beenden"))
        self.menuAnsicht.setTitle(_translate("MainWindow", "Ansicht"))
        self.changeName.setText(_translate("MainWindow", "Namen ändern"))
        self.focusWindow.setText(_translate("MainWindow", "Fenster Fokusieren"))
        self.darkMode.setText(_translate("MainWindow", "Dunkel Ansicht"))

    def send(self, *args):
        Network.networkmanager.send_message(self.userChat.text())
        self.userChat.setText("")

    def poll_for_new_messages(self):
        while True:
            time.sleep(0.1)
            # In case new messages are found in the message_queue:
            if Network.networkmanager.message_queue:
                for messagepayload in Network.networkmanager.message_queue:
                    # Get message payload
                    payload = json.loads(messagepayload)
                    if "type" in payload is None:
                        continue

                    payloadtype = payload["type"]
                    message = None

                    if payloadtype == "customMessage":
                        message = payload["message"] + "\n"

                    if payloadtype == "userMessage":
                        # format the payload to print as a readable message format
                        message = payload["date"] + payload["name"] + " : " + payload["message"] + "\n"

                    if message is not None:
                        # make message box "state" "normal" to be editable
                        self.chatBox.insertPlainText( message)
                        # remove message from message_queue
                        Network.networkmanager.message_queue.remove(messagepayload)

                    if payloadtype == "command":
                        print("@TODO Command")
                    # Scrolled automatisch zu einer neuen Nachricht

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
