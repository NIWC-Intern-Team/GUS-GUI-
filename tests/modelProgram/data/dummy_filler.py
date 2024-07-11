# Generates random data for gus files 
import csv
import random
import time
import math
import pandas as pd

class dummyDataCreator: 
    # Headers
    def __init__(self):
        self.headers = ['lat', 'lon', 'l_motor_speed', 'r_motor_speed', 'net_velocity', 'net_accel', 'voltage', 
                '1_temp', '2_temp', '3_temp', '1_phidg_v', '1_phidg_c', '2_phidg_v', '2_phidg_c', 'speed', 'average_temperature']

        self.angle = 0 
        
    # creates data structure 
    def create_data(self):
            # Loop to create and initialize multiple CSV files
        for i in range(1,6):
            filename = f'{i}_gus.csv'
            try:
                df = pd.read_csv(f'{i}_gus.csv')
                print(f"File {i}_gus.csv exists")
                
            except Exception as e:
                print(f"Error: {e}")
                df = pd.DataFrame(columns=self.headers)
                df.loc[0] = 0  # Initialize with zeros
                df.to_csv(f'{filename}', index=False)
            # finally: # does finally always execute?
                
        pass

    # fills csv files with dummy data 
    def update_data(self):
        for i in range(1,6):
            try:
                filename = f'{i}_gus.csv'
                df = pd.read_csv(filename)
                self.angle += math.pi / 30  # Increment angle for next point (adjust for desired resolution)
                lat = 32.70476 + 0.001 * math.cos(self.angle)  
                lon = -117.22940 + 0.001 * math.sin(self.angle)

                for x in self.headers:
                    if x == 'lat':
                        df[x] = lat
                    elif x == 'lon':
                        df[x] = lon
                    else:
                        df[x] = random.uniform(0,100)
            
                
                
                df.to_csv(filename, index=False)
            
            except Exception as e:
                print(f"Error: {e}")

        
        
        pass

if __name__ == "__main__":
    # write_header()  # Write header once
    dd = dummyDataCreator()
    dd.create_data()

    while True:
        time.sleep(0.5)
        dd.update_data()
