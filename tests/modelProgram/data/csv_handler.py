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
                # print(f"File {filename} loaded successfully")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    def get_csv_data(self, idx):
        return self.dataframes[f'df_{idx}']
    
    def get_lat_lon(self, idx):
        df = self.dataframes[f'df_{idx}']
        lat = df['lat'].values[0]
        lon = df['lon'].values[0]
        return lat, lon
    
    def get_speed(self, idx):
        df = self.dataframes[f'df_{idx}']
        speed = df['speed'].values[0]
        return speed
    
    def get_average_temp(self, idx):
        df = self.dataframes[f'df_{idx}']
        temp = df['average_temp'].values[0]
        return temp    
    
    def get_battery(self, idx):
        df = self.dataframes[f'df_{idx}']
        battery = df['battery'].values[0]
        return battery    
    
    def get_heading(self, idx):
        df = self.dataframes[f'df_{idx}']
        heading = df['heading'].values[0]
        return heading    
    
    def print_data(self):
        for name, df in self.dataframes.items():
            print(f"DataFrame {name}:")
            print(df)
            print("\n")

if __name__ == "__main__":
    csv_handler = csvHandler()
    csv_handler.print_data()
