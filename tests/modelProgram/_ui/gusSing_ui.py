from __future__ import annotations

import sys
import os 
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QJsonValue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGroupBox, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel


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


class _Group1(QGroupBox):
    def __init__(self) -> None:
        super().__init__("hopefully a map")
        # self.setGeometry(100, 100, 800, 600)

        # Widgets
        group_push = QGroupBox()




        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        
        # Setup path to map.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 2nd parameter (between current_dir & map.html) can be set to subdir within parent for access to map.html
        html_path = os.path.join(current_dir, 'templates', 'map.html') 
        self.view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up QWebChannel for communication
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)
        
        
        
        # Layout
        g_map = QGridLayout()
        g_map.addWidget(self.view, 0, 0)
        self.setLayout(g_map)






class singUI:
    """The ui class of widgets window. nice :-D"""

    def setup_ui(self, win: QWidget) -> None:
        """Set up ui."""
        # Widgets
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal)

        # Setup widgets
        group1 = _Group1()
        h_splitter_1.addWidget(group1)
        # h_splitter_1.setStretchFactor(0, 1)  # Make the first widget (group1) stretch more

        v_main_layout = QVBoxLayout(win)
        v_main_layout.addWidget(h_splitter_1)