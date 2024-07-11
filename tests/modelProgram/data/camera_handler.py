import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class CameraFeed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

        self.web_view.setUrl(QUrl("http://100.64.219.47:8081/video_feed"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraFeed()
    window.show()
    sys.exit(app.exec_())
