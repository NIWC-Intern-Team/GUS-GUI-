import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer

class LiveUpdateListWidget(QWidget):
    # Static variables for diagnostic data
    leftMotorSpeed = 0
    rightMotorSpeed = 0
    posX = 0
    posY = 0
    velX = 0
    velY = 0
    accX = 0
    accY = 0
    posNames = ["left_motor_speed", "right_motor_speed", "x_pos", "y_pos", "x_speed", "y_speed"]
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Example data linked to class-level attributes
        self.data = {
            "Left Motor Speed": lambda: LiveUpdateListWidget.leftMotorSpeed,
            "Right Motor Speed": lambda:LiveUpdateListWidget.rightMotorSpeed,
            "X Position": lambda:LiveUpdateListWidget.posX,
            "Y Position": lambda:LiveUpdateListWidget.posY,
            "X Velocity": lambda:LiveUpdateListWidget.velX,
            "Y Velocity": lambda:LiveUpdateListWidget.velY,
            "X Acceleration": lambda:LiveUpdateListWidget.accX,
            "Y Acceleration":  lambda:LiveUpdateListWidget.accY,
        }

        self.initUI()
        self.setLayout(self.layout)
        
        # Timer for live updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.autoUpdateValues)
        self.timer.start(100)  # Update every 10 milliseconds

    def initUI(self):
        # Populate list widget with initial data
        for name in self.data.keys():
            item = QListWidgetItem(f"{name}: {self.data[name]}")
            self.list_widget.addItem(item)
            
    def manualUpdateValues(self):
        try:
            with open("shared_data.txt", "r") as f:
                fileData = f.read()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            pass
        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            name = item.text().split(":")[0]
            item.setText(f"{name}: {self.data[name]()}")
            
            
    def autoUpdateValues(self):
        # Auto updating values
        LiveUpdateListWidget.leftMotorSpeed += 1
        LiveUpdateListWidget.rightMotorSpeed += 2
        LiveUpdateListWidget.posX += 0.1
        LiveUpdateListWidget.posY += 0.2
        LiveUpdateListWidget.velX += 0.01
        LiveUpdateListWidget.velY += 0.02
        LiveUpdateListWidget.accX += 0.001
        LiveUpdateListWidget.accY += 0.002

        # Update the list widget
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            name = item.text().split(":")[0]
            item.setText(f"{name}: {self.data[name]()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LiveUpdateListWidget()
    widget.show()
    sys.exit(app.exec_())
