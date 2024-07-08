import sys
import cv2
import numpy as np
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraFeedWidget(QWidget):
    def __init__(self, feed_url):
        super().__init__()
        self.feed_url = feed_url
        
        # Set up the UI
        self.image_label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)
        
        # Set up a timer to fetch the feed periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_feed)
        self.timer.start(30)  # Update every 30 ms (about 33 frames per second)
        
    def update_feed(self):
        # Fetch the frame from the feed
        response = requests.get(self.feed_url)
        image_np = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        # Convert the frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        
        # Update the QLabel with the QImage
        self.image_label.setPixmap(QPixmap.fromImage(q_image))


def main(feed_url):
    app = QApplication(sys.argv)
    window = CameraFeedWidget(feed_url)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    feed_url = "https://192.111.111.111" 
    main(feed_url)
