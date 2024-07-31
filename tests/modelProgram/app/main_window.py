"""Main module of GUS GUI."""
import os, sys
import qdarktheme

from qdarktheme.qtpy.QtCore import QDir, Qt, Slot 
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QIcon, QFont
from qdarktheme.qtpy.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from app._ui.gusSing_ui import singUI
from app._ui.gusAll_ui import allUI
from app._ui.settings_window import SettingsWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources') # to be shifted to resources 
ICON_PATH = os.path.join(RESOURCES_DIR, 'ship.ico')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.csv_handler import csvHandler

class Backend(QObject):
    '''JS access to PyQt backend'''
    datatohtml = pyqtSignal(str)  # Signal to send data to HTML

    @pyqtSlot(str)
    def switch_map_ui_mode(self, ui_mode):
        self.datatohtml.emit(ui_mode)
            
class CustomWebEnginePage(QWebEnginePage):
    '''Used to override JS message method to enable data transfer between frontend and backend'''
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")

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
        
        self.actions_theme = [QAction(theme, main_win) for theme in ["Dark", "Light"]]
        self.actions_font_size = [QAction(font_size, main_win) for font_size in ["Small", "Medium", "Large"]]

        action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()
        self.toolbar = QToolBar("Toolbar")

        activitybar = QToolBar("activitybar")
        statusbar = QStatusBar() # indicate RF Connection? 
        menubar = QMenuBar()
        # tool_btn_settings, tool_btn_theme, tool_btn_enable, tool_btn_disable, tool_btn_message_box = (
        #     QToolButton() for _ in range(5)
        # )
        tool_btn_settings = QToolButton()

        spacer = QToolButton()
        
        # Setup Actions 
        for action in self.actions_page:
            action.setCheckable(True)
            action_group_toolbar.addAction(action)
        self.actions_page[0].setChecked(True)
        
        # Setup Widgets

        # BC (31 July 2024): The File, Edit, and Help top menu items will be implemented sometime in the future

        # menubar.addMenu("&File")
        menu_ui_mode = menubar.addMenu("&UI Mode")
        menu_ui_mode.addActions(self.actions_theme)
        menu_font_size = menubar.addMenu("&Font Size")
        menu_font_size.addActions(self.actions_font_size)
        menu_options = menubar.addMenu("&Options")
        # menubar.addMenu("&Edit")
        # menubar.addMenu("&Help")
         
        menu_options.addActions(
            (self.action_open_folder, self.action_open_color_dialog, self.action_open_font_dialog, self.action_open_ip_dialog)
        )

        # TODO: Read status from diagnostics CSV file
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
        self.settings_window = SettingsWindow()
        self._ui = Navigator()
        self._ui.setup_ui(self)
        self._theme = "dark"
        self._font_size = "medium"
        self._corner_shape = "rounded"
        self.setWindowTitle("For the GUS!")

        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)

        # Setup path to map.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2nd parameter (between current_dir & map.html) can be set to subdir within parent for access to map.html
        html_path = os.path.join(current_dir, '_ui', 'static', 'map.html') 
        self.view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up QWebChannel for communication
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)

        try: 
            QDir.addSearchPath("icons", "./svg")

            self.setWindowIcon(QtGui.QIcon(ICON_PATH))

        except Exception as e:
            print(f"Error: {e}")

        for action in self._ui.actions_font_size:
            action.triggered.connect(self._change_font_size)

        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
                   
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

    def _change_font_size(self) -> None:
            self._font_size = self.sender().text()
            selected_font_size = self._font_size

            group_box = "QGroupBox"
            push_button = "QPushButton"
            menu_bar = "QMenuBar"
            menu_element = "QMenu"
            table_widget = "QTableWidget"
            general_widget = "QWidget"
            text_edit = "QTextEdit"
            tab_bar = "QTabBar"

            if (selected_font_size == "Small"):
                small_font = QFont()
                small_font.setPixelSize(10)
                qApp.setFont(small_font, group_box)
                qApp.setFont(small_font, push_button)
                qApp.setFont(small_font, menu_bar)
                qApp.setFont(small_font, menu_element)
                qApp.setFont(small_font, table_widget)
                qApp.setFont(small_font, general_widget)
                qApp.setFont(small_font, text_edit)
                qApp.setFont(small_font, tab_bar)
            elif (selected_font_size == "Medium"):
                medium_font = QFont()
                medium_font.setPixelSize(14)
                qApp.setFont(medium_font, group_box)
                qApp.setFont(medium_font, push_button)
                qApp.setFont(medium_font, menu_bar)
                qApp.setFont(medium_font, menu_element)
                qApp.setFont(medium_font, table_widget)
                qApp.setFont(medium_font, general_widget)
                qApp.setFont(medium_font, text_edit)
                qApp.setFont(medium_font, tab_bar)
            elif (selected_font_size == "Large"):
                large_font = QFont()
                large_font.setPixelSize(18)
                qApp.setFont(large_font, group_box)
                qApp.setFont(large_font, push_button)
                qApp.setFont(large_font, menu_bar)
                qApp.setFont(large_font, menu_element)
                qApp.setFont(large_font, table_widget)
                qApp.setFont(large_font, general_widget)
                qApp.setFont(large_font, text_edit)
                qApp.setFont(large_font, tab_bar)

    def _change_theme(self):
        self._theme = self.sender().text().lower()
        qdarktheme.setup_theme(self._theme, self._corner_shape)
        self.backend.switch_map_ui_mode(self._theme)
           
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

    # @Slot()
    # def _change_theme(self) -> None:
    #     self._theme = self.sender().text().lower()
    #     qdarktheme.setup_theme(self._theme, self._corner_shape)
        # group_1 = self.children()[4].children()[1].children()[0].children()[1].children()[1].children()[1]
        # group_1_csv_handler = group_1.csv_handler
        # group_1_tab = group_1.tab
        # group_1_test = outerClass._Group1(group_1_csv_handler, group_1_tab)
        # group_1_test.button_test.click()
        #group_1_test.change_theme()
        #group_1().change_theme()
        # self.backend.switch_map_ui_mode("dark")

        # self.backend.switch_map_ui_mode(self._theme)
        # ui_mode_button = self.ui_mode_button
        # ui_mode_selection = ui_mode_button.property("ui_mode")
        # qdarktheme.setup_theme(ui_mode_selection, self._corner_shape)
        # if (ui_mode_selection == "dark"):
        #     ui_mode_button.setProperty("ui_mode", "light")
        #     ui_mode_button.setText("Light mode")
        # else:
        #     ui_mode_button.setProperty("ui_mode", "dark")
        #     ui_mode_button.setText("Dark mode")
        
    @Slot() 
    def _secondary_options(self) -> None:
        print("Secondary screen selected")
