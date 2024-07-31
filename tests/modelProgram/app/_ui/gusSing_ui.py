from __future__ import annotations

import os

from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineCertificateError
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QAbstractScrollArea,
    QHeaderView,
    QTableWidget, 
    QTableWidgetItem,
    QGroupBox
)

from typing import Any
from data.dummy_filler import dummyDataCreator
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QProcess
from app._ui.scripts.gusdrive import *

import pygame
from pygame.locals import *


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Terminal")
        self.setGeometry(100, 100, 800, 600)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        
        self.input_area = QLineEdit(self)
        self.input_area.returnPressed.connect(self.run_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

    def run_command(self):
        command = self.input_area.text().strip()
        if command:
            self.output_area.append(f"$ {command}")
            if command.startswith("cd "):
                self.change_directory(command)
            elif command in ["exit", "exit()"]:
                if self.process.state() == QProcess.Running:
                    self.process.kill()
                    self.output_area.append("Terminating process...\n")
            elif self.process.state() == QProcess.NotRunning:
                self.process.start(command)
                self.input_area.clear()
            else:
                self.output_area.append("Error: Process is already running. Please wait for it to finish.")

    def change_directory(self, command):
        try:
            # Extract the directory path
            directory = command[3:].strip()
            # Change the directory
            os.chdir(directory)
            # Update the output area with the new working directory
            self.output_area.append(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            self.output_area.append(f"Error: {str(e)}")

    def read_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_area.append(data)

    def read_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_area.append(data)

    def process_finished(self):
        self.output_area.append("Process finished.\n")
   

class CustomWebEnginePage(QWebEnginePage):
    '''Used to override JS message method to enable data transfer between frontend and backend'''
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")

    def certificateError(self, error):
        # If you want to ignore the certificates of certain pages
        # then do something like
        # if error.url() == QUrl("https://www.us.army.mil/"):
        #     error.ignoreCertificateError()
        #     return True
        # return super().certificateError(error)

        error.ignoreCertificateError()
        return True

class CustomWebEngineView(QWebEngineView, QWebEngineCertificateError):
    def __init__(self, parent=None):
        super().__init__(parent)

    def certificateError(self, error):
        # If you want to ignore the certificates of certain pages
        # then do something like
        # if error.url() == QUrl("https://www.us.army.mil/"):
        #     error.ignoreCertificateError()
        #     return True
        # return super().certificateError(error)

        error.ignoreCertificateError()
        return True
class Backend(QObject):
    '''JS access to PyQt backend'''
    datatohtml = pyqtSignal(str)  # Signal to send data to HTML
    datafromhtml = pyqtSignal(str)  # Signal to receive data from HTML
    clear_waypoints = pyqtSignal()  # Signal to clear waypoints in HTML

    def __init__(self, parent=None):
        super().__init__()
        self.latlon_arr = []

    @pyqtSlot(float, float)
    def send_gus_coord_htlm(self, lat, lng):
        self.datatohtml.emit(f"Latitude: {lat}, Longitude: {lng}")  # Emit signal with the coordinates

    @pyqtSlot(str)
    def waypoint_Coord(self, message):
        print(f"Waypoint coordinates: {message}")
        self.latlon_arr.append(message)
        print(self.latlon_arr)

    def send_latlon_arr(self):
        return self.latlon_arr

    @pyqtSlot()
    def clear_waypoints_slot(self):
        self.latlon_arr = []
        self.clear_waypoints.emit()  # Emit signal to clear waypoints in HTML

class outerClass: 
    def __init__(self, csv_handler, tab, joystick_count):
        self.tab = tab 
        self.joystick_count = joystick_count
        self.group1 = self._Group1(csv_handler, self.tab)
        self.group2 = self._Group2(csv_handler, self.tab, self.joystick_count)
        self.group3 = self._Group3(csv_handler, self.tab)
        self.group4 = self._Group4(csv_handler, self.tab)

    class _Group1(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("Map")
            self.tab = tab
            self.csv_handler = csv_handler           

            # Widgets        
            push_btn_send, push_btn_delete = QPushButton("Send waypoints"), QPushButton("Delete all waypoints")
                
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
            push_btn_send.clicked.connect(self.send_waypoints)
            push_btn_delete.clicked.connect(self.delete_waypoints)

            # Connect the signal to the slot
            self.backend.datafromhtml.connect(self.backend.waypoint_Coord)

            # Layout setup
            g_map = QGridLayout()

            # Add the view to take up most of the space
            g_map.addWidget(self.view, 1, 0, 1, 3)  

            # Add buttons at the top
            g_map.addWidget(push_btn_send, 0, 0)  # First row, second column
            g_map.addWidget(push_btn_delete, 0, 1)  # First row, third column

            self.setLayout(g_map)
            # Timer to call send_data_to_html every 3 seconds
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.send_data_to_html)
            self.timer.start(500) 
            
        def send_data_to_html(self):
            self.reload_csv_data()
            lat, lon = self.csv_handler.get_lat_lon(self.tab + 1)
            self.backend.send_gus_coord_htlm(lat, lon)

        def reload_csv_data(self):
            self.csv_handler.load_dataframes()
            # print("CSV data reloaded")
            
        def send_waypoints(self):
            latlon_arr = self.backend.send_latlon_arr()
            print(f"-------------- Sent Data --------------\n{latlon_arr}")
            pass

        def delete_waypoints(self):
            print(f"-------------- Deleting array data --------------")
            self.backend.clear_waypoints_slot()  # Call the slot to clear waypoints
            
    class _Group2(QGroupBox):
        def __init__(self, csv_handler, tab, joystick_count) -> None:
            super().__init__("Terminal")
            # Create tab widget for errors and warnings directly
            tab_widget = QTabWidget()
            tab_errors = QWidget()
            tab_warnings = QWidget()
            tab_terminal = Terminal()
            
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
            tab_widget.addTab(tab_terminal, "Terminal")
            for i in range(joystick_count):
                if tab == i:
                    tab_controller = gusCtrl(i)
                    print(f"Controller {i} for tab {tab} set")
                    tab_widget.addTab(tab_controller, f"Controller {i}")
                    break
                else:
                    tab_controller = QTextEdit()
                    tab_layout = QVBoxLayout()
                    tab_layout.addWidget(tab_controller)
                    tab_controller.append("No Assigned controller")
                    tab_widget.addTab(tab_controller, "No Control")
                    

            # Layout setup
            g_map = QGridLayout()

            # Add the error tab to the bottom 
            g_map.addWidget(tab_widget)  
            self.setLayout(g_map)
            
    class _Group3(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("Diagnostics")

            self.csv_handler = csv_handler
            self.tab = tab
            self.angle = 0

            # Create QTableWidget for readouts
            numbers_of_rows = 6
            self.table = QTableWidget(numbers_of_rows, 1)  # 6 rows, 2 columns
            diagnostics_table = self.table
            
            diagnostics_table.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
            diagnostics_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
            diagnostics_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            diagnostics_table.setHorizontalHeaderLabels([' '])
            diagnostics_table.setVerticalHeaderLabels([
                'Latitude', 'Longitude', 'Status', 'Mode', 'Name', 'Battery Status'
            ])
            diagnostics_table.setAlternatingRowColors(True)
            diagnostics_table.setMinimumHeight(205)

            # Initialize the table with empty data
            for i in range(numbers_of_rows):
                self.table.setItem(i, 0, QTableWidgetItem('0'))

            # Main grid layout setup
            g_layout_main = QGridLayout(self)
            g_layout_main.addWidget(self.table)

            # BC (10 July 2024): Adding one to the tab index that I am passing into the update_values method corresponds to a GUS-V number,
            #                    i.e., tab index + 1 = GUS-V number, else this function call will throw an error.
            #                    Example: Tab index 2 = GUS-V 3
            # BC (15 July 2024): The system is reading from a CSV file that will be randomly updated every five seconds to simulate live data
            self.update_values(csv_handler, tab + 1)
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.update_values(csv_handler, tab + 1))
            self.timer.start(10000)

        def update_values(self, csv_handler, gus_number):
            # BC (10 July 2024): Use the CSV handler component to read from CSV files and populate the diagnostic table, 
            #                    in lieu of the dummy data generated below.
            data = csv_handler.get_csv_data(gus_number)
            
            # Update the table with new data
            # BC (10 July 2024): When using CSV data, you must ensure that the value being passed into QTableWidgetItem is an string,
            #                    else the data will not be displayed, so I am using the round() function for a more accurate, less lossy result.
            #                    If the engineers require float-point numbers, then another implementation must be used.
            # BC (17 July 2024): Adding additional conditional statements to process numerical data differently than textual data
            for i, column in enumerate(data):
                data_value = data[column][0]
                self.table.setItem(i-1, 1, QTableWidgetItem(str(data_value)))

            dummyDataCreator.update_data(self)

    class _Group4(QGroupBox):
        def __init__(self, csv_handler, tab) -> None:
            super().__init__("Camera Feeds")
            
            # ip address handling?
            
            # Widgets
            groupL = QGroupBox("Left")
            groupR = QGroupBox("Right")
            groupF = QGroupBox("Rear View")
            groupA = QGroupBox("Front View")

            # Setup widgets
            try:
                self.sensor_ip_dict = csv_handler.load_ip_data(tab+1)
                iplist = list(self.sensor_ip_dict.keys())

            except Exception as e:
                print(f"Error: {e}")
                iplist = ["https://000.000.00.000", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed"]
            finally: 
                pass
            # csv_handler.get_veh_ip_sensor(tab)
            # print(iplist)
            url = "192.168.54.172:8081/video_feed"
            
            # iplist = ["https://000.000.00.000", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed", "https://000.000.00.000:8081/video_feed"]
            modified_ip_list = [f"httpS://{ip}" for ip in iplist]
            
            # Layout
            v_layout_line_edit1 = QVBoxLayout()
            self.web_view = CustomWebEngineView()
            v_layout_line_edit1.addWidget(self.web_view)
            groupL.setLayout(v_layout_line_edit1)
            self.web_view.setUrl(QUrl(modified_ip_list[0]))

            v_layout_line_edit2 = QVBoxLayout()
            self.web_view2 = QWebEngineView()
            v_layout_line_edit2.addWidget(self.web_view2)
            groupR.setLayout(v_layout_line_edit2)
            self.web_view2.setUrl(QUrl(modified_ip_list[1]))


            v_layout_line_edit3 = QVBoxLayout()
            self.web_view3 = QWebEngineView()
            v_layout_line_edit3.addWidget(self.web_view3)
            groupF.setLayout(v_layout_line_edit3)
            self.web_view3.setUrl(QUrl(modified_ip_list[2]))

            v_layout_line_edit4 = QVBoxLayout()
            self.web_view4 = QWebEngineView()
            v_layout_line_edit4.addWidget(self.web_view4)

            groupA.setLayout(v_layout_line_edit4)
            self.web_view4.setUrl(QUrl(modified_ip_list[3]))


            g_layout_main = QGridLayout(self)
            g_layout_main.addWidget(groupL, 0, 0)
            g_layout_main.addWidget(groupR, 0, 1)
            g_layout_main.addWidget(groupF, 1, 0)
            g_layout_main.addWidget(groupA, 1, 1)
            
            g_layout_main.setColumnMinimumWidth(0, 100)
            g_layout_main.setColumnMinimumWidth(1, 100)
        
class singUI:
    """The ui class of widgets window. nice :-D"""

    def setup_ui(self, win: QWidget, csv_handler, tab, joystick_count) -> None:
        """Set up ui."""
        
        # Widgets
        h_splitter_1 = QSplitter(Qt.Horizontal, win)
        h_splitter_1.setMinimumWidth(100)  # Ensure splitter has a minimum width

        outer_instance = outerClass(csv_handler, tab, joystick_count)
        # Left vertical splitter
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(outer_instance.group1)
        left_splitter.addWidget(outer_instance.group2)
        left_splitter.setMinimumHeight(75)
        left_splitter.setMinimumWidth(500)  # Ensure reasonable width for usability

        # Right vertical splitter
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(outer_instance.group3)
        right_splitter.addWidget(outer_instance.group4)
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
