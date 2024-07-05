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
    QSizePolicy
)


from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import random 

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
    def __init__(self, csv_handler) -> None:
        super().__init__("hopefully a map")
        # self.setGeometry(100, 100, 800, 600)
        csv_handler.print_data()
        # lat = csv_handler.self.dataframes
        

        # Widgets        
        map_group = QGroupBox("Map & Features")
        group_push = QGroupBox("Push Button")

        push_btn_send, push_btn_delete = QPushButton("Send waypoints"), QPushButton("Delete all waypoints")
            
            
        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        # self.view.setMinimumSize(300, 400)

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
        g_map.addWidget(self.view, 1, 0, 1, 3)  

        # Add buttons at the top
        g_map.addWidget(push_btn_send, 0, 0)  # First row, second column
        g_map.addWidget(push_btn_delete, 0, 1)  # First row, third column

        self.setLayout(g_map)
        
class _Group2(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Terminal")
        # self.setGeometry(100, 100, 800, 600)

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
 
        # Layout setup
        g_map = QGridLayout()

        # Add the error tab to the bottom 
        g_map.addWidget(tab_widget)  
        self.setLayout(g_map)

class _Group3(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Diagnostic Panel")

        # Create Readout group boxes
        # groupR1 = QGroupBox("Readout 1")
        groupR2 = QGroupBox("Readout 2")
        # groupR3 = QGroupBox("Readout 3")
        # groupR4 = QGroupBox("Readout 4")

        # Create QTableWidget for readout 1
        self.table = QTableWidget(6, 1)  # 6 rows, 2 columns
        self.table.setHorizontalHeaderLabels(['Value'])
        
        self.table.setVerticalHeaderLabels([
            'L motor speed', 'R motor speed', 'Velocity', 'Acceleration', 
            'Phidget 1 current', 'Phidget 2 current'
        ])
        # Initialize the table with empty data
        for i in range(6):
            # self.table.setItem(i, 0, QTableWidgetItem(self.table.verticalHeaderItem(i).text()))
            self.table.setItem(i, 0, QTableWidgetItem('0'))

        # Add the table to groupR1
        # layoutR1 = QVBoxLayout()
        # layoutR1.addWidget(self.table)
        # groupR1.setLayout(layoutR1)

        # Add dummy content to other readout groups for demonstration
        for group in [groupR2]:
            layout = QVBoxLayout()
            layout.addWidget(QLabel("to be filled with another table"))
            group.setLayout(layout)

        # Main grid layout setup
        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(self.table, 0, 0)
        g_layout_main.addWidget(groupR2, 0, 1)
        # g_layout_main.addWidget(groupR3, 1, 0)
        # g_layout_main.addWidget(groupR4, 1, 1)

        # Set stretch factors to ensure equal sizing
        # g_layout_main.setRowStretch(0, 4)
        # g_layout_main.setRowStretch(1, 4)
        g_layout_main.setColumnStretch(0, 4)
        g_layout_main.setColumnStretch(1, 4)

        # # Set size policies to ensure all group boxes are the same size
        # for group in [self.table, groupR2]:
        #     group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set up a timer to update values every 3 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(3000)  # 3000 milliseconds = 3 seconds

    def update_values(self):
        # Generate new data with specific formatting for floating-point numbers
        data = [
            str(random.randint(0, 100)),  # L motor speed
            str(random.randint(0, 100)),  # L motor speed
            str(random.randint(0, 100)),  # R motor speed
            f"{random.uniform(0, 10):.2f}",   # Velocity, formatted to 2 decimal places
            f"{random.uniform(0, 5):.2f}",    # Acceleration, formatted to 2 decimal places
            f"{random.uniform(0, 10):.2f}",   # Phidget 1 current, formatted to 2 decimal places
            f"{random.uniform(0, 10):.2f}"    # Phidget 2 current, formatted to 2 decimal places
        ]

        # Update the table with new data
        for i, value in enumerate(data):
            self.table.setItem(i-1, 1, QTableWidgetItem(value))


class _Group4(QGroupBox):
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
    # def __init__(self, csv_handler, tab)
    def setup_ui(self, win: QWidget, csv_handler, tab) -> None:
        """Set up ui."""
        # Widgets
        # val1.print_data()
        self.tab = tab
        
        h_splitter_1 = QSplitter(Qt.Horizontal, win)
        h_splitter_1.setMinimumWidth(100)  # Ensure splitter has a minimum width

        # Left vertical splitter
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(_Group1(csv_handler))
        left_splitter.addWidget(_Group2())
        left_splitter.setMinimumHeight(75)
        left_splitter.setMinimumWidth(500)  # Ensure reasonable width for usability

        # Right vertical splitter
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(_Group3())
        right_splitter.addWidget(_Group4())
        right_splitter.setMinimumHeight(75)
        right_splitter.setMinimumWidth(250)

        # Add both splitters to the horizontal splitter
        h_splitter_1.addWidget(left_splitter)
        h_splitter_1.addWidget(right_splitter)

        # Set even initial sizes
        total_width = h_splitter_1.size().width()
        h_splitter_1.setSizes([total_width//2, total_width//2])  # Divide the total width evenly

        # Main layout setup
        main_layout = QVBoxLayout(win)
        main_layout.addWidget(h_splitter_1)
        win.setLayout(main_layout)
        h_splitter_1.setStretchFactor(1, 2)  
