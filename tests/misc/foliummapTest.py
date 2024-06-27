import sys
import os 
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QJsonValue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel

# JS access to PyQt backend 
class Backend(QObject):
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        print(f"Latitude: {lat}, Longitude: {lng}")

# Used to override JS message method to enable data transfer bewteen frontend & backend
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Leaflet Map with PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        
        # Setup path to map.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 2nd parameter (between current_dir & map.html) can be set to subdir within parent for access to map.html
        html_path = os.path.join(current_dir, 'templates', 'map.html') 
        self.view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up QWebChannel for communication
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())