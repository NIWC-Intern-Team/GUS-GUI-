"""Main module of GUS GUI."""
import os, sys
import qdarktheme

from qdarktheme._util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QIcon, QFont
from qdarktheme.qtpy.QtWidgets import *
from PyQt5 import QtGui
from app._ui.gusSing_ui import singUI
from app._ui.gusAll_ui import allUI
from app._ui.settings_window import SettingsWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources') # to be shifted to resources 
ICON_PATH = os.path.join(RESOURCES_DIR, 'ship.ico')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.csv_handler import csvHandler

class Navigator: 
    """Navigator Setup"""
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
        self.action_open_folder = QAction(QIcon(os.path.join(RESOURCES_DIR,"folder_open_24dp.svg")), "Open folder dialog")
        self.action_open_color_dialog = QAction(QIcon(os.path.join(RESOURCES_DIR,"palette_24dp.svg")), "Open color dialog")
        self.action_open_font_dialog = QAction(
            QIcon(os.path.join(RESOURCES_DIR,"font_download_24dp.svg")), "Open font dialog"
        )  
        self.action_open_ip_dialog = QAction(
            QIcon(os.path.join(RESOURCES_DIR,"ipv2.png")), "Open IP dialog"
        )  
        
        self.actions_theme = [QAction(theme, main_win) for theme in ["dark", "light"]]

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
        menubar.addMenu("&File")
        menu_view = menubar.addMenu("&View")
        menu_view.addActions(self.actions_theme)

        menu_options = menubar.addMenu("&Options")
        menubar.addMenu("&Edit")
        menubar.addMenu("&Help")
         
        menu_options.addActions(
            (self.action_open_folder, self.action_open_color_dialog, self.action_open_font_dialog, self.action_open_ip_dialog)
        )
        # To be read from diagnostics sheet
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
            
        except Exception as e:
            print(f"Error: {e}")
            
        tab_list = [singUI, singUI, singUI, singUI, singUI, allUI]
        
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
        csv_handler = csvHandler()
        self.settings_window = SettingsWindow()


        self._ui = Navigator()
        self._ui.setup_ui(self)
        self._theme = "dark"
        self._corner_shape = "rounded"
        self.setWindowTitle("For the GUS!")
        try: 
            QDir.addSearchPath("icons", "./svg")

            self.setWindowIcon(QtGui.QIcon(ICON_PATH))

        except Exception as e:
            print(f"Error: {e}")
                   
        for action in self._ui.actions_page:
            action.triggered.connect(self._change_page)
            
        # Signal
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(
                self, "Open File", options=QFileDialog.Option.DontUseNativeDialog
            )
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(
                parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog
            )
        )
        self._ui.action_open_font_dialog.triggered.connect(
            lambda: QFontDialog.getFont(
                QFont(), parent=self, options=QFontDialog.FontDialogOption.DontUseNativeDialog
            )
        )  
        self._ui.action_open_ip_dialog.triggered.connect(
            self.openSettings
        )  
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
           
    def openSettings(self):
        self.settings_window.show() 
        
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
    @Slot()
    def _change_theme(self) -> None:
        self._theme = self.sender().text()  # type: ignore
        qdarktheme.setup_theme(self._theme, self._corner_shape)
        
        
    @Slot() 
    def _secondary_options(self) -> None:
        print("Secondary screen selected")
        
