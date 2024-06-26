import json
import keyboard  # You need to install the 'keyboard' library: pip install keyboard

# Initial data
data = {
    "left_motor_speed": 0,
    "right_motor_speed": 0,
    "x_pos": 0,
    "y_pos": 0,
    "x_speed": 0,
    "y_speed": 0,
}

def update_file(data):
    with open("shared_data.txt", "w") as f:
        json.dump(data, f)

def key_press_handler():
    print("Press 'Q/A' to adjust left motor speed, 'W/S' for right motor speed, 'E/D' for X pos, 'R/F' for Y pos, 'T/G' for X speed, 'Y/H' for Y speed. Press 'ESC' to exit.")
    while True:
        if keyboard.is_pressed('q'):
            data["left_motor_speed"] += 1
            update_file(data)
            while keyboard.is_pressed('q'):  # Wait for key release
                pass
        elif keyboard.is_pressed('a'):
            data["left_motor_speed"] -= 1
            update_file(data)
            while keyboard.is_pressed('a'):  # Wait for key release
                pass
        elif keyboard.is_pressed('w'):
            data["right_motor_speed"] += 1
            update_file(data)
            while keyboard.is_pressed('w'):  # Wait for key release
                pass
        elif keyboard.is_pressed('s'):
            data["right_motor_speed"] -= 1
            update_file(data)
            while keyboard.is_pressed('s'):  # Wait for key release
                pass
        elif keyboard.is_pressed('e'):
            data["x_pos"] += 1
            update_file(data)
            while keyboard.is_pressed('e'):  # Wait for key release
                pass
        elif keyboard.is_pressed('d'):
            data["x_pos"] -= 1
            update_file(data)
            while keyboard.is_pressed('d'):  # Wait for key release
                pass
        elif keyboard.is_pressed('r'):
            data["y_pos"] += 1
            update_file(data)
            while keyboard.is_pressed('r'):  # Wait for key release
                pass
        elif keyboard.is_pressed('f'):
            data["y_pos"] -= 1
            update_file(data)
            while keyboard.is_pressed('f'):  # Wait for key release
                pass
        elif keyboard.is_pressed('t'):
            data["x_speed"] += 1
            update_file(data)
            while keyboard.is_pressed('t'):  # Wait for key release
                pass
        elif keyboard.is_pressed('g'):
            data["x_speed"] -= 1
            update_file(data)
            while keyboard.is_pressed('g'):  # Wait for key release
                pass
        elif keyboard.is_pressed('y'):
            data["y_speed"] += 1
            update_file(data)
            while keyboard.is_pressed('y'):  # Wait for key release
                pass
        elif keyboard.is_pressed('h'):
            data["y_speed"] -= 1
            update_file(data)
            while keyboard.is_pressed('h'):  # Wait for key release
                pass
        elif keyboard.is_pressed('esc'):
            update_file(data)
            break

if __name__ == '__main__':
    key_press_handler()
