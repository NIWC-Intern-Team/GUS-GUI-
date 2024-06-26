import json
import time
def read_data():
    with open("shared_data.txt", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    while(1):
        data = read_data()
        print("Left Motor Speed:", data["left_motor_speed"])
        print("Right Motor Speed:", data["right_motor_speed"])
        print("X Position:", data["x_pos"])
        print("Y Position:", data["y_pos"])
        print("X Speed:", data["x_speed"])
        print("Y Speed:", data["y_speed"])
        time.sleep(1)