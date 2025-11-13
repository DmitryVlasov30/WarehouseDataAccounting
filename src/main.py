import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../projectV1.ui", self)

        self.comparison_page = self.Comparison
        self.search_page = self.Search
        self.analysis_page = self.Analise

        self.comparison_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "Comparison_btn")
        self.comparison_btn.clicked.connect(self.export_comparison_table)

        self.import_warehouse_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "get_excel_table_1")
        self.import_warehouse_btn.clicked.connect(self.import_comparison_table)

    def export_comparison_table(self):
        pass

    def import_comparison_table(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())