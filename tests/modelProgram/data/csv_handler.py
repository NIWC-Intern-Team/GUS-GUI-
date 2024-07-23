import os
import pandas as pd

class csvHandler():
    def __init__(self) -> None:
        print("CSV handler initialized")
        self.dataframes = {}
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory where csv_handler.py is located
        self.load_dataframes()

    def load_dataframes(self):
        for i in range(1, 6):
            filename = os.path.join(self.base_path, f'{i}_gus.csv')  # Create an absolute path to the CSV file
            try:
                df = pd.read_csv(filename)
                setattr(self, f'df_{i}', df)
                self.dataframes[f'df_{i}'] = df
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    def get_csv_data(self, idx):
        return self.dataframes[f'df_{idx}']
    
    def get_lat_lon(self, idx):
        df = self.dataframes[f'df_{idx}']
        lat = df['lat'].values[0]
        lon = df['lon'].values[0]
        return lat, lon
    
    # BC (23 July 2024): The engineers requested that the battery voltage displayed on the default screen, but did not request
    #                    the heading, speed, or average temperature be displayed on either the default or secondary screens,
    #                    so I changed the get_battery method to get_battery_voltage and commented out the get_speed, get_heading, 
    #                    and get_average_temp methods.
    
    #def get_speed(self, idx):
        #df = self.dataframes[f'df_{idx}']
        #speed = df['speed'].values[0]
        #return speed
    
    #def get_average_temp(self, idx):
        #df = self.dataframes[f'df_{idx}']
        #temp = df['average_temp'].values[0]
        #return temp    
    
    def get_battery_voltage(self, idx):
        df = self.dataframes[f'df_{idx}']
        battery_voltage = df['battery_voltage'].values[0]
        return battery_voltage    
    
    #def get_heading(self, idx):
        #df = self.dataframes[f'df_{idx}']
        #heading = df['heading'].values[0]
        #return heading    
    
    def print_data(self):
        for name, df in self.dataframes.items():
            print(f"DataFrame {name}:")
            print(df)
            print("\n")
    
    def load_ip_data(self):
        filename = os.path.join(self.base_path, f'ip_address.csv')  # Create an absolute path to the CSV file
        try:
            df = pd.read_csv(filename)
            setattr(self, f'ip_address', df)
            self.dataframes[f'ip_address'] = df
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    def print_ip_data(self):
        print(self.dataframes['ip_address'])
    
if __name__ == "__main__":
    csv_handler = csvHandler()
    csv_handler.print_data()
