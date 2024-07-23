import sys
import subprocess
import platform
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QListWidget, QStackedWidget, QSizePolicy

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.file_path = 'data/ip_address.csv'
        self.ip_addresses, self.sensors = self.load_ip_addresses_and_sensors_from_csv(self.file_path)
        self.initUI()

    def load_ip_addresses_and_sensors_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        ip_dict = {}
        sensor_dict = {}
        for vehicle in df['Vehicle'].unique():
            vehicle_df = df[df['Vehicle'] == vehicle]  # Filter the DataFrame for each vehicle
            ip_dict[vehicle] = vehicle_df['IP Address'].tolist()  # Extract IP addresses as a list
            sensor_dict[vehicle] = vehicle_df['Sensor'].tolist()  # Extract sensor names as a list
        return ip_dict, sensor_dict

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Create the QListWidget for the sections
        self.section_list = QListWidget()
        self.section_list.addItem("GUS IP SETTINGS")
        for vehicle in self.ip_addresses.keys():
            self.section_list.addItem(vehicle)
        self.section_list.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.section_list.setMaximumWidth(150)  # Adjust the width as needed

        # Create the QStackedWidget for the settings panels
        self.stacked_widget = QStackedWidget()

        # Create and add the settings panels
        self.settings_panels = [self.createSettingsPanel("GUS IP SETTINGS")]
        for vehicle in self.ip_addresses.keys():
            ips = self.ip_addresses[vehicle]
            sensors = self.sensors[vehicle]
            self.settings_panels.append(self.createSettingsPanel(f"Settings for {vehicle}", vehicle, ips, sensors))
        for panel in self.settings_panels:
            self.stacked_widget.addWidget(panel)

        # Connect the QListWidget selection change to switch the panels
        self.section_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Add widgets to the main layout
        main_layout.addWidget(self.section_list)
        main_layout.addWidget(self.stacked_widget)

    def createSettingsPanel(self, text, vehicle=None, ip_addresses=None, sensors=None):
        numbers_of_rows = len(sensors) if sensors else 6
        self.table = QTableWidget(numbers_of_rows, 2)  # 6 rows, 2 columns
                
        self.table.setHorizontalHeaderLabels(['IP Address', "Ping"])
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(205)
        
        if sensors is None or ip_addresses is None:
            pass
        else:
            self.table.setVerticalHeaderLabels(sensors)
            for i in range(numbers_of_rows):
                self.table.setItem(i, 0, QTableWidgetItem(f'{ip_addresses[i]}'))
                push_btn_ping = QPushButton(f"Ping")
                push_btn_ping.clicked.connect(lambda _, ip=ip_addresses[i]: self.ping(ip))
                self.table.setCellWidget(i, 1, push_btn_ping)

        return self.table

    def save_changes(self):
        df = pd.read_csv(self.file_path)
        
        for vehicle, sensor, line_edit in self.line_edits:
            new_ip = line_edit.text()
            df.loc[(df['Vehicle'] == vehicle) & (df['Sensor'] == sensor), 'IP Address'] = new_ip
        
        df.to_csv(self.file_path, index=False)
        print(df)
        print("Changes saved to", 'ip_address.csv')
        
    def ping(self, host):
        print(f"Pinging {host}...")
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        try:
            result = subprocess.run(['ping', param, '4', host], capture_output=True, text=True)
            print(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            print(f"Ping failed: {e}")
            return e.returncode
        except PermissionError as e:
            print(f"Access denied. Try running the script with administrative privileges. {e}")
            return -1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
