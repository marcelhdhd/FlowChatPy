# Form implementation generated from reading ui file 'changeNameWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

import Network.networkmanager
import main_chatWIndow


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(482, 155)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 461, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nickname_Input_field = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.nickname_Input_field.setObjectName("nickname_Input_field")
        self.verticalLayout.addWidget(self.nickname_Input_field)
        self.changeNameLabel = QtWidgets.QLabel(parent=Dialog)
        self.changeNameLabel.setGeometry(QtCore.QRect(120, 20, 251, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.changeNameLabel.setFont(font)
        self.changeNameLabel.setObjectName("changeNameLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 110, 481, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.clicked.connect(self.changeName)
        self.horizontalLayout.addWidget(self.ok_button)
        self.cancel_Button = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.cancel_Button.setObjectName("cancel_Button")
        self.horizontalLayout.addWidget(self.cancel_Button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Namen eingeben"))
        self.changeNameLabel.setText(_translate("Dialog", "Enter your Nickname"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.cancel_Button.setText(_translate("Dialog", "cancel"))

    def changeName(self):
        Network.networkmanager.username = self.nickname_Input_field.text()
        Dialog = QtWidgets.QDialog()
        newwindow = main_chatWIndow.Ui_MainWindow()
        ui = newwindow
        ui.setupUi(Dialog)
        self.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
