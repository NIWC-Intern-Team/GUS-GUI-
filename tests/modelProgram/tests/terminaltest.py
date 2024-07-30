import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QProcess

class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Terminal")
        self.setGeometry(100, 100, 800, 600)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        
        self.input_area = QLineEdit(self)
        self.input_area.returnPressed.connect(self.run_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

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

    def change_directory(self, command):
        try:
            # Extract the directory path
            directory = command[3:].strip()
            # Change the directory
            os.chdir(directory)
            # Update the output area with the new working directory
            self.output_area.append(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            self.output_area.append(f"Error: {str(e)}")

    def read_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_area.append(data)

    def read_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_area.append(data)

    def process_finished(self):
        self.output_area.append("Process finished.\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    terminal = Terminal()
    terminal.show()
    sys.exit(app.exec_())
