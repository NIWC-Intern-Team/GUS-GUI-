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

# Map Widget
class _Group1(QGroupBox):
    def __init__(self) -> None:
        super().__init__("hopefully a map")
        # self.setGeometry(100, 100, 800, 600)

        # Widgets        
        map_group = QGroupBox("Map & Features")
        group_push = QGroupBox("Push Button")

        push_btn_send, push_btn_delete = QPushButton("Send waypoints"), QPushButton("Delete all waypoints")
            
            
        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.setMinimumSize(300, 400)
        

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
     
 
        # Layout setup
        g_map = QGridLayout()

        # Add the view to take up most of the space
        g_map.addWidget(self.view, 1, 0, 1, 3)  

        # Add the error tab to the bottom 
      #  g_map.addWidget(tab_widget, 2, 0, 1, 3)  

        self.setLayout(g_map)

# All GUS overview
class _Group2(QGroupBox):
    def __init__(self) -> None:
        super().__init__("All Gus Connections")

        groupR1 = QGroupBox("Gus Overview")

        v_layout_r1 = QVBoxLayout(groupR1)

        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(groupR1, 0, 0)

# Warning and Error Widget
class _Group3(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Terminal")

        # self.view.setMaximumSize(100,100)
        tab_widget = QTabWidget()
        tab_errors = QWidget()
        tab_warnings = QWidget()

        # Add text areas for errors and warnings
        errors_text_edit = QTextEdit()
        warnings_text_edit = QTextEdit()

        # Layouts for tabs
        errors_layout = QVBoxLayout()
        errors_layout.addWidget(errors_text_edit)
        tab_errors.setLayout(errors_layout)

        warnings_layout = QVBoxLayout()
        warnings_layout.addWidget(warnings_text_edit)
        tab_warnings.setLayout(warnings_layout)

        # Add tabs to the tab widget
        tab_widget.addTab(tab_errors, "Errors")
        tab_widget.addTab(tab_warnings, "Warnings")

        g_error_layout = QGridLayout()
        g_error_layout.addWidget(tab_widget, 2, 0, 1, 3)  
        self.setLayout(g_error_layout)

class allUI:
    """The ui class of All widgets window. nice :-D"""

    def setup_ui(self, win: QWidget,  csv_handler, tab) -> None:
        """Set up ui."""
        self.group1 = _Group1()

        # Widgets
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal) # Creates left and right side to resize horizontally
        # Setup widgets
        h_splitter_1.setMinimumHeight(350)  # Fix bug layout crush

        # Layout
        self.left_splitter = QSplitter(Qt.Vertical) # Creates left stack of widgets to resize vertically
        self.left_splitter.addWidget(_Group1())
        self.left_splitter.addWidget(_Group3())

        # Adds vertical left widgets and the right widget to be able to resize horizontally
        h_splitter_1.addWidget(self.left_splitter)
        h_splitter_1.addWidget(_Group2())

        widget_container = QWidget()
        
        # Set the main layout
        main_layout = QVBoxLayout(win)
        main_layout.addWidget(h_splitter_1)
        win.setLayout(main_layout)

        # Adjust splitter sizes dynamically
        h_splitter_1.setStretchFactor(1, 2)  # Vertical splitter takes more space

        h_splitter_1.setSizes([150, 150])  # Equal initial sizes for vertical sections