import sys, os
import subprocess
import platform
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QListWidget, QStackedWidget, QSizePolicy
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QListWidget, QStackedWidget, QSizePolicy
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot, QObject, pyqtSignal

class WorkerSignals(QObject):
    result = pyqtSignal(int, int, str, int)


class PingWorker(QRunnable):
    def __init__(self, host, table, row, table_id):
        super().__init__()
        self.host = host
        self.table = table
        self.row = row
        self.table_id = table_id 
        self.signals = WorkerSignals()
        

    @pyqtSlot()
    def run(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        print(f"Pinging info: {param}, {self.host}, {self.table}, {self.row}, table id: {self.table_id}")
        try:
            result = subprocess.run(['ping', self.host], capture_output=True, text=True, check=True)
            if result.returncode == 0  and "Destination host unreachable" not in result.stdout: 
                print(f"Ping data result: \n-------\n{result}\n-------\n")
                self.signals.result.emit(self.row, 2, "Pass!", self.table_id)
            else: 
                print(f"Ping data result: \n-------\n{result}\n-------\n")
                self.signals.result.emit(self.row, 2, "Fail!", self.table_id)

        except subprocess.CalledProcessError:
            self.signals.result.emit(self.row, 2, "Fail!",  self.table_id)
        except PermissionError as e:
            self.signals.result.emit(self.row, 2, f"Access Denied: {e}",  self.table_id)



class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
#         self.file_path = 'data/ip_address.csv' # Fixed backslash to work on my system
        
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            # print("non exec")
            base_path = os.path.abspath(".")
        
        relative_path = os.path.join('data', 'ip_address.csv')
        # Get the current directory of settings_window.py
        csv_path = os.path.join(base_path, relative_path)
        
   
        self.file_path = csv_path

        self.ip_addresses, self.sensors = self.load_ip_addresses_and_sensors_from_csv(self.file_path)
        self.tables = []
        self.threadpool = QThreadPool()
        self.initUI()

    def load_ip_addresses_and_sensors_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        ip_dict = {}
        sensor_dict = {}
        for vehicle in df['Vehicle'].unique():
            vehicle_df = df[df['Vehicle'] == vehicle]  # Filter the DataFrame for each vehicle
            ip_dict[vehicle] = vehicle_df['IP Address'].tolist()  # Extract IP addresses as a list
            sensor_dict[vehicle] = vehicle_df['Sensor'].tolist()  
        return ip_dict, sensor_dict
    def save_changes(self):
        df = pd.read_csv(self.file_path)
        
        for vehicle, sensor, line_edit in self.line_edits:
            new_ip = line_edit.text()
            df.loc[(df['Vehicle'] == vehicle) & (df['Sensor'] == sensor), 'IP Address'] = new_ip
        
        df.to_csv(self.file_path, index=False)
        print(df)
        print("Changes saved to", 'ip_address.csv')
        
    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Create the QListWidget for the sections
        self.section_list = QListWidget()
        self.section_list.addItem("GUS IP SETTINGS")
        for vehicle in self.ip_addresses.keys():
            self.section_list.addItem(vehicle)
        self.section_list.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.section_list.setMaximumWidth(150)  

        # Create the QStackedWidget for the settings panels
        self.stacked_widget = QStackedWidget()

        # Create and add the settings panels
        self.settings_panels = [self.createSettingsPanel("GUS IP SETTINGS")]
        table_id = 1
        for vehicle in self.ip_addresses.keys():
            ips = self.ip_addresses[vehicle]
            sensors = self.sensors[vehicle]
            self.settings_panels.append(self.createSettingsPanel(f"Settings for {vehicle}", table_id, vehicle, ips, sensors))
            table_id+=1
        for panel in self.settings_panels:
            self.stacked_widget.addWidget(panel)

        # Connect the QListWidget selection change to switch the panels
        self.section_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Add widgets to the main layout
        main_layout.addWidget(self.section_list)
        main_layout.addWidget(self.stacked_widget)

    def createSettingsPanel(self, text, table_id=None, vehicle=None, ip_addresses=None, sensors=None):
        numbers_of_rows = len(sensors) if sensors else 6
        table = QTableWidget(numbers_of_rows, 3)  # 6 rows, 2 columns
                
        table.setHorizontalHeaderLabels(['IP Address', "Ping", "Result"])
        table.setAlternatingRowColors(True)
        table.setMinimumHeight(205)
        
        if sensors is None or ip_addresses is None:
            pass
        else:
            table.setVerticalHeaderLabels(sensors)
            for i in range(numbers_of_rows):
                table.setItem(i, 0, QTableWidgetItem(f'{ip_addresses[i]}'))
                push_btn_ping = QPushButton(f"Ping")
                push_btn_ping.clicked.connect(lambda _, ip=ip_addresses[i], tbl=table, row=i: self.start_ping(ip, tbl, row, table_id))
                table.setCellWidget(i, 1, push_btn_ping)
                table.setItem(i, 2, QTableWidgetItem("N/A"))
        self.tables.append(table)

        return table

        
    def start_ping(self, host, table, row, table_id):
        
        worker = PingWorker(host, table, row, table_id)
        worker.signals.result.connect(self.update_result)
        self.threadpool.start(worker)

    def update_result(self, row, column, result, table_id):
        table = self.tables[table_id]        
        print(f"Updating table {table} with ID {table_id}")
        if table.item(row, column):
            table.setItem(row, column, QTableWidgetItem(result))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
