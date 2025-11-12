import sys
import io

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../projectV1.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())