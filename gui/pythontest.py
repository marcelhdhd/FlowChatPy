# Form implementation generated from reading ui file 'changeNameWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication

from settings import settings


class ChangeNameWindow:

    def __init__(self):
        super().__init__()
        app = QApplication(sys.argv)

        self.dialog = QtWidgets.QDialog()

        self.font = QtGui.QFont()
        self.font.setPointSize(14)

        self.__loadButtons__()
        self.__loadTranslation__()

        self.dialog.show()

        app.exec()

    def __loadButtons__(self):
        print("load change name window buttons")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 461, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nickname_Input_field = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.nickname_Input_field.setObjectName("nickname_Input_field")
        self.verticalLayout.addWidget(self.nickname_Input_field)
        self.changeNameLabel = QtWidgets.QLabel(parent=self.dialog)
        self.changeNameLabel.setGeometry(QtCore.QRect(120, 20, 251, 21))
        self.changeNameLabel.setFont(self.font)
        self.changeNameLabel.setObjectName("changeNameLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 110, 481, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.clicked.connect(self.doChangeName)
        self.horizontalLayout.addWidget(self.ok_button)
        self.cancel_Button = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.cancel_Button.setObjectName("cancel_Button")
        self.horizontalLayout.addWidget(self.cancel_Button)

    def __loadTranslation__(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Namen eingeben"))
        self.changeNameLabel.setText(_translate("Dialog", "Enter your Nickname"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.cancel_Button.setText(_translate("Dialog", "cancel"))

    def doChangeName(self):
        userNameInput = self.nickname_Input_field.text()
        if userNameInput is None:
            return
        if len(userNameInput) == 0:
            return

        settings.user_name = userNameInput
        print("changed name to '" + userNameInput + "'")

        self.dialog.close()
