import os
import pandas as pd

class csvHandler():
    def __init__(self) -> None:
        print("CSV handler initialized")
        self.dataframes = {}
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory where csv_handler.py is located
        for i in range(1, 6):
            filename = os.path.join(base_path, f'{i}_gus.csv')  # Create an absolute path to the CSV file
            try:
                df = pd.read_csv(filename)
                setattr(self, f'df_{i}', df)
                self.dataframes[f'df_{i}'] = df
                # print(f"File {filename} loaded successfully")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    def get_csv_data(self):
        return self.dataframes

    def print_data(self):
        for name, df in self.dataframes.items():
            print(f"DataFrame {name}:")
            print(df)
            print("\n")

if __name__ == "__main__":
    csv_handler = csvHandler()
    csv_handler.print_data()
