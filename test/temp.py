import sys
import folium
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QClipboard
from folium.plugins import MousePosition, LocateControl

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Folium Map with PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Create a folium map
        self.map = folium.Map(location=[32.694, -117.238], zoom_start=15)
        LocateControl(auto_start=True).add_to(self.map)

        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};"

        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(self.map)

        # Add click listener to the map
        self.map.add_child(folium.ClickForMarker())

        # Save the map as an HTML file
        self.map.save('map.html')

        # Create a QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.setUrl(QUrl('file:///map.html'))

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Access clipboard using PyQt5
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        print(f"Clipboard content: {clipboard_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
