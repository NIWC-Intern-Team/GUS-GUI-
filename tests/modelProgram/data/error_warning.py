from app._ui.gusAll_ui import outerClass
from datetime import datetime
from PyQt5.QtCore import QTimer

class Error(outerClass._Group3):
    
    def thresholds(self):
        # Allows for repeating errors if constantly above/below threshold
        def check_errors():
            for i in range(1, self.tab + 1):
                if self.flags[i-1][0]:
                    battery = self.csv_handler.get_battery(i)
                    self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Error - Battery low ({battery:.3f}%)')
                    
                if self.flags[i-1][2]:
                    speed = self.csv_handler.get_speed(i)
                    self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Error - Speed too high ({speed:.3f} m/s)')
                    
                if self.flags[i-1][3]:
                    temperature = self.csv_handler.get_average_temp(i)
                    self.errors_text_edit.append(f'{self.time} Gus {i}: Repeat Error - Temperature too high ({temperature:.3f} °C)')
                    
        self.time = datetime.now().strftime('%H:%M:%S')
        # Timer for how often repeat errors should be repeated
        t = QTimer(self)
        t.timeout.connect(check_errors)
        
        for i in range(1, self.tab + 1):
            self.reload_csv_data()
            # Load data from csv files
            self.battery = self.csv_handler.get_battery(i)
            self.lat, self.long = self.csv_handler.get_lat_lon(i)
            self.speed = self.csv_handler.get_speed(i)
            self.temperature = self.csv_handler.get_average_temp(i)
            self.heading = self.csv_handler.get_heading(i)
            
            # Battery threshold
            if self.battery < 45 and not self.flags[i-1][0]: 
                self.flags[i-1][0] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Battery low ({self.battery:.3f}%)')
                t.start(60000) # repeats every 60 seconds
            elif self.battery >= 45:
                self.flags[i-1][0] = False
            
            # Lat and lon threshold
            if self.lat > 200 or self.long > 200: 
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Position too far ({self.lat:.3f}, {self.long:.3f})')
            
            # Speed threshold
            if self.speed > 80 and not self.flags[i-1][2]: 
                self.flags[i-1][2] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Speed too high ({self.speed:.3f} m/s)')
                t.start(60000) # repeats every 60 seconds
            elif self.speed <= 80:
                self.flags[i-1][2] = False
                    
            # Temperature threshold
            if self.temperature > 80 and not self.flags[i-1][3]: 
                self.flags[i-1][3] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{self.time} Gus {i}: Error - Temperature too high ({self.temperature:.3f} °C)')
                t.start(60000) # repeats every 60 seconds
            elif self.temperature <= 80:
                self.flags[i-1][3] = False
                
            self.tab_widget.setTabText(0, f'Errors({self.error_counter})') # Update total Errors on tab title