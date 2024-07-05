# Generates random data for gus files 
import csv
import random
import time
import math
import pandas as pd


# Headers
headers = ['lat', 'lon', '_motor_speed', 'r_motor_speed', 'net_velocity', 'net_accel', 'voltage', 
           '1_temp', '2_temp', '3_temp', '1_phidg_v', '1_phidg_c', '2_phidg_v', '2_phidg_c']


# creates data structure 
def create_data():
        # Loop to create and initialize multiple CSV files
    for i in range(1,6):
        filename = f'{i}_gus.csv'
        try:
            df = pd.read_csv(f'{i}_gus.csv')
            print(f"File {i}_gus.csv exists")
            
        except Exception as e:
            print(f"Error: {e}")
            df = pd.DataFrame(columns=headers)
            df.loc[0] = 0  # Initialize with zeros
            df.to_csv(f'{filename}', index=False)
        # finally: # does finally always execute?
            
    pass

# fills csv files with dummy data - 
def dummy_data():
    for i in range(1,6):
        try:
            filename = f'{i}_gus.csv'
            df = pd.read_csv(filename)
            t = random.uniform(0, 2 * math.pi)
            lat = 37.7749 + 0.01 * math.cos(t)  # Example center around 37.7749 (San Francisco latitude)
            lon = -122.4194 + 0.01 * math.sin(t)  # Example center around -122.4194 (San Francisco longitude)

            for x in headers:
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

# Main loop to generate and append data every 2 seconds
if __name__ == "__main__":
    # write_header()  # Write header once
    create_data()
    while True:
        dummy_data()
        time.sleep(2)
    