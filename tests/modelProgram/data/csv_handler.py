import os
import pandas as pd

class csvHandler():
    def __init__(self) -> None:
        print("CSV handler initialized")
        self.diag_dataframes = {}
        self.ip_sensor_df = {}
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory where csv_handler.py is located
        self.load_dataframes()

    def load_dataframes(self):
        for i in range(1, 6):
            filename = os.path.join(self.base_path, f'{i}_gus.csv')  # Create an absolute path to the CSV file
            try:
                df = pd.read_csv(filename)
                setattr(self, f'df_{i}', df)
                self.diag_dataframes[f'df_{i}'] = df
                # print(f"File {filename} loaded successfully")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    def get_csv_data(self, idx):
        return self.diag_dataframes[f'df_{idx}']
    
    def get_lat_lon(self, idx):
        df = self.diag_dataframes[f'df_{idx}']
        lat = df['lat'].values[0]
        lon = df['lon'].values[0]
        return lat, lon
    
    def get_speed(self, idx):
        df = self.diag_dataframes[f'df_{idx}']
        speed = df['speed'].values[0]
        return speed
    
    def get_average_temp(self, idx):
        df = self.diag_dataframes[f'df_{idx}']
        temp = df['average_temp'].values[0]
        return temp    
    
    def get_battery(self, idx):
        df = self.diag_dataframes[f'df_{idx}']
        battery = df['battery'].values[0]
        return battery    
    
    def get_heading(self, idx):
        df = self.diag_dataframes[f'df_{idx}']
        heading = df['heading'].values[0]
        return heading    
    
    def print_data(self):
        for name, df in self.diag_dataframes.items():
            print(f"DataFrame {name}:")
            print(df)
            print("\n")
            
            
    def load_ip_data(self, tab):
        filename = os.path.join(self.base_path, 'ip_address.csv')  # Create an absolute path to the CSV file
        try:
            df = pd.read_csv(filename)
            df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
            setattr(self, 'ip_address', df)
            self.ip_sensor_df = df
            print(f"File {filename} loaded successfully")
            # print("Columns:", self.ip_sensor_df.columns[0])  
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        finally:
            sensor_ip_dict = self.get_veh_ip_sensor(tab)
            return sensor_ip_dict

    # def print_ip_data(self):
    #     gus_1_df = self.ip_sensor_df[self.ip_sensor_df['Vehicle'] == 'GUS 1']
    #     print(gus_1_df)

    def get_veh_ip_sensor(self, tab):
        
        ip_dict = {}
        sensor_dict = {}
        ip_dict = self.ip_sensor_df[self.ip_sensor_df['Vehicle'] == f'GUS {tab}']['IP Address'].tolist()
        sensor_dict = self.ip_sensor_df[self.ip_sensor_df['Vehicle'] == f'GUS {tab}']['Sensor'].tolist()
        sensor_ip_dict = dict(zip(ip_dict, sensor_dict))
        # print(gus_1_df[0])
        # print(type(sensor_ip_dict))
        return sensor_ip_dict    
    

if __name__ == "__main__":
    csv_handler = csvHandler()
    print("here")
    csv_handler.load_ip_data()
    # csv_handler.print_ip_data()
    csv_handler.get_veh_ip_sensor(5)
    # csv_handler.print_data()
