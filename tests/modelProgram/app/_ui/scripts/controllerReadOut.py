import sys
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtCore import QTimer

class JoystickWidget(QWidget):
    def __init__(self, tab):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 300)

        # Initialize Pygame
        pygame.init()
        pygame.joystick.init()
        self.joysticks = []
        self.init_joysticks()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_events)
        self.timer.start(100)

    def init_joysticks(self):
        ctrl_count = pygame.joystick.get_count()
        if ctrl_count == 0:
            self.output_area.append("No joystick connected")
            return
        print(f"Number of connected controllers: {ctrl_count}")
        self.output_area.append(f"Number of connected controllers: {ctrl_count}")

        for i in range(ctrl_count):
            try:
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                self.joysticks.append(joystick)
                self.output_area.append(f"Joystick {i} name: {joystick.get_name()}")
                self.output_area.append(f"Joystick {i} number of axes: {joystick.get_numaxes()}")
                self.output_area.append(f"Joystick {i} number of buttons: {joystick.get_numbuttons()}")
                self.output_area.append(f"Joystick {i} number of hats: {joystick.get_numhats()}")
            except Exception as e:
                self.output_area.append(f"Error initializing joystick {i}: {e}")

    def check_events(self):
        pygame.event.pump()  # Ensure Pygame is processing events
        for event in pygame.event.get():
            # self.output_area.append(f"Event: {event}")  # Debugging: Print all events to check the queue
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick {event.joy} button {event.button} pressed")
                self.output_area.append(f"Joystick {event.joy} button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Joystick {event.joy} button {event.button} released")
                self.output_area.append(f"Joystick {event.joy} button {event.button} released")
            # elif event.type in [pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION]:
            #     self.output_area.append(f"Event from joystick {event.joy}: {event}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JoystickWidget(0)
    window.show()
    sys.exit(app.exec_())
