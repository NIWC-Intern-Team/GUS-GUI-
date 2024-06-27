import sys
import os
from PyQt5 import QtWidgets, uic, QtCore, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot

class Backend(QtCore.QObject):
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        print(f"Latitude: {lat}, Longitude: {lng}")

class CustomWebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber} @ {sourceId})")

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # Load the UI layout from Qt Designer .ui file
        uic.loadUi("C:/Users/16193/Documents/Files_You_use/ProjectFiles/NIWC2024/guiDevelopment/tests/modelProgram/_ui/gusSing_QtC.ui", self)
        
        # Access the GraphicsView widget (assuming it is named 'graphicsView' in Qt Designer)
        self.map_view = self.findChild('QGraphicsView')
        
        if not self.map_view:
            self.map_view = QtWebEngineWidgets.QWebEngineView()
            # self.centralWidget().layout().addWidget(self.map_view)  # Assuming there's a central widget with a layout
        
        # Set up web page for map view
        self.page = CustomWebEnginePage(self)
        self.map_view.setPage(self.page)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'templates', 'map.html')
        self.map_view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up communication channel
        self.channel = QtWebChannel.QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
