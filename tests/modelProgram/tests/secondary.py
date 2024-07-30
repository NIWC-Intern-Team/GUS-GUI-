import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QStackedWidget, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout
)


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Create the QListWidget for the sections
        self.section_list = QListWidget()
        self.section_list.addItem("GUS IP SETTINGS")
        self.section_list.addItem("GUS 1")
        self.section_list.addItem("GUS 2")
        self.section_list.addItem("GUS 3")
        self.section_list.addItem("GUS 4")

        # Create the QStackedWidget for the settings panels
        self.stacked_widget = QStackedWidget()
        
        # Create and add the settings panels
        self.settings_panels = [
            self.createSettingsPanel("GUS IP SETTINGS"),
            self.createSettingsPanel("Settings for GUS 1"),
            self.createSettingsPanel("Settings for GUS 2"),
            self.createSettingsPanel("Settings for GUS 3"),
            self.createSettingsPanel("Settings for GUS 4")
        ]

        for panel in self.settings_panels:
            self.stacked_widget.addWidget(panel)

        # Connect the QListWidget selection change to switch the panels
        self.section_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Add widgets to the main layout
        main_layout.addWidget(self.section_list)
        main_layout.addWidget(self.stacked_widget)

    def createSettingsPanel(self, text):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        label = QLabel(text)
        layout.addWidget(label)
        return panel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Create the settings window
        self.settings_window = SettingsWindow()

        # Create a menu action to open the settings window
        settings_action = self.menuBar().addAction("Settings")
        settings_action.triggered.connect(self.openSettings)

        # Set the main window layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_label = QLabel("Main Application")
        main_layout.addWidget(main_label)
        self.setCentralWidget(main_widget)

    def openSettings(self):
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
