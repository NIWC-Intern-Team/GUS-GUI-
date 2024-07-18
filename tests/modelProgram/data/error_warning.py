from app._ui.gusAll_ui import outerClass

class Error(outerClass._Group3):
    
    def thresholds(self):
        for i in range(1, self.tab + 1):
            self.reload_csv_data()
            
            # Load data from csv files
            self.battery = self.csv_handler.get_battery(i)
            self.lat, self.long = self.csv_handler.get_lat_lon(i)
            self.speed = self.csv_handler.get_speed(i)
            self.temperature = self.csv_handler.get_average_temp(i)
            self.heading = self.csv_handler.get_heading(i)
            
            if self.battery < 20: # battery threshold
                self.error_counter += 1
                self.errors_text_edit.append(f'Gus {i}: Error - Battery low ({self.battery})')
                    
            if self.lat > 200 or self.long > 200: # position threshold
                self.error_counter += 1
                self.errors_text_edit.append(f'Gus {i}: Error - Position too far ({self.lat}, {self.long})')
                    
            if self.speed > 50: # speed threshold
                self.error_counter += 1
                self.errors_text_edit.append(f'Gus {i}: Error - Speed above 50 m/s ({self.speed})')
                    
            if self.temperature > 80: # temperature threshold
                self.error_counter += 1
                self.errors_text_edit.append(f'Gus {i}: Error - Temperature too high ({self.temperature})')
                
            self.tab_widget.setTabText(0, f'Errors({self.error_counter})') # Update total Errors on tab title