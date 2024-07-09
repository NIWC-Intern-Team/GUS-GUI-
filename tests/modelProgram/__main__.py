import sys
import qdarktheme
from qdarktheme.qtpy.QtWidgets import QApplication
from app.main_window import MainWindow


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    win = MainWindow()
    win.show()
    app.exec()
