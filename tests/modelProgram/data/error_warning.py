from app._ui.gusAll_ui import outerClass
from datetime import datetime
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

class Error(outerClass._Group3):
    
    def thresholds(self):
        # Allows for repeating errors if constantly above/below threshold
        def check_errors():
            for i in range(1, self.tab + 1):
                if self.flags[i-1][0]:
                    battery = self.csv_handler.get_battery(i)
                    self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Warning - Battery low ({battery:.3f}%)')
                    
                # if self.flags[i-1][2]:
                #     speed = self.csv_handler.get_speed(i)
                #     self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Warning - Speed too high ({speed:.3f} m/s)')
                    
                if self.flags[i-1][3]:
                    temperature = self.csv_handler.get_average_temp(i)
                    self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Warning - Temperature too high ({temperature:.3f} °C)')
                    
        self.time = datetime.now().strftime('%H:%M:%S')
        # Timer for how often repeat errors should be repeated
        t = QTimer(self)
        t.timeout.connect(check_errors)
        # Popup box for Errors
        error_popup = QMessageBox()
        error_popup.setWindowTitle("Error")
        error_popup.setIcon(QMessageBox.Critical)
        error_popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        error_popup.setDefaultButton(QMessageBox.Ok)
        
        for i in range(1, self.tab + 1):
            self.reload_csv_data()
            # Load data from csv files
            self.battery = self.csv_handler.get_battery(i)
            self.lat, self.long = self.csv_handler.get_lat_lon(i)
            self.speed = self.csv_handler.get_speed(i)
            self.temperature = self.csv_handler.get_average_temp(i)
            self.heading = self.csv_handler.get_heading(i)
            
            # Battery Warning
            if self.battery < 20 and self.battery > 15 and not self.warning_flags[i-1][0]: # Battery Warning
                self.warning_flags[i-1][0] = True
                self.warning_counter += 1
                self.warnings_text_edit.append(f'{self.time} Gus {i}: Warning - Battery low ({self.battery:.3f} V)')
                t.start(60000)
            # Battery Error
            elif self.battery <= 15 and not self.error_flags[i-1][0]: 
                self.error_flags[i-1][0] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Battery low ({self.battery:.3f} V)')
                error_popup.setText(f'{self.time} Gus {i}: Error - Battery low ({self.battery:.3f} V)')
                error_popup.exec_()
            if self.battery > 20:
                self.warning_flags[i-1][0] = False
                self.error_flags[i-1][0] = False
            
            # Lat and lon threshold
            if self.lat > 200 or self.long > 200: 
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Position too far ({self.lat:.3f}, {self.long:.3f})')
            
            # Speed threshold
            # if self.speed > 80 and not self.flags[i-1][2]: 
            #     self.flags[i-1][2] = True
            #     self.error_counter += 1
            #     self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Speed too high ({self.speed:.3f} m/s)')
            #     t.start(60000) # repeats every 60 seconds
            # elif self.speed <= 80:
            #     self.flags[i-1][2] = False
                    
            # Temperature Warning
            if self.temperature > 40 and self.temperature < 45 and not self.warning_flags[i-1][3]: 
                self.warning_flags[i-1][3] = True
                self.warning_counter += 1
                self.warnings_text_edit.append(f'{self.time} Gus {i}: Warning - Temperature too high ({self.temperature:.3f} °C)')
                t.start(60000) # repeats every 60 seconds
            # Temperature Error
            elif self.temperature >= 45 and not self.error_flags[i-1][3]:
                self.error_flags[i-1][3] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Temperature too high ({self.temperature:.3f} °C)')
                error_popup.setText(f'{self.time} Gus {i}: Error - Temperature too high ({self.temperature:.3f} °C)')
                error_popup.exec_()
            if self.temperature <= 40:
                self.warning_flags[i-1][3] = False
                self.error_flags[i-1][3] = False
                
            self.tab_widget.setTabText(0, f'Errors({self.error_counter})') # Update total Errors on tab title
            self.tab_widget.setTabText(1, f'Warnings({self.warning_counter})')