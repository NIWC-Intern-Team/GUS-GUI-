import sys
import folium
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from customClass import customClickLatLng
from folium.plugins import MousePosition
from folium.plugins import LocateControl


# testChange


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Folium Map with PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Create a folium map
        self.map = folium.Map(location=[32.694, -117.238], zoom_start=15)
        LocateControl(auto_start=True).add_to(self.map) # attempt to set to cLoc
   
        
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
        # folium.Map().add_child(
        #     folium.ClickForMarker()
        # )

        # self.map.add_child(folium.LatLngPopup())
        self.map.add_child(folium.ClickForMarker())
        # Save the map as an HTML file
        self.map.save('map.html')

        # Create a QWebEngineView widget
        self.view = QWebEngineView()
        self.view.setUrl(QUrl('file:///map.html'))

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
