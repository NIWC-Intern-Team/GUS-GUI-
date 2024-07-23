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

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import random 

# JS access to PyQt backend 
class Backend(QObject):
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        print(f"Latitude: {lat}, Longitude: {lng}")
    
    def sendSpeed(self, speed):
        print(f'Speed: {speed}')
        
    def sendTemperature(self, temperature):
        print(f'Temperature: {temperature}')

# Used to override JS message method to enable data transfer bewteen frontend & backend
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")


class outerClass:
    def __init__(self, csv_handler, tab):
        self.tab = tab
        self.group1 = self._Group1(csv_handler, self.tab)
        self.group2 = self._Group2(csv_handler, self.tab)
        self.group3 = self._Group3(csv_handler, self.tab)
    
    
# Map Widget
    class _Group1(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("Map")
            
            self.tab = tab
            self.csv_handler = csv_handler

            # self.outer_instance = outer
            # self.tab = tab
            # self.setGeometry(100, 100, 800, 600)
            # csv_handler.print_data()
            # lat = csv_handler.self.dataframes
            

            # Widgets        
            map_group = QGroupBox("Map & Features")
            group_push = QGroupBox("Push Button")

            push_btn_send, push_btn_delete = QPushButton("Send waypoints"), QPushButton("Delete all waypoints")
            
            # test_btn
                
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
            push_btn_send.clicked.connect(self.send_waypoints)

            # Layout setup
            g_map = QGridLayout()

            # Add the view to take up most of the space
            g_map.addWidget(self.view, 1, 0, 1, 3)  

            self.setLayout(g_map)
            
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.send_data_to_html)
            self.timer.start(500)
            
        def send_data_to_html(self):
            self.reload_csv_data()
            lat, lon = self.csv_handler.get_lat_lon(self.tab)
            self.backend.sendCoordinates(lat, lon)

        def reload_csv_data(self):
            self.csv_handler.load_dataframes()
            # print("CSV data reloaded")
            
        def send_waypoints(self):
            pass

    # All GUS overview
    class _Group2(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("All Gus Connections")

            self.tab = tab
            self.csv_handler = csv_handler

            # Creating column and row names for tables
            self.labels = []
            self.tables = []
            
            for i in range(1,6):
                label = QLabel(f'Gus {i}')
                table = QTableWidget(5,1)
                table.setVerticalHeaderLabels(['Battery Percentage', 'Location', 'Speed', 'Temperature', 'Heading']) # add header and battery percent
                table.setHorizontalHeaderLabels(['Values'])
                
                self.labels.append(label)
                self.tables.append(table)
                
            g_layout_main = QGridLayout(self)
            
            # Adding label and table widgets to layout
            for i in range(5):
                g_layout_main.addWidget(self.labels[i], i, 0)
                g_layout_main.addWidget(self.tables[i], i, 1)
            
            # Populate table with -1
            for table in self.tables:
                for i in range(3):
                    table.setItem(i, 0, QTableWidgetItem('-1'))
                    
            
            #self.backend = Backend()
            # Timer to update table data
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.send_data_to_gui)
            self.timer.start(500)
            
            
            
        def send_data_to_gui(self):
            # Access CSV data and update table data
            for i in range(1, self.tab + 1):
                self.reload_csv_data()
                
                self.battery = self.csv_handler.get_battery(i)
                self.tables[i - 1].setItem(0,0, QTableWidgetItem(f'{self.battery:.3f}%'))
                
                self.lat, self.long = self.csv_handler.get_lat_lon(i)
                self.tables[i - 1].setItem(1,0, QTableWidgetItem(f'{self.lat:.3f}, {self.long:.3f}'))
                    
                self.speed = self.csv_handler.get_speed(i)
                self.tables[i - 1].setItem(2, 0, QTableWidgetItem(f'{self.speed:.3f} m/s'))
                    
                self.temperature = self.csv_handler.get_average_temp(i)
                self.tables[i - 1].setItem(3, 0, QTableWidgetItem(f'{self.temperature:.3f} °C'))
                
                self.heading = self.csv_handler.get_heading(i)
                self.tables[i - 1].setItem(4,0, QTableWidgetItem(f'{self.heading:.3f}°'))
                
                self.tables[i - 1].resizeColumnsToContents()

                
                #self.backend.sendTemperature(temperature)
               # self.backend.sendSpeed(speed)

        
        def reload_csv_data(self):
            self.csv_handler.load_dataframes()
            

    # Warning and Error Widget
    class _Group3(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("Terminal")

            self.csv_handler = csv_handler
            self.tab = tab
            self.error_counter = 0
            # self.view.setMaximumSize(100,100)
            self.tab_widget = QTabWidget()
            tab_errors = QWidget()
            tab_warnings = QWidget()

            # Add text areas for errors and warnings
            self.errors_text_edit = QTextEdit()
            warnings_text_edit = QTextEdit()

            # Layouts for tabs
            errors_layout = QVBoxLayout()
            errors_layout.addWidget(self.errors_text_edit)
            tab_errors.setLayout(errors_layout)

            warnings_layout = QVBoxLayout()
            warnings_layout.addWidget(warnings_text_edit)
            tab_warnings.setLayout(warnings_layout)
            
            # Add tabs to the tab widget
            self.tab_widget.addTab(tab_errors, f'Errors({self.error_counter})')
            self.tab_widget.addTab(tab_warnings, "Warnings")

            g_error_layout = QGridLayout()
            g_error_layout.addWidget(self.tab_widget, 2, 0, 1, 3)  
            self.setLayout(g_error_layout)
            
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.thresholds)
            self.timer.start(500)
            
            self.flags = [[False, False, False, False], # battery, location, speed, temperature
                [False, False, False, False], 
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],] 
            
        # Checks for error thresholds
        def thresholds(self):
            from data.error_warning import Error
            Error.thresholds(self)
        
        def reload_csv_data(self):
            self.csv_handler.load_dataframes()
            
            
class allUI:
    """The ui class of All widgets window. nice :-D"""

    def setup_ui(self, win: QWidget,  csv_handler, tab) -> None:
        """Set up ui."""
        outer_instance = outerClass(csv_handler, tab)
        
        # Widgets
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal) # Creates left and right side to resize horizontally
        # Setup widgets
        h_splitter_1.setMinimumHeight(350)  # Fix bug layout crush

        # Layout
        self.left_splitter = QSplitter(Qt.Vertical) # Creates left stack of widgets to resize vertically
        self.left_splitter.addWidget(outer_instance.group1)
        self.left_splitter.addWidget(outer_instance.group3)

        # Adds vertical left widgets and the right widget to be able to resize horizontally
        h_splitter_1.addWidget(self.left_splitter)
        outer_instance.group2.setMinimumWidth(360) #adjust gus overview minimum size
        h_splitter_1.addWidget(outer_instance.group2)

        widget_container = QWidget()
        
        # Set the main layout
        main_layout = QVBoxLayout(win)
        main_layout.addWidget(h_splitter_1)
        win.setLayout(main_layout)

        # Adjust splitter sizes dynamically
        #h_splitter_1.setStretchFactor(1, 2)  # Vertical splitter takes more space

        h_splitter_1.setSizes([800, 150])  # Equal initial sizes for vertical sections