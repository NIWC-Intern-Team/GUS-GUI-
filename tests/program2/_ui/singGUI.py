from __future__ import annotations

import sys
import os 
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QJsonValue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGroupBox, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel

from PyQt5 import uic
from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel, QTextOption
from PyQt5.QtWidgets import (
    QCheckBox,
    QColumnView,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableView,
    QTabWidget,
    QTextEdit,
    QToolBox,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)
from PyQt5 import QtCore, QtGui, QtWidgets

# JS access to PyQt backend 
class Backend(QObject):
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        print(f"Latitude: {lat}, Longitude: {lng}")

# Used to override JS message method to enable data transfer bewteen frontend & backend
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")


class Ui_MainWindow():
    def setupUi(self, win: QWidget):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(6, 6, 391, 301))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 30, 361, 241))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 342, 216))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.layoutWidget)
        
        
        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        
        # Setup path to map.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 2nd parameter (between current_dir & map.html) can be set to subdir within parent for access to map.html
        html_path = os.path.join(current_dir, 'static', 'map.html') 
        self.view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up QWebChannel for communication
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)
        
        
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.view, 0, 0, 3, 1)
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WWWW"))
        self.groupBox.setTitle(_translate("MainWindow", "Hopefully a map"))
        self.pushButton.setText(_translate("MainWindow", "Send path"))
        self.pushButton_2.setText(_translate("MainWindow", "Delete all"))
