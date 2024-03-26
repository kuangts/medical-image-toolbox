import sys
from PySide6.QtWidgets import QApplication
from . import ui


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ui.AppWindow()
    win.show()
    sys.exit(app.exec())
