import sys
from config import settings
from sql_requests import Database

from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from utils import Comparison

from loguru import logger


logger.add(settings.log_file, level="DEBUG")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../projectV1.ui", self)
        self.setWindowTitle("project 1")

        self.path_first_table = None
        self.path_second_table = None

        self.comparison_page = self.Comparison
        self.search_page = self.Search
        self.analysis_page = self.Analise

        self.comparison_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "Comparison_btn")
        self.comparison_btn.clicked.connect(self.export_comparison_table)

        self.import_warehouse_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "get_excel_table_1")
        self.import_warehouse_btn.clicked.connect(self.import_first_table)

        self.import_accounting_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "get_excel_table_2")
        self.import_accounting_btn.clicked.connect(self.import_second_table)

        self.comp_data = self.comparison_page.findChild(QtWidgets.QPushButton, "Comparison_btn")
        self.comp_data.clicked.connect(self.comparison_table)

    def export_comparison_table(self):
        pass

    @logger.catch
    def import_first_table(self):
        self.path_first_table, _ = QtWidgets.QFileDialog.getOpenFileName()
        label_first = self.comparison_page.findChild(QtWidgets.QLabel, "first_table")
        label_first.setText("""<html><head/><body><p><span style=' font-size:10pt;
         font-weight:600;'>Первая таблица: сохранена</span></p></body></html>""")

    @logger.catch
    def import_second_table(self):
        self.path_second_table, _ = QtWidgets.QFileDialog.getOpenFileName()
        label_second = self.comparison_page.findChild(QtWidgets.QLabel, "second_table")
        label_second.setText("""<html><head/><body><p><span style=' font-size:10pt;
         font-weight:600;'>Вторая таблица: сохранена</span></p></body></html>""")

    @logger.catch
    def comparison_table(self):
        label_error = self.comparison_page.findChild(QtWidgets.QLabel, "error_message")
        if not (self.path_first_table and self.path_second_table):
            label_error.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Вы не загрузили две таблицы</span></p></body></html>
                    """)
            return

        comp = Comparison(self.path_first_table,
                          self.path_second_table,
                          r"C:\Users\diwex\PycharmProjects\WarehouseDataAccounting\src\output.csv")
        print(comp.comparison_tables())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())