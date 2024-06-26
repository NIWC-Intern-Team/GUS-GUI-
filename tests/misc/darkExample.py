import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import qdarktheme

# Function to enable dark mode in Windows 10+
def enable_windows_dark_mode():
    try:
        # Enable dark mode for windows borders and other elements
        ctypes.windll.dwmapi.DwmSetWindowAttribute.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_uint
        ]
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_MICA_EFFECT = 1029
        
        # Get system's dark mode setting
        dark_mode = ctypes.c_int(1)  # 1 to enable, 0 to disable
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_MICA_EFFECT, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))
    except Exception as e:
        print(f"Failed to set dark mode: {e}")

app = QApplication(sys.argv)

# Apply dark theme
qdarktheme.setup_theme("auto")  # Automatically use dark mode based on system settings

# Enable dark mode for the application window
enable_windows_dark_mode()

main_win = QMainWindow()
main_win.setWindowTitle("PyQt Dark Theme Example")
main_win.resize(300, 200)
push_button = QPushButton("PyQtDarkTheme!!", main_win)
main_win.setCentralWidget(push_button)

main_win.show()
sys.exit(app.exec_())
