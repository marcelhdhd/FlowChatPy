# Form implementation generated from reading ui file 'main_chatWIndow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import os
import threading
import time

from PyQt6.QtCore import Qt, QSize, QRect, QMetaObject, QCoreApplication
from PyQt6.QtGui import QAction, QPalette, QColor, QTextCursor, QIcon
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow, QGridLayout, QLineEdit, QListView, \
    QPushButton, QTextBrowser, QMenuBar, QMenu

import net.networkmanager
from gui import changeNameWindow, aboutFlowChatPyWindow
from net import networkmanager
from settings import settings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(ROOT_DIR, 'icon.ico')


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(ICON_PATH))
        MainWindow.setWindowIcon(QIcon(ICON_PATH))
        networkmanager.run_daemon()

    def setupUi(self, MainWindow):
        self.setWindowIcon(QIcon(ICON_PATH))
        MainWindow.setWindowIcon(QIcon(ICON_PATH))
        # MainWindow Object
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 675)
        MainWindow.setMinimumSize(QSize(838, 0))
        MainWindow.setMaximumSize(QSize(4048, 4048))
        MainWindow.closeEvent = self.closeEvent

        # Centralwidget Object
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # GridLayout Object
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # UserChat Object    -   The inputbar
        self.userChat = QLineEdit(parent=self.centralwidget)
        self.userChat.setObjectName("userChat")
        self.gridLayout.addWidget(self.userChat, 1, 0, 1, 2)
        self.userChat.returnPressed.connect(self.send)

        # Chatbutton Object  -   The Send-Button
        self.chatButton = QPushButton(parent=self.centralwidget)
        self.chatButton.setAutoDefault(True)
        self.chatButton.setObjectName("chatButton")
        self.gridLayout.addWidget(self.chatButton, 1, 2, 1, 1)
        self.chatButton.clicked.connect(self.send)

        # Userlist Object    -   The List of all users
        self.userList = QListView(parent=self.centralwidget)
        self.userList.setObjectName("userList")
        self.gridLayout.addWidget(self.userList, 0, 1, 1, 2)

        # Chatbox Object     -   The Chatwindow
        self.chatBox = QTextBrowser(parent=self.centralwidget)
        self.chatBox.setObjectName("chatBox")
        self.gridLayout.addWidget(self.chatBox, 0, 0, 1, 1)

        # Menubar Object     -   A Menubar with Objects "Einstellungen", "Beenden" and "Help"
        self.menubar = QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1026, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # Einstellungen
        self.menuEinstellungen = QMenu(parent=self.menubar)
        self.menuEinstellungen.setObjectName("menuEinstellungen")
        self.menubar.addAction(self.menuEinstellungen.menuAction())
        # Beenden
        self.menuBeenden = QAction(parent=self.menubar)
        self.menuBeenden.setObjectName("menuBeenden")
        self.menuBeenden.triggered.connect(self.close)
        self.menubar.addAction(self.menuBeenden)
        # Help
        self.menuHilfe = QMenu(parent=self.menubar)
        self.menuHilfe.setObjectName("menuHilfe")
        self.menubar.addAction(self.menuHilfe.menuAction())

        # Changename Object  -   A Button in "Einstellungen"-Object
        self.changeName = QAction(parent=MainWindow)
        self.changeName.setObjectName("changeName")
        self.changeName.triggered.connect(self.openNameChangeWindow)
        self.menuEinstellungen.addAction(self.changeName)

        # About_FlowChatPi Object    -   A Button in "Einstellungen"-Object
        self.action_about_FlowChatPy = QAction(parent=MainWindow)
        self.action_about_FlowChatPy.setObjectName("action_ber_FlowChatPy")
        self.action_about_FlowChatPy.triggered.connect(self.openAboutWindow)
        self.menuHilfe.addAction(self.action_about_FlowChatPy)

        # FensterFokusieren Object  -   A Button in "Einstellungen"-Object
        self.actionFenster_Fokusieren = QAction(parent=MainWindow)
        self.actionFenster_Fokusieren.setCheckable(True)
        self.actionFenster_Fokusieren.setObjectName("actionFenster_Fokusieren")
        self.actionFenster_Fokusieren.triggered.connect(self.change_always_on_top)
        self.menuEinstellungen.addAction(self.actionFenster_Fokusieren)

        # Dunkle_Ansicht Object  -   A Button in "Einstellungen"-Object to change the color theme
        self.actionDunkle_Ansicht = QAction(parent=MainWindow)
        self.actionDunkle_Ansicht.setCheckable(True)
        self.actionDunkle_Ansicht.setObjectName("darkMode")
        self.actionDunkle_Ansicht.triggered.connect(self.change_theme)
        self.menuEinstellungen.addAction(self.actionDunkle_Ansicht)

        self.retranslateUi(MainWindow)

        self.change_theme_color()

        self.recv = threading.Thread(target=self.poll_for_new_messages)
        self.recv.start()
        QMetaObject.connectSlotsByName(MainWindow)

    # defines what happens when you close the window
    def closeEvent(self, event):
        qmsgbox = QMessageBox()
        reply = qmsgbox.question(MainWindow, "Beenden", "Willst du FlowChatPy wirklich beenden?",
                                 qmsgbox.standardButtons().Yes, qmsgbox.standardButtons().No)
        # confirmation box
        if reply == qmsgbox.standardButtons().Yes:
            event.accept()
            # closes sockets
            net.networkmanager.on_closing()
            # stops all threads and shuts down the application on close
            os._exit(0)
        else:
            event.ignore()

    def openNameChangeWindow(self):
        self.changeNameWindow = changeNameWindow.ChangeNameWindow()

    def openAboutWindow(self):
        self.aboutWindow = aboutFlowChatPyWindow.AboutWindow()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FlowChatPy"))
        self.chatButton.setText(_translate("MainWindow", "Senden"))
        self.menuEinstellungen.setTitle(_translate("MainWindow", "Einstellungen"))
        self.menuBeenden.setText(_translate("MainWindow", "Beenden"))
        self.menuHilfe.setTitle(_translate("MainWindow", "Hilfe"))
        self.changeName.setText(_translate("MainWindow", "Namen ändern"))
        self.actionFenster_Fokusieren.setText(_translate("MainWindow", "Fenster fokussieren"))
        self.actionDunkle_Ansicht.setText(_translate("MainWindow", "Darkmode"))
        self.action_about_FlowChatPy.setText(_translate("MainWindow", "Über FlowChatPy"))

    def send(self, *args):
        net.networkmanager.send_message(self.userChat.text())
        self.userChat.setText("")

    def change_theme(self, changedSettings):
        if self.actionDunkle_Ansicht.isChecked():
            settings.settingsInstance.dark_mode = True
        else:
            settings.settingsInstance.dark_mode = False
        settings.settingsInstance.save()
        self.change_theme_color()

    def change_always_on_top(self):
        if self.actionFenster_Fokusieren.isChecked():
            settings.settingsInstance.focus_window = True
        else:
            settings.settingsInstance.focus_window = False
        settings.settingsInstance.save()
        self.change_focus()

    def change_focus(self):
        if settings.settingsInstance.focus_window:
            MainWindow.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        else:
            MainWindow.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        MainWindow.show()

    def change_theme_color(self):
        palette = QPalette()
        if settings.settingsInstance.dark_mode:
            palette.setColor(QPalette.ColorRole.Window, QColor(48, 48, 45))
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 0))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        else:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.lightGray)
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        app.setPalette(palette)

    def poll_for_new_messages(self):
        while True:
            time.sleep(0.1)
            # In case new messages are found in the message_queue:
            if net.networkmanager.message_queue:
                for messagepayload in net.networkmanager.message_queue:
                    # Get message payload
                    payload = json.loads(messagepayload)
                    if "type" in payload is None:
                        continue

                    payloadtype = payload["type"]
                    message = None

                    if payloadtype == "customMessage":
                        message = payload["message"]

                    if payloadtype == "userMessage":
                        # format the payload to print as a readable message format
                        message = payload["date"] + payload["name"] + " : " + payload["message"]

                    if message is not None and payload["message"] != "":
                        self.chatBox.append(message)
                        # Scrolled automatisch zu einer neuen Nachricht
                        self.chatBox.moveCursor(QTextCursor.MoveOperation.End)

                    # remove message from message_queue
                    net.networkmanager.message_queue.remove(messagepayload)

                    if payloadtype == "command":
                        print("@TODO Command")


import sys

print("Icon Path: ")
print(ICON_PATH)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(ICON_PATH))
MainWindow = QMainWindow()
MainWindow.setWindowIcon(QIcon(ICON_PATH))
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())
