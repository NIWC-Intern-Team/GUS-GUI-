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


class _Group1(QGroupBox):
    def __init__(self) -> None:
        super().__init__("hopefully a map")
        # self.setGeometry(100, 100, 800, 600)

        # Widgets        
        map_group = QGroupBox("Map & Features")
        group_push = QGroupBox("Push Button")

        push_btn_send, push_btn_delete = QPushButton("Send waypoints"), QPushButton("Delete all waypoints")


        # Setup widgets
        # self.setCheckable(True)
        # for btn in (push_btn_toggled, ):
        #     btn.setCheckable(True)
        #     btn.setChecked(True)
            
            
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
        # self.view.setMaximumSize(100,100)
        
        # Layout setup
        g_map = QGridLayout()

        # Add the view to take up most of the space
        g_map.addWidget(self.view, 1, 0, 1, 3)  # Span across columns if needed

        # Add buttons at the top
        g_map.addWidget(push_btn_send, 0, 0)  # First row, second column
        g_map.addWidget(push_btn_delete, 0, 1)  # First row, third column

        self.setLayout(g_map)




class _Group2(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Diagnostic Panel")

        # Create Readout group boxes
        groupR1 = QGroupBox("Readout 1")
        groupR2 = QGroupBox("Readout 2")

        # Create tab widget for errors and warnings directly
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

        # Layout for readout groups
        v_layout_r1 = QVBoxLayout(groupR1)
        v_layout_r2 = QVBoxLayout(groupR2)
        label1 = QLabel("Information about Readout 1")
        label2 = QLabel("Information about Readout 2")
        v_layout_r1.addWidget(label1)
        v_layout_r2.addWidget(label2)

        # Main grid layout setup
        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(groupR1, 0, 0,1,2)
        g_layout_main.addWidget(groupR2, 1, 0,1,2)
        g_layout_main.addWidget(tab_widget, 0, 2, 2, 1)  # Span two rows for tab widget

        # Configure column stretch factors
        g_layout_main.setColumnStretch(0, 1)
        g_layout_main.setColumnStretch(1, 1)
        g_layout_main.setColumnStretch(2, 2)  # Give more space to the tab widget


class _Group3(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Camera Feeds")
        
        # ip address handling?
        
        # Widgets
        groupL = QGroupBox("Left")
        groupR = QGroupBox("Right")
        groupF = QGroupBox("Fire on Ice")
        groupA = QGroupBox("Angela Merkel")

        # Setup widgets


        # Layout
        v_layout_line_edit1 = QVBoxLayout()

        groupL.setLayout(v_layout_line_edit1)

        v_layout_line_edit2 = QVBoxLayout()

        groupR.setLayout(v_layout_line_edit2)

        v_layout_line_edit3 = QVBoxLayout()

        groupF.setLayout(v_layout_line_edit3)

        v_layout_line_edit4 = QVBoxLayout()

        groupA.setLayout(v_layout_line_edit4)


        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(groupL, 0, 0)
        g_layout_main.addWidget(groupR, 0, 1)
        g_layout_main.addWidget(groupF, 1, 0)
        g_layout_main.addWidget(groupA, 1, 1)
        
        g_layout_main.setColumnMinimumWidth(0, 100)
        g_layout_main.setColumnMinimumWidth(1, 100)
        
class singUI:
    """The ui class of widgets window. nice :-D"""

    def setup_ui(self, win: QWidget) -> None:
        """Set up ui."""
        """Set up ui."""
        # Widgets
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal)
        # Setup widgets
        h_splitter_1.setMinimumHeight(350)  # Fix bug layout crush

        # Layout
        h_splitter_1.addWidget(_Group1())
        right_splitter = QSplitter(Qt.Vertical)

        right_splitter.addWidget(_Group2())
        right_splitter.addWidget(_Group3()) # additional Groups for more information 
        # h_splitter_2.addWidget(_Group4())

        h_splitter_1.addWidget(right_splitter)

        widget_container = QWidget()
        
    # Set the main layout
        main_layout = QVBoxLayout(win)
        main_layout.addWidget(h_splitter_1)
        win.setLayout(main_layout)
        h_splitter_1.setStretchFactor(0, 1)  # Group1 takes less space
        h_splitter_1.setStretchFactor(1, 2)  # Vertical splitter takes more space

        # Adjust splitter sizes dynamically
        h_splitter_1.setSizes([200, 300])  # Adjust initial sizes as needed
        h_splitter_1.setSizes([150, 150])  # Equal initial sizes for vertical sections
