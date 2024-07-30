import pygame
from pygame.locals import *
import serial
import time
import serial.tools.list_ports



# Initialize Pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of hats: {joystick.get_numhats()}")

while True:
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            if event.axis == 3:  
                print(f"Axis {event.axis} value: {event.value}")
                if event.value <= -1.0:
                    print("Right joystick hit max left")
                    # ser.write(b"max_left\n")
                elif event.value >= 1.0:
                    print("Right joystick hit max right")
                    # ser.write(b"max_right")
    pygame.time.wait(10)
