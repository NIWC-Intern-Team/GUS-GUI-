import sys
import pygame
import time
import socket
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

import os

from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineCertificateError
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QAbstractScrollArea,
    QHeaderView,
    QTableWidget, 
    QTableWidgetItem,
    QGroupBox
)

from typing import Any
# from data.dummy_filler import dummyDataCreator
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QProcess

import pygame
from pygame.locals import *

USV_IP = "192.168.1.113"
USV_PORT = 11111

udpOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP output

CONTROL_IP = "192.168.1.202"
CONTROL_PORT = 10101
udpIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpIn.bind((CONTROL_IP, CONTROL_PORT))  # UDP input

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


class gusCtrl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.gain = 10
        self.enabled = False
        self.manual = True
        self.autonano = False
        self.autopix = False
        self.done = False
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Initialize Pygame
        pygame.init()
        pygame.joystick.init()

        # Check if joystick is connected
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            # self.joystick.init()

        self.screen = pygame.Surface((500, 500))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(30)

        self.text_print = TextPrint()
        self.joysticks = {}

    def disableUSV(self):
        print("Sending DISABLE message")
        udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))
        udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))
        udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))

    def killUSV(self):
        print("Sending KILL message")
        udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))
        udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))
        udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))

    def update_pygame(self):
        if self.enabled:
            udpOut.sendto(b"ENABLE\n", (USV_IP, USV_PORT))
        if self.autonano:
            udpOut.sendto(b"AUTONANO\n", (USV_IP, USV_PORT))
        if self.autopix:
            udpOut.sendto(b"AUTOPIX\n", (USV_IP, USV_PORT))

        # Event processing step.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.enabled = False
                    self.autonano = False
                    self.autopix = False
                    self.disableUSV()
                    joystick = self.joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)
                if event.button == 1:
                    self.enabled = True
                    self.manual = True
                    self.autonano = False
                    self.autopix = False
                    joystick = self.joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)
                if event.button == 2:
                    self.enabled = True
                    self.manual = False
                    self.autonano = True
                    self.autopix = False
                if event.button == 3:
                    self.enabled = True
                    self.manual = False
                    self.autonano = False
                    self.autopix = True
                if event.button == 4:
                    if self.gain > 10:
                        self.gain = self.gain - 10
                    joystick = self.joysticks[event.instance_id]
                    joystick.rumble(0, 0.7, 500)
                if event.button == 5:
                    if self.gain < 100:
                        self.gain = self.gain + 10
                    joystick = self.joysticks[event.instance_id]
                    joystick.rumble(0, 0.7, 500)
                if event.button == 10:
                    self.enabled = False
                    self.autonano = False
                    self.autopix = False
                    self.killUSV()
                    joystick = self.joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        self.screen.fill((255, 255, 255))
        self.text_print.reset()

        joystick_count = pygame.joystick.get_count()

        for joystick in self.joysticks.values():
            name = joystick.get_name()
            self.text_print.tprint(self.screen, f"Joystick: {name}")

            if self.enabled and self.manual:
                self.text_print.tprint(self.screen, f"Manual Enabled!")

                portaxis = joystick.get_axis(1)
                if abs(portaxis) < 0.1:
                    portaxis = 0
                portaxis = round(portaxis * (-self.gain))
                self.text_print.tprint(self.screen, f"Port Thrust: {portaxis}")

                stbdaxis = joystick.get_axis(4)
                if abs(stbdaxis) < 0.1:
                    stbdaxis = 0
                stbdaxis = round(stbdaxis * (-self.gain))
                self.text_print.tprint(self.screen, f"Stbt Thrust: {stbdaxis}")
                drivecmd = f"DRIVE,{portaxis},{stbdaxis}\n"
                udpOut.sendto(bytes(drivecmd, 'ascii'), (USV_IP, USV_PORT))

                gaindownbutton = joystick.get_button(4)
                self.text_print.tprint(self.screen, f"Gain Down: {gaindownbutton}")

                gainupbutton = joystick.get_button(5)
                self.text_print.tprint(self.screen, f"Gain Up: {gainupbutton}")

            elif self.enabled and self.autonano:
                self.text_print.tprint(self.screen, f"Autonano Enabled!")
            elif self.enabled and self.autopix:
                self.text_print.tprint(self.screen, f"Autopix Enabled!")
            else:
                self.text_print.tprint(self.screen, f"Disabled!")

            self.text_print.tprint(self.screen, "STATUS,time.time,enabled,state,vbat")
            self.text_print.tprint(self.screen, "STATE,time.time,lat,lon,hdg,spd,fixtype,port,stbd")
            self.text_print.tprint(self.screen, "DESIRED,time.time, trackangle (GPS), dist_to_tgt, brng_to_tgt")

        self.update_qt_label()

    def update_qt_label(self):
        raw_str = pygame.image.tostring(self.screen, 'RGB')
        image = QImage(raw_str, self.screen.get_width(), self.screen.get_height(), QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
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
        self.tab = tab 
        self.init_joysticks(tab)
        

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.check_events)
        # self.timer.start(100)

    def init_joysticks(self, tab):
        ctrl_count = pygame.joystick.get_count()
        if ctrl_count == 0:
            self.output_area.append("No joystick connected")
            return
        print(f"Number of connected controllers: {ctrl_count} - tab: {self.tab}")
        self.output_area.append(f"Number of connected controllers: {ctrl_count}")

        try:
            joystick = pygame.joystick.Joystick(tab)
            joystick.init()
            self.joysticks.append(joystick)
            self.output_area.append(f"Joystick {tab} name: {joystick.get_name()}")
            self.output_area.append(f"Joystick {tab} number of axes: {joystick.get_numaxes()}")
            self.output_area.append(f"Joystick {tab} number of buttons: {joystick.get_numbuttons()}")
            self.output_area.append(f"Joystick {tab} number of hats: {joystick.get_numhats()}")
        except Exception as e:
            self.output_area.append(f"Error initializing joystick {tab}: {e}")

    def check_events(self):
        pygame.event.pump()  # Ensure Pygame is processing events
        for event in pygame.event.get():
            # self.output_area.append(f"Event: {event}")  # Debugging: Print all events to check the queue
            if event.type == pygame.JOYBUTTONDOWN:
                
                print(f"instace: {event.instance_id} and tab {self.tab}")
                self.output_area.append(f"Joystick {event.joy} button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"instace: {event.instance_id}")
                self.output_area.append(f"Joystick {event.joy} button {event.button} released")


class ctrlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        # Initialize Pygame
        pygame.init()
        pygame.joystick.init()

        # Check if joystick is connected
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            # self.joystick.init()
            
def main():
    app = QApplication(sys.argv)
    window = ctrlUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
