import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class SplitterExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the top horizontal splitter
        h_splitter_top = QSplitter(Qt.Horizontal)
        text_edit_top_left = QTextEdit("Top Left Pane")
        text_edit_top_right = QTextEdit("Top Right Pane")
        h_splitter_top.addWidget(text_edit_top_left)
        h_splitter_top.addWidget(text_edit_top_right)

        # Create the bottom horizontal splitter
        h_splitter_bottom = QSplitter(Qt.Horizontal)
        text_edit_bottom_left = QTextEdit("Bottom Left Pane")
        text_edit_bottom_right = QTextEdit("Bottom Right Pane")
        h_splitter_bottom.addWidget(text_edit_bottom_left)
        h_splitter_bottom.addWidget(text_edit_bottom_right)

        # Create the vertical splitter and add the horizontal splitters to it
        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(h_splitter_top)
        v_splitter.addWidget(h_splitter_bottom)

        # Layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(v_splitter)
        self.setLayout(main_layout)

        # Window properties
        self.setWindowTitle('2x2 Grid with Splitters')
        self.setGeometry(300, 300, 600, 400)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SplitterExample()
    ex.show()
    sys.exit(app.exec_())
