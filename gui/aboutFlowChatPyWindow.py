from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout
import os


class AboutWindow:

    def __init__(self):
        super().__init__()
        self.dialog = QDialog()

        self.dialog.resize(500, 400)

        self.font = QFont()
        self.font.setPointSize(12)

        self.__loadWidgets__()
        self.__loadText__()

        self.dialog.setLayout(self.layout)
        self.dialog.show()

    def __loadWidgets__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(root_dir, 'icon.png')

        print("loading about window widgets")
        self.layout = QVBoxLayout()

        self.iconLabel = QLabel(parent=self.dialog)
        icon_pixmap = QPixmap(icon_path)
        self.iconLabel.setPixmap(icon_pixmap.scaledToHeight(256))
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.iconLabel)

        self.textLabel = QLabel(parent=self.dialog)
        self.textLabel.setFont(self.font)
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setObjectName("textLabel")
        self.layout.addWidget(self.textLabel)

    def __loadText__(self):
        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "About FlowChatPy"))
        self.textLabel.setText(_translate("Dialog", "FlowChatPy ist ein LAN-Chat Programm, mit Hilfe dessen \n"
                                                    "alle Personen im gleichen Netzwerk problemlos miteinander \n"
                                                    "chatten können.\n\n"
                                                    "©2023 Julian Röder, Jonas Hormeß, Pascal Mika, Marcel Popp, "
                                                    "Max Kratzer\nv1.0"))
