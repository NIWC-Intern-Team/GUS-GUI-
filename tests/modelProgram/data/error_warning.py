from app._ui.gusAll_ui import outerClass
from datetime import datetime

class Error(outerClass._Group3):
    
    def thresholds(self):
        time = datetime.now()
        time = time.strftime('%H:%M:%S')
        for i in range(1, self.tab + 1):
            self.reload_csv_data()
            
            # Load data from csv files
            self.battery = self.csv_handler.get_battery(i)
            self.lat, self.long = self.csv_handler.get_lat_lon(i)
            self.speed = self.csv_handler.get_speed(i)
            self.temperature = self.csv_handler.get_average_temp(i)
            self.heading = self.csv_handler.get_heading(i)
            
            if self.battery < 30 and not self.flags[i-1][0]: # battery threshold
                self.flags[i-1][0] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{time} Gus {i}: Error - Battery low ({self.battery})')
            elif self.battery >=20:
                self.flags[i-1][0] = False
                
                    
            if self.lat > 200 or self.long > 200: # position threshold
                self.error_counter += 1
                self.errors_text_edit.append(f'{time} Gus {i}: Error - Position too far ({self.lat}, {self.long})')
                    
            if self.speed > 80 and not self.flags[i-1][2]: # Speed threshold
                self.flags[i-1][2] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{time} Gus {i}: Error - Speed too high ({self.speed})')
            elif self.speed <= 80:
                self.flags[i-1][2] = False
                    
            if self.temperature > 80 and not self.flags[i-1][3]: # temperature threshold
                self.flags[i-1][3] = True
                self.error_counter += 1
                self.errors_text_edit.append(f'{time} Gus {i}: Error - Temperature too high ({self.temperature})')
            elif self.temperature <= 80:
                self.flags[i-1][3] = False
                
            self.tab_widget.setTabText(0, f'Errors({self.error_counter})') # Update total Errors on tab title