import sys
import subprocess
import platform
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QListWidget, QStackedWidget, QSizePolicy

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.file_path = 'app/_ui/ip_address.csv' # Fixed backslash to work on my system
        self.ip_addresses, self.sensors = self.load_ip_addresses_and_sensors_from_csv(self.file_path)
        self.tables = []

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
                push_btn_ping.clicked.connect(lambda _, ip=ip_addresses[i], tbl=table, row=i: self.ping(ip, tbl, row))
                table.setCellWidget(i, 1, push_btn_ping)
                table.setItem(i, 2, QTableWidgetItem("N/A"))
        self.tables.append(table)

        return table

        
    def ping(self, host, table, row):
        print(f"Detected system: {sys.platform} - testing {host}")
        if sys.platform == "win32":
            param = '-n' if platform.system().lower() == 'windows' else '-c'

            try:
                # Run the ping command
                result = subprocess.run(['ping', param, '4', host], capture_output=True, text=True, check=True)
                print(result.stdout)
                print("Ping success!")
                print(row)
                table.setItem(row, 2, QTableWidgetItem("Pass!"))
                return 1
            except subprocess.CalledProcessError as e:
                table.setItem(row, 2, QTableWidgetItem("Fail!"))

                print(f"Ping failed: {e}")
                return e.returncode
            except PermissionError as e:
                print(f"Access denied. Try running the script with administrative privileges. {e}")
                return -1
        elif "linux" in sys.platform:
            print("Linux ping function not tested yet")
                    # Run the ping command
            result = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)

            # Print the output of the ping command
            print(result.stdout)

            # Return the return code (0 means success)
            return result.returncode
        else:
            print("Unknown system.platform: %s  Installation failed, see setup.py." % sys.platform)
            sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
