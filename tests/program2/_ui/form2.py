# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1196, 636)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 30, 371, 211))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 181))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 3, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(400, 40, 251, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(9, 28, 52, 66))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_2 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_2.setMaximumSize(QtCore.QSize(50, 30))
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.textEdit_3 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_3.setMaximumSize(QtCore.QSize(50, 30))
        self.textEdit_3.setObjectName("textEdit_3")
        self.verticalLayout.addWidget(self.textEdit_3)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Hopefully a map"))
        self.pushButton.setText(_translate("Form", "Send path"))
        self.pushButton_2.setText(_translate("Form", "Delete all"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))