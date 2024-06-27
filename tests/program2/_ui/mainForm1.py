import sys
from PyQt5 import QtWidgets
from form1 import Ui_Form 

class MyForm(QtWidgets.QWidget):
    def __init__(self):
        super(MyForm, self).__init__()
        self.ui = Ui_Form()
        self.ui.setup_ui(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MyForm()
    mainWin.show()
    sys.exit(app.exec_())
