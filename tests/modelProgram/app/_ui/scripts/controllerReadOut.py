import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Ensure at least one joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
# print(pygame.joystick.Joystick(1))
print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of hats: {joystick.get_numhats()}")

while True:
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            print(f"Axis {event.axis} value: {event.value}")
        elif event.type == JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        elif event.type == JOYBUTTONUP:
            print(f"Button {event.button} released")
        elif event.type == JOYHATMOTION:
            print(f"Hat {event.hat} value: {event.value}")

    # Optional: add a small delay to reduce CPU usage
    # pygame.time.wait(10)
