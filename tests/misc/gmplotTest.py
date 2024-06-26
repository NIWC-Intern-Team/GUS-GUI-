import sys
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import gmplot

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('gmplot Map with PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Create a gmplot map
        gmap = gmplot.GoogleMapPlotter(32.694, -117.238, 13)

        # Save the map to an HTML file
        gmap.draw('gmap.html')

        # Create a QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.setUrl(QUrl('file:///gmap.html'))

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)

        # Add a button to trigger JavaScript
        self.button = QPushButton("Click to Add Marker")
        self.button.clicked.connect(self.add_marker)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @pyqtSlot()
    def add_marker(self):
        js = """
        function initMap() {
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 13,
                center: {lat: 32.694, lng: -117.238}
            });

            map.addListener('click', function(event) {
                var lat = event.latLng.lat();
                var lng = event.latLng.lng();
                console.log("Latitude: " + lat + ", Longitude: " + lng);
                new google.maps.Marker({
                    position: event.latLng,
                    map: map
                });
            });
        }
        """
        self.view.page().runJavaScript(js)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
