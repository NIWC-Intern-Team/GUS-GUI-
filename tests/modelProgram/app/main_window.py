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
from PyQt5 import QtWidgets, QtGui
import os, sys
from app._ui.gusSing_ui import singUI
from app._ui.gusAll_ui import allUI


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources') # to be shifted to resources 
ICON_PATH = os.path.join(RESOURCES_DIR, 'ship.ico')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.csv_handler import csvHandler

class Navigator: 
    """ Navigator Setup """
    def setup_ui(self, main_win: QMainWindow) -> None: 
        
        # Actions     
        try:
            self.actions_page = [
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_1.svg")), "Move to 1"),
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_2.svg")), "Move to 2"),
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_3.svg")), "Move to 3"),
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_4.svg")), "Move to 4"),
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_5.svg")), "Move to 5"),
                QAction(QIcon(os.path.join(RESOURCES_DIR, "niwc_all.svg")), "Move to all")
            ]
        except Exception as e:
            print(f"Error: {e}")
            
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
        statusbar = QStatusBar() # indicate RF Connection? 
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
        menu_toggle = menubar.addMenu("&File")
        menu_toggle = menubar.addMenu("&View")
        menu_toggle = menubar.addMenu("&Options")
        menu_toggle = menubar.addMenu("&Edit")
        menu_toggle = menubar.addMenu("&Help")
        
        # Indication of RF connection - important should be separated 
        
        # statusbar.addPermanentWidget(tool_btn_enable) #
        # statusbar.addPermanentWidget(tool_btn_disable)
         
        # to be read from diagnostics sheet
        if (1):
            statusbar.showMessage("Connected") # swap between connected and disconnected
        else:
            statusbar.showMessage("Disconnected") # swap between connected and disconnected

        activitybar.setMovable(True)
        activitybar.addActions(self.actions_page)
        activitybar.addWidget(spacer)
        activitybar.addWidget(tool_btn_settings)
        self.stack_widget = QStackedWidget()

        try:
            csv_handler = csvHandler()
            # csv_handler.print_data()
            
        except Exception as e:
            print(f"Error: {e}")
            
        tab_list = [allUI, singUI, singUI, singUI, singUI, singUI]
        # Layout 
        for tab, ui in enumerate(tab_list):
            container = QWidget()
            ui().setup_ui(container, csv_handler, tab)
            self.stack_widget.addWidget(container)
            
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

        self._ui = Navigator()
        self._ui.setup_ui(self)
        self._theme = "dark"
        self._corner_shape = "rounded"
        self.setWindowTitle("For the GUS!")
        try: 
            QDir.addSearchPath("icons", "./svg")

            self.setWindowIcon(QtGui.QIcon(ICON_PATH))
            # Signal
            # self._ui.action_open_folder.triggered.connect(
            #     lambda: QFileDialog.getOpenFileName(
            #         self, "Open File", options=QFileDialog.Option.DontUseNativeDialog
            #     )
            # )
        except Exception as e:
            print(f"Error: {e}")
        

            
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
        
        
        
        
        
        
        
        

        