import sys
import pygame
import time
import socket
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QListWidget, QStackedWidget, QSizePolicy

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
    def __init__(self, tab):
        super().__init__()
        if tab == 0:
            self.USV_IP = "192.168.1.113"
            self.USV_PORT = 11111


            CONTROL_IP = "192.168.1.202"
            CONTROL_PORT = 10101
        elif tab == 1:
            self.USV_IP = "127.0.0.1"  # Loopback IP address for testing
            self.USV_PORT = 11111  # Dummy port number

            CONTROL_IP = "127.0.0.1"  # Loopback IP address for testing
            CONTROL_PORT = 10101  # Dummy port number
            
            
        self.udpOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.udpIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
        self.udpIn.bind((CONTROL_IP, CONTROL_PORT))  # UDP input

        self.tab = tab 
        self.initUI()
        self.gain = 10
        self.enabled = False
        self.manual = True
        self.autonano = False
        self.autopix = False
        self.done = False
        
    def initUI(self):
        self.main_layout = QHBoxLayout(self)
        self.table = QTableWidget(1, 5) 
        self.table.setHorizontalHeaderLabels(['Joystick', "Status", "Port", "Stb", "Gain"])
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(205)
        self.main_layout.addWidget(self.table)
        self.setLayout(self.main_layout)
        print("Table added to tab:", self.tab)

        # # Initialize Pygame
        pygame.init()
        pygame.joystick.init()

        # # Check if joystick is connected
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(self.tab)
            # self.joystick.init()

        # # self.screen = pygame.Surface((600, 100))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(30)

        self.text_print = TextPrint()
        self.joysticks = {}

    def disableUSV(self):
        print("Sending DISABLE message")
        self.udpOut.sendto(b"DISABLE\n", (self.USV_IP, self.USV_PORT))
        self.udpOut.sendto(b"DISABLE\n", (self.USV_IP, self.USV_PORT))
        self.udpOut.sendto(b"DISABLE\n", (self.USV_IP, self.USV_PORT))

    def killUSV(self):
        print("Sending KILL message")
        self.udpOut.sendto(b"KILL\n", (self.USV_IP, self.USV_PORT))
        self.udpOut.sendto(b"KILL\n", (self.USV_IP, self.USV_PORT))
        self.udpOut.sendto(b"KILL\n", (self.USV_IP, self.USV_PORT))

    def update_pygame(self):
        if self.enabled:
            self.udpOut.sendto(b"ENABLE\n", (self.USV_IP, self.USV_PORT))
        if self.autonano:
            self.udpOut.sendto(b"AUTONANO\n", (self.USV_IP, self.USV_PORT))
        if self.autopix:
           self.udpOut.sendto(b"AUTOPIX\n", (self.USV_IP, self.USV_PORT))

        # Event processing step.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True  # Flag that we are done so we exit this loop.
            '''
            on dev machine key map 
            square: 2
            circle: 1 
            x: 0
            tri: 3
            r1: 10
            when on base station keys need to be remappped 
            
            
            '''
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.enabled = False
                    self.autonano = False
                    self.autopix = False
                    self.disableUSV()
                    # joystick = self.joysticks[0]
                    print("0 hit")
                    self.joystick.rumble(10, 0.7, 500)
                if event.button == 1:
                    self.enabled = True
                    self.manual = True
                    self.autonano = False
                    self.autopix = False
    
                    print(f"Self values: {self.enabled} and {self.manual}")

                    self.joystick.rumble(10, 0.7, 500)
                if event.button == 2:
                    self.enabled = True
                    self.manual = False
                    self.autonano = True
                    self.autopix = False
                    print("2 hit")

                if event.button == 3:
                    self.enabled = True
                    self.manual = False
                    self.autonano = False
                    self.autopix = True
                if event.button == 4:
                    if self.gain > 10:
                        self.gain = self.gain - 10
                    # joystick = self.joysticks[0]
                    self.joystick.rumble(0, 0.7, 500)
                    print("button 4")
                if event.button == 5:
                    if self.gain < 100:
                        self.gain = self.gain + 10
                    # joystick = self.joysticks[0]
                    print("button5")
                    self.joystick.rumble(0, 0.7, 500)
                # if event.button == 10:
                #     self.enabled = False
                #     self.autonano = False
                #     self.autopix = False
                #     self.killUSV()
                #     # joystick = self.joysticks[0]
                #     self.joystick.rumble(10, 0.7, 500)
                if event.button == 10: # R1
                    self.gain = self.gain + 1 
                elif event.button == 9: # L1
                    self.gain = self.gain -1 
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

  
        joystick_count = pygame.joystick.get_count()

        for joystick in self.joysticks.values():
            name = joystick.get_name()
            # self.text_print.tprint(self.screen, f"Joystick: {name}")
            self.table.setItem(0,0,QTableWidgetItem(f"{name}"))
            # print(f"Joystick name: {name}")
            # print(f"again! values: {self.enabled} and {self.manual}")
            if self.enabled and self.manual:
                
                # self.text_print.tprint(self.screen, f"Manual Enabled!")
                self.table.setItem(0,1,QTableWidgetItem("Manual Enabled"))
                # print("manual enableds")
                portaxis = joystick.get_axis(1)
                if abs(portaxis) < 0.1:
                    portaxis = 0
                portaxis = round(portaxis * (-self.gain))
                # self.text_print.tprint(self.screen, f"Port Thrust: {portaxis}")
                self.table.setItem(0,2,QTableWidgetItem(f"{portaxis}"))

                stbdaxis = joystick.get_axis(3)
                if abs(stbdaxis) < 0.1:
                    stbdaxis = 0
                stbdaxis = round(stbdaxis * (-self.gain))
                # self.text_print.tprint(self.screen, f"Stbt Thrust: {stbdaxis}")
                self.table.setItem(0,3,QTableWidgetItem(f"{stbdaxis}"))

                drivecmd = "DRIVE," + str(portaxis) + "," + str(stbdaxis) + "\n"
                self.udpOut.sendto(bytes(drivecmd, 'ascii'), (self.USV_IP, self.USV_PORT))
                

                self.table.setItem(0,4,QTableWidgetItem(f"{self.gain}"))

            elif self.enabled and self.autonano:
                # self.text_print.tprint(self.screen, f"Autonano Enabled!")
                self.table.setItem(0,1,QTableWidgetItem(f"Autonano Enabled"))

                pass
            elif self.enabled and self.autopix:
                # self.text_print.tprint(self.screen, f"Autopix Enabled!")
                self.table.setItem(0,1,QTableWidgetItem(f"Autopix Enabled"))

                pass
            else:
                # self.text_print.tprint(self.screen, f"Disabled!")
                self.table.setItem(0,1,QTableWidgetItem(f"Disabled"))

                pass

            # self.text_print.tprint(self.screen, "STATUS,time.time,enabled,state,vbat")
            # self.text_print.tprint(self.screen, "STATE,time.time,lat,lon,hdg,spd,fixtype,port,stbd")
            # self.text_print.tprint(self.screen, "DESIRED,time.time, trackangle (GPS), dist_to_tgt, brng_to_tgt")

        # self.update_qt_label()

    # def update_qt_label(self):
    #     raw_str = pygame.image.tostring(self.screen, 'RGB')
    #     image = QImage(raw_str, self.screen.get_width(), self.screen.get_height(), QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(image)
    #     self.label.setPixmap(pixmap)
        
def main():
    app = QApplication(sys.argv)
    window = gusCtrl()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
