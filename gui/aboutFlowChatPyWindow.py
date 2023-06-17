from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLabel


class AboutWindow:

    def __init__(self):
        super().__init__()

        self.dialog = QDialog()

        self.dialog.resize(500, 400)

        self.font = QFont()
        self.font.setPointSize(12)

        self.__loadWidgets__()
        self.__loadText__()

        self.dialog.show()

    def __loadWidgets__(self):
        print("load about window widgets")
        self.textLabel = QLabel(parent=self.dialog)
        self.textLabel.setFont(self.font)
        self.textLabel.setObjectName("textLabel")

    def __loadText__(self):
        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "About FlowChatPy"))
        self.textLabel.setText(_translate("Dialog", "FlowChatPy ist ein LAN-Chat Programm, mit Hilfe dessen \n"
                                                          "alle Personen im gleichen Netzwerk problemlos miteinander \n"
                                                          "chatten können"))
