"""Main module of GUS GUI."""
from qdarktheme._util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon
from qdarktheme.qtpy.QtWidgets import (
    QColorDialog,
    QFileDialog,
    QFontDialog,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QWidget,
)

# from _ui.singGUI import Ui_MainWindow

from _ui.form2 import Ui_Form
class Navigator: 
    """ Navigator Setup """
    def setup_ui(self, main_win: QMainWindow) -> None: 
        
        # Actions     
        self.action_open_folder = QAction(QIcon("icons:niwc_1.svg"), "Open folder dialog")
        self.action_open_color_dialog = QAction(QIcon("icons:niwc_1.svg"), "Open color dialog")
        self.action_open_font_dialog = QAction(
            QIcon("icons:niwc_1.svg"), "Open font dialog"
        )
        self.action_enable = QAction(QIcon("icons:niwc_1.svg"), "Enable")
        self.action_disable = QAction(QIcon("icons:niwc_1.svg"), "Disable")
        self.actions_theme = [QAction(theme, main_win) for theme in ["auto", "dark", "light"]]
        self.actions_page = (
            QAction(QIcon("icons:niwc_1.svg"), "Move to 1"),
            QAction(QIcon("icons:niwc_2.svg"), "Move to 2"),
            QAction(QIcon("icons:niwc_3.svg"), "Move to 3"),
            QAction(QIcon("icons:niwc_4.svg"), "Move to 4"),
            QAction(QIcon("icons:niwc_5.svg"), "Move to 5"),
            QAction(QIcon("icons:niwc_all.svg"), "Move to all"),

        )
        self.actions_message_box = (
            QAction(text="Open question dialog"),
            QAction(text="Open information dialog"),
            QAction(text="Open warning dialog"),
            QAction(text="Open critical dialog"),
        )
        self.actions_corner_radius = (QAction(text="rounded"), QAction(text="sharp"))

        action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()
        self.toolbar = QToolBar("Toolbar")
        activitybar = QToolBar("activitybar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_btn_settings, tool_btn_theme, tool_btn_enable, tool_btn_disable, tool_btn_message_box = (
            QToolButton() for _ in range(5)
        )
        spacer = QToolButton()

        # Setup Actions 
        for action in self.actions_page:
            action.setCheckable(True)
            action_group_toolbar.addAction(action)
        self.actions_page[0].setChecked(True)
        
        # Setup Widgets 
        # Setup Widgets 
        menu_toggle = menubar.addMenu("&File")
        activitybar.setMovable(True)
        activitybar.addActions(self.actions_page)
        activitybar.addWidget(spacer)
        activitybar.addWidget(tool_btn_settings)
        self.stack_widget = QStackedWidget()

        # Try initializing and adding maps in tabs
        for _ in range(5):  # assuming 5 tabs for example
            container = QWidget()
            ui = Ui_Form()  # Create an instance of Ui_Form
            ui.setupUi(container)  # Setup the UI in the container
            self.stack_widget.addWidget(container)  # Add the container to the stack widget

                
        self.central_window.setCentralWidget(self.stack_widget)
        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        main_win.setMenuBar(menubar)
        main_win.setStatusBar(statusbar)
        
class MainWindow(QMainWindow):
    
    """ Main window """
    def __init__(self) -> None:
        """Initialization of the MainWindow class."""
        super().__init__()
        QDir.addSearchPath("icons", "./svg")

        self._ui = Navigator()
        self._ui.setup_ui(self)
        self._theme = "dark"
        self._corner_shape = "rounded"
        
        # Signal
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(
                self, "Open File", options=QFileDialog.Option.DontUseNativeDialog
            )
        )
        
        for action in self._ui.actions_page:
            action.triggered.connect(self._change_page)
            
    @Slot()
    def _change_page(self) -> None:
        action_name: str = self.sender().text()  # type: ignore
        if "1" in action_name:
            index = 0
        elif "2" in action_name:
            index = 1
        elif "3" in action_name:
            index = 2
        elif "4" in action_name:
            index = 3
        elif "5" in action_name:
            index = 4 
        else:
            index = 5 # All tab 
        print(f"current tab {index}")
        self._ui.stack_widget.setCurrentIndex(index)