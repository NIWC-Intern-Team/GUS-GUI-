import random
import time
import math
from numpy import long
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = ['lat','lon','status','mode','name','ip_address','network_status','temp_sensor_1','temp_sensor_2','temp_sensor_3',
           'volt_5v_line_sensor','volt_killsig_line_sensor','volt_24v_line_sensor','volt_curr_24v_line_sensor','volt_curr_thr_line_sensor',
           'battery_status','lidar_sensor','video_feed','teensy_status','thruster_status']
NUMBER_OF_CSV_FILES = 6

class dummyDataCreator:
    """Generates random data for CSV files."""
    def __init__(self):
        self.angle = 0 
        
    def create_data(self):
        '''Creates data structure.'''
        # Loop to create and initialize multiple CSV files
        for i in range(1,NUMBER_OF_CSV_FILES):
            filename = os.path.join(BASE_DIR, f'{i}_gus.csv')
            try:
                df = pd.read_csv(filename)
                print(f"File {i}_gus.csv exists")
                
            except Exception as e:
                print(f"Error: {e}")
                df = pd.DataFrame(columns=HEADERS)
                df.loc[0] = 0  # Initialize with zeros
                df.to_csv(f'{filename}', index=False)            
        pass

    def update_data(self):
        '''Fills csv files with dummy data.'''
        for i in range(1,NUMBER_OF_CSV_FILES):
            try:
                filename = os.path.join(BASE_DIR, f'{i}_gus.csv')
                data_frame = pd.read_csv(filename)
                self.angle += math.pi / 30  # Increment angle for next point (adjust for desired resolution)
                lat_value = 32.70476 + 0.001 * math.cos(self.angle)  
                lon_value = -117.22940 + 0.001 * math.sin(self.angle)
                
                # BC (17 July 2024): I am using the class name in lieu of self because self refers to an external class instance 
                #                    originating from the gusSing_ui.outerClass._Group* module
                data_frame = dummyDataCreator.process_data(data_frame, lat_value, lon_value)
                data_frame.to_csv(filename, index=False)
            except Exception as e:
                print(f"Error: {e}")
        pass

    def process_data(df, lat, lon):
        '''Update numerical fields with random numbers and text fields with a randomly selected value.''' 
        for column_name, column_values in df.items():
            current_value = column_values[0]
            if (isinstance(current_value, float)):
                if column_name == 'lat':
                    df[column_name] = lat
                elif column_name == 'lon':
                    df[column_name] = lon
            elif (isinstance(current_value, (int, long))):
                rounded_number_value = round(random.uniform(0,100))
                df[column_name] = rounded_number_value
            elif (isinstance(current_value, str)):
                if ';' in current_value:
                    current_value_list = current_value.split(';')
                    random_choice_from_list = random.choice(current_value_list)
                    df[column_name] = random_choice_from_list
                else:
                    df[column_name] = current_value
        return df
            

if __name__ == "__main__":
    # write_header()  # Write header once
    dd = dummyDataCreator()
    dd.create_data()

    while True:
        time.sleep(0.5)
        dd.update_data()
