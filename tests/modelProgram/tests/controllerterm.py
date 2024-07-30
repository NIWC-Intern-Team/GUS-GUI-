import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QProcess

class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controller Terminal ")
        self.setGeometry(100, 100, 800, 600)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



    def run_command(self):
        command = self.input_area.text().strip()
        if command:
            self.output_area.append(f"$ {command}")
            if command.startswith("cd "):
                self.change_directory(command)
            elif command in ["exit", "exit()"]:
                if self.process.state() == QProcess.Running:
                    self.process.kill()
                    self.output_area.append("Terminating process...\n")
            elif self.process.state() == QProcess.NotRunning:
                self.process.start(command)
                self.input_area.clear()
            else:
                self.output_area.append("Error: Process is already running. Please wait for it to finish.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    terminal = Terminal()
    terminal.show()
    sys.exit(app.exec_())
