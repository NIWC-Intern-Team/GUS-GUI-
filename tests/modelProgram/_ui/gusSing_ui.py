from __future__ import annotations

import sys
import os 
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QJsonValue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGroupBox, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel

from PyQt5 import uic
from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel, QTextOption
from PyQt5.QtWidgets import (
    QCheckBox,
    QColumnView,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableView,
    QTabWidget,
    QTextEdit,
    QToolBox,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

# JS access to PyQt backend 
class Backend(QObject):
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lng):
        print(f"Latitude: {lat}, Longitude: {lng}")

# Used to override JS message method to enable data transfer bewteen frontend & backend
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print(f"JS: {message} (line {lineNumber}, {sourceId})")


class _Group1(QGroupBox):
    def __init__(self) -> None:
        super().__init__("hopefully a map")
        # self.setGeometry(100, 100, 800, 600)

        # Widgets        
        map_group = QGroupBox("Map & Features")
        group_push = QGroupBox("Push Button")

        push_btn, push_btn_toggled = QPushButton("NORMAL"), QPushButton("TOGGLED")
        push_btn_flat, push_btn_flat_toggled = QPushButton("NORMAL"), QPushButton("TOGGLED")


        # Setup widgets
        self.setCheckable(True)
        push_btn_flat.setFlat(True)
        push_btn_flat_toggled.setFlat(True)
        for btn in (push_btn_toggled, push_btn_flat_toggled):
            btn.setCheckable(True)
            btn.setChecked(True)
            
            
        # Create the QWebEngineView widget
        self.view = QWebEngineView()
        self.page = CustomWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.setMinimumSize(300, 400)

        # Setup path to map.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 2nd parameter (between current_dir & map.html) can be set to subdir within parent for access to map.html
        html_path = os.path.join(current_dir, 'static', 'map.html') 
        self.view.setUrl(QUrl.fromLocalFile(html_path))
        
        # Set up QWebChannel for communication
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.page.setWebChannel(self.channel)
        
        
        
        # Layout
        # Layout setup
        g_map = QGridLayout()

        # Add the view to take up most of the space
        g_map.addWidget(self.view, 1, 0, 1, 3)  # Span across columns if needed

        # Add buttons at the top
        g_map.addWidget(push_btn_flat, 0, 0)  # First row, second column
        g_map.addWidget(push_btn_flat_toggled, 0, 2)  # First row, third column

        self.setLayout(g_map)



class _Group2(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Line boxes")
        # Widgets
        group_spinbox = QGroupBox("Spinbox")
        group_combobox = QGroupBox("Combobox")
        group_editable = QGroupBox("Line edit")
        group_date = QGroupBox("Date time edit")

        spinbox, spinbox_suffix = QSpinBox(), QSpinBox()
        combobox, combobox_line_edit = QComboBox(), QComboBox()
        line_edit = QLineEdit()
        date_time_edit, date_time_edit_calendar = QDateTimeEdit(), QDateTimeEdit()

        # Setup widgets
        self.setCheckable(True)
        spinbox_suffix.setSuffix(" m")

        combobox.addItems(("Item 1", "Item 2", "Item 3"))
        combobox_line_edit.addItems(("Item 1", "Item 2", "Item 3"))
        combobox_line_edit.setEditable(True)

        line_edit.setPlaceholderText("Placeholder text")
        date_time_edit_calendar.setCalendarPopup(True)

        # Layout
        v_layout_spin = QVBoxLayout()
        v_layout_spin.addWidget(spinbox)
        v_layout_spin.addWidget(spinbox_suffix)
        group_spinbox.setLayout(v_layout_spin)

        v_layout_combo = QVBoxLayout()
        v_layout_combo.addWidget(combobox)
        v_layout_combo.addWidget(combobox_line_edit)
        group_combobox.setLayout(v_layout_combo)

        v_layout_line_edit = QVBoxLayout()
        v_layout_line_edit.addWidget(line_edit)
        group_editable.setLayout(v_layout_line_edit)

        v_layout_date = QVBoxLayout()
        v_layout_date.addWidget(date_time_edit)
        v_layout_date.addWidget(date_time_edit_calendar)
        group_date.setLayout(v_layout_date)

        g_layout_main = QGridLayout(self)
        g_layout_main.addWidget(group_spinbox, 0, 0)
        g_layout_main.addWidget(group_combobox, 0, 1)
        g_layout_main.addWidget(group_editable, 1, 0)
        g_layout_main.addWidget(group_date, 1, 1)


class _TableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._data = [[i * 10 + j for j in range(4)] for i in range(5)]

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 1:
            return Qt.CheckState.Checked if index.row() % 2 == 0 else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.EditRole and index.column() == 2:
            return self._data[index.row()][index.column()]  # pragma: no cover
        return None

    def rowCount(self, index) -> int:  # noqa: N802
        return len(self._data)

    def columnCount(self, index) -> int:  # noqa: N802
        return len(self._data[0])

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flag = super().flags(index)
        if index.column() == 1:
            flag |= Qt.ItemFlag.ItemIsUserCheckable
        elif index.column() in (2, 3):
            flag |= Qt.ItemFlag.ItemIsEditable
        return flag  # type: ignore

    def headerData(  # noqa: N802
        self, section: int, orientation: Qt.Orientation, role: int = ...
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return ["Normal", "Checkbox", "Spinbox", "LineEdit"][section]
        return section * 100


class _Group3(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Scroll area and QTabWidget (QGroupBox.flat = True)")

        # Widgets
        tab_widget = QTabWidget()
        tab_text_edit = QTextEdit()
        tab_table = QTableView()
        tab_list = QListWidget()
        tab_tree = QTreeWidget()
        tab_column = QColumnView()
        btn_toggle_alternating = QPushButton("Alternating")

        # Setup widgets
        self.setCheckable(True)
        self.setFlat(True)
        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        tab_text_edit.append("<b>PyQtDarkTheme</b>")
        tab_text_edit.append("Dark theme for PySide and PyQt.")
        tab_text_edit.append("This project is licensed under the MIT license.")
        tab_text_edit.append('<a href="https://pyqtdarktheme.readthedocs.io">PyQtDarkTheme Doc</a>')
        tab_text_edit.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        tab_table.setModel(_TableModel())
        tab_table.setSortingEnabled(True)

        tab_list.addItems([f"Item {i+1}" for i in range(30)])

        tab_tree.setColumnCount(2)
        for i in range(5):
            item = QTreeWidgetItem([f"Item {i+1}" for _ in range(2)])
            for j in range(2):
                item.addChild(QTreeWidgetItem([f"Child Item {i+1}_{j+1}" for _ in range(2)]))
            tab_tree.insertTopLevelItem(i, item)

        tab_column_model = QStandardItemModel()
        tab_column_model.setHorizontalHeaderLabels(("Header 1", "Header 2"))
        for row in range(5):
            item = QStandardItem(f"Item {row+1}")
            for column in range(15):
                item.setChild(column, QStandardItem(f"Child Item {row+1}_{column+1}"))
            tab_column_model.setItem(row, item)
        tab_column.setModel(tab_column_model)

        def toggle_alternating(checked: bool):
            tab_table.setAlternatingRowColors(checked)
            tab_list.setAlternatingRowColors(checked)
            tab_tree.setAlternatingRowColors(checked)
            tab_column.setAlternatingRowColors(checked)

        btn_toggle_alternating.setCheckable(True)
        btn_toggle_alternating.toggled.connect(toggle_alternating)
        btn_toggle_alternating.setChecked(True)

        # layout
        tab_widget.addTab(tab_table, "Table")
        tab_widget.addTab(tab_text_edit, "Text Edit")
        tab_widget.addTab(tab_list, "List")
        tab_widget.addTab(tab_tree, "Tree")
        tab_widget.addTab(tab_column, "Column")

        v_layout_main = QVBoxLayout(self)
        v_layout_main.addWidget(tab_widget)
        v_layout_main.addWidget(btn_toggle_alternating)


class _Group4(QGroupBox):
    def __init__(self) -> None:
        super().__init__("QToolBox")
        # Widgets
        toolbox = QToolBox()
        h_slider, v_slider = QSlider(Qt.Orientation.Horizontal), QSlider(Qt.Orientation.Vertical)
        dial_ticks = QDial()
        progressbar = QProgressBar()
        lcd_number = QLCDNumber()

        # Setup widgets
        self.setCheckable(True)
        # If the slider value is 50, it is not clear which orientation is active.
        h_slider.setValue(30)
        v_slider.setValue(30)
        dial_ticks.setNotchesVisible(True)
        progressbar.setValue(50)
        lcd_number.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        lcd_number.display(123)

        # Layout
        slider_component = QWidget()
        v_layout = QVBoxLayout(slider_component)
        v_layout.addWidget(h_slider)
        v_layout.addWidget(v_slider)
        toolbox.addItem(slider_component, "Slider")
        toolbox.addItem(dial_ticks, "Dial")
        toolbox.addItem(progressbar, "Progress Bar")
        toolbox.addItem(lcd_number, "LCD Number")
        QVBoxLayout(self).addWidget(toolbox)






class singUI:
    """The ui class of widgets window. nice :-D"""

    def setup_ui(self, win: QWidget) -> None:
        """Set up ui."""
        # Widgets
        h_splitter_1, h_splitter_2 = QSplitter(Qt.Orientation.Horizontal), QSplitter(
            Qt.Orientation.Horizontal
        )

        # Setup widgets
        h_splitter_1.setMinimumHeight(100)  # Fix bug layout crush

        # Layout
        h_splitter_1.addWidget(_Group1())
   

        widget_container = QWidget()
        v_layout = QVBoxLayout(widget_container)
        v_layout.addWidget(h_splitter_1)
        v_layout.addWidget(h_splitter_2)

        scroll_area = QScrollArea()
        scroll_area.setWidget(widget_container)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.addWidget(scroll_area)
