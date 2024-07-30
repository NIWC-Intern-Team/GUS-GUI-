import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.joystick.init()
ctrl_count = pygame.joystick.get_count()
# Ensure at least one joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()
print(f"number of conn ctrllers: {pygame.joystick.get_count()}")

# Initialize the first joystick
joystick_1 = pygame.joystick.Joystick(0)
# joystick_2 = pygame.joystick.Joystick(1)

joystick_1.init()
# joystick_2.init()


joysticks = []
for i in range(ctrl_count+1):
    print(i)
    try:
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        print(f"Joystick {i} name: {joystick.get_name()}")
        print(f"Joystick {i} number of axes: {joystick.get_numaxes()}")
        print(f"Joystick {i} number of buttons: {joystick.get_numbuttons()}")
        print(f"Joystick {i} number of hats: {joystick.get_numhats()}")
    except Exception as e:
        print(f"Error initializing joystick {i}: {e}")


while True:
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            print(f"Joystick {event.instance_id} button {event.button} pressed")
        elif event.type == JOYBUTTONUP:
            print(f"Joystick {event.instance_id} button {event.button} released")
        elif event.type == pygame.JOYAXISMOTION:
            axis_value = joystick.get_axis(event.axis)
            print(f"Joystick {event.instance_id} axis {event.axis} value: {axis_value:.2f}")
