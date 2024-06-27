import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class SplitterExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the main vertical splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left pane (entire left side)
        text_edit_left = QTextEdit("Left Pane")
        main_splitter.addWidget(text_edit_left)

        # Right pane (split into two vertically)
        right_splitter = QSplitter(Qt.Vertical)
        text_edit_top_right = QTextEdit("Top Right Pane")
        text_edit_bottom_right = QTextEdit("Bottom Right Pane")
        right_splitter.addWidget(text_edit_top_right)
        right_splitter.addWidget(text_edit_bottom_right)

        # Add the right splitter to the main splitter
        main_splitter.addWidget(right_splitter)

        # Layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

        # Window properties
        self.setWindowTitle('Left-Right Split Layout')
        self.setGeometry(300, 300, 600, 400)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SplitterExample()
    ex.show()
    sys.exit(app.exec_())
