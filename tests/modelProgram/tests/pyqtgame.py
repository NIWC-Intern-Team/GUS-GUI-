import sys
import pygame
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class PygameWidget(QWidget):
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
        self.screen = pygame.Surface((400, 300))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(30)

    def update_pygame(self):
        # Example Pygame rendering
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), (200, 150), 50)
        
        # Convert Pygame surface to QImage
        raw_str = pygame.image.tostring(self.screen, 'RGB')
        image = QImage(raw_str, self.screen.get_width(), self.screen.get_height(), QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        
        # Display the QPixmap on the QLabel
        self.label.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = PygameWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
