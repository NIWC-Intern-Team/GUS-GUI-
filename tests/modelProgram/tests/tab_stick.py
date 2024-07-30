import sys
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QSizePolicy, QTabWidget
from PyQt5.QtCore import QTimer

class JoystickWidget(QWidget):
    def __init__(self, joystick_index):
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
        
        if joystick_index >= pygame.joystick.get_count():
            self.output_area.append("Joystick index out of range")
            return
        
        try:
            self.joystick = pygame.joystick.Joystick(joystick_index)
            self.joystick.init()
            self.output_area.append(f"Joystick {joystick_index} name: {self.joystick.get_name()}")
            self.output_area.append(f"Joystick {joystick_index} number of axes: {self.joystick.get_numaxes()}")
            self.output_area.append(f"Joystick {joystick_index} number of buttons: {self.joystick.get_numbuttons()}")
            self.output_area.append(f"Joystick {joystick_index} number of hats: {self.joystick.get_numhats()}")
        except Exception as e:
            self.output_area.append(f"Error initializing joystick {joystick_index}: {e}")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_events)
        self.timer.start(100)

    def check_events(self):
        pygame.event.pump()  # Ensure Pygame is processing events
        for event in pygame.event.get():
            if event.type:
                self.output_area.append(f"Event: {event}")  # Debugging: Print all events to check the queue
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"Joystick {event.instance_id} button {event.button} pressed")
                    self.output_area.append(f"Joystick {event.instance_id} button {event.button} pressed")
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"Joystick {event.instance_id} button {event.button} released")
                    self.output_area.append(f"Joystick {event.instance_id} button {event.button} released")
                elif event.type in [pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION]:
                    self.output_area.append(f"Event from joystick {event.instance_id}: {event}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab_widget)

        self.setLayout(self.layout)

        self.init_tabs()

    def init_tabs(self):
        joystick_count = 2
        if joystick_count == 0:
            no_joystick_tab = QWidget()
            no_joystick_tab.setLayout(QVBoxLayout())
            no_joystick_tab.layout().addWidget(QTextEdit("No joysticks connected"))
            self.tab_widget.addTab(no_joystick_tab, "No Joystick")
        else:
            for i in range(joystick_count):
                joystick_tab = JoystickWidget(i)
                self.tab_widget.addTab(joystick_tab, f"Joystick {i}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
