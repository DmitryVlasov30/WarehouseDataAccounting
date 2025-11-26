import sys
import os

from config import settings
from sql_requests import Database
from utils import Comparison, ParsePDFTable

from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import shutil

from loguru import logger


logger.add(settings.path_log, level="DEBUG")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../projectV1.ui", self)
        self.setWindowTitle("project 1")

        self.path_first_table = None
        self.path_second_table = None
        self.pdf_file = None

        self.comparison_page = self.Comparison
        self.search_page = self.Search

        self.update_table()

        self.import_warehouse_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "get_excel_table_1")
        self.import_warehouse_btn.clicked.connect(self.import_first_table)

        self.import_accounting_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "get_excel_table_2")
        self.import_accounting_btn.clicked.connect(self.import_second_table)

        self.comp_data = self.comparison_page.findChild(QtWidgets.QPushButton, "Comparison_btn")
        self.comp_data.clicked.connect(self.comparison_table)

        self.add_unit_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "addUnitBtn")
        self.add_unit_btn.clicked.connect(self.add_measurement_unit)

        self.delete_unit_btn = self.comparison_page.findChild(QtWidgets.QPushButton, "DeleteUnitBtn")
        self.delete_unit_btn.clicked.connect(self.delete_measurement_unit)

        self.export_pdf = self.comparison_page.findChild(QtWidgets.QPushButton, "excel_save")
        self.export_pdf.clicked.connect(self.export_result_excel_table)

        self.import_pdf = self.comparison_page.findChild(QtWidgets.QPushButton, "get_pdf_file")
        self.import_pdf.clicked.connect(self.get_pdf_data)

    @logger.catch
    def import_first_table(self, flag):
        self.path_first_table, _ = QtWidgets.QFileDialog.getOpenFileName()
        if not self.path_first_table:
            return
        label_first = self.comparison_page.findChild(QtWidgets.QLabel, "first_table")
        label_first.setText("""<html><head/><body><p><span style=' font-size:10pt;
         font-weight:600;'>Складская таблица: сохранена</span></p></body></html>""")

    @logger.catch
    def import_second_table(self, flag):
        self.path_second_table, _ = QtWidgets.QFileDialog.getOpenFileName()
        if not self.path_second_table:
            return
        label_second = self.comparison_page.findChild(QtWidgets.QLabel, "second_table")
        label_second.setText("""<html><head/><body><p><span style=' font-size:10pt;
         font-weight:600;'>Бухгалтерская таблица: сохранена</span></p></body></html>""")

    @logger.catch
    def comparison_table(self, flag):
        label_error = self.comparison_page.findChild(QtWidgets.QLabel, "error_message")
        if not (self.path_first_table and self.path_second_table):
            label_error.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Вы не загрузили две таблицы</span></p></body></html>
                    """)
            return

        save_path, _ = QtWidgets.QFileDialog.getSaveFileName()
        table = self.comparison_page.findChild(QtWidgets.QTableWidget, "Comparison_result")

        comp = Comparison(self.path_first_table,
                          self.path_second_table)

        self.path_first_table = None
        self.path_second_table = None

        data = comp.comparison_data()
        if not data:
            table.clearContents()

        table.setRowCount(0)
        table.setRowCount(len(data))

        for row, row_data in enumerate(data):
            arr = [row_data["id_item"]]
            arr += row_data["data"]
            row_data = arr
            for col, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                table.setItem(row, col, item)

        try:
            save_path = save_path.split("/")
            name_file = save_path[-1]
            directory = save_path[:-1]

            directory_excel = "/".join(settings.excel_result_file.split("/")[:-1])

            name_file += ".xlsx"
            new_path_file = directory_excel + name_file
            os.rename(settings.excel_comp_result, new_path_file)
            shutil.move(new_path_file, "/".join(directory))
        except Exception as ex:
            logger.error(ex)

    def add_measurement_unit(self, flag):
        full_unit = self.comparison_page.findChild(QtWidgets.QLineEdit, "fullInputUnit").text().strip()
        short_unit = self.comparison_page.findChild(QtWidgets.QLineEdit, "shortInputUnit").text().strip()
        message_answer = self.comparison_page.findChild(QtWidgets.QLabel, "resultMessage")

        try:
            db = Database(settings.path_sql_database, settings.name_table)
            db.insert_data(full_unit, short_unit)
        except Exception as ex:
            message_answer.setText("""<html><head/>
                            <body><p><span style=' font-size:10pt;
                            font-weight:600;'>Ошибка</span></p></body></html>""")
            logger.error(ex)
            return

        message_answer.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Сокращение добавлено</span></p></body></html>""")

        self.comparison_page.findChild(QtWidgets.QLineEdit, "fullInputUnit").clear()
        self.comparison_page.findChild(QtWidgets.QLineEdit, "shortInputUnit").clear()

        self.update_table()

    def delete_measurement_unit(self, flag):
        full_unit = self.comparison_page.findChild(QtWidgets.QLineEdit, "fullInputUnit").text().strip()
        short_unit = self.comparison_page.findChild(QtWidgets.QLineEdit, "shortInputUnit").text().strip()
        message_answer = self.comparison_page.findChild(QtWidgets.QLabel, "resultMessage")

        try:
            db = Database(settings.path_sql_database, settings.name_table)
            db.delete_data(full_unit, short_unit)
        except Exception as ex:
            message_answer.setText("""<html><head/>
                            <body><p><span style=' font-size:10pt;
                            font-weight:600;'>Ошибка</span></p></body></html>""")
            logger.error(ex)
            return

        message_answer.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Сокращение удалено</span></p></body></html>""")

        self.comparison_page.findChild(QtWidgets.QLineEdit, "fullInputUnit").clear()
        self.comparison_page.findChild(QtWidgets.QLineEdit, "shortInputUnit").clear()

        self.update_table()

    def update_table(self):
        try:
            db = Database(settings.path_sql_database, settings.name_table)
            data = list(map(lambda el: list(el), db.get_data()))

            table = self.comparison_page.findChild(QtWidgets.QTableWidget, "unitTable")
            if not data:
                table.clearContents()

            table.setRowCount(0)
            table.setRowCount(len(data))
            if data:
                num_cols = len(data[0])
                table.setColumnCount(num_cols)

            for idx, items in enumerate(data):
                items[0] = idx + 1

            for row, row_data in enumerate(data):
                for col, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    table.setItem(row, col, item)

        except Exception as e:
            print(f"Ошибка при обновлении таблицы: {e}")

    def get_pdf_data(self, flag):
        try:
            self.pdf_file, _ = QtWidgets.QFileDialog.getOpenFileName()
            label_error = self.comparison_page.findChild(QtWidgets.QLabel, "error_message")

            parser = ParsePDFTable(self.pdf_file, settings.csv_path_file, settings.excel_result_file)
            parser.transform_pdf_to_excel()

            label_error.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Данные сохранены, можете выгружать данные из номенклатуры</span></p></body></html>
                    """)
        except Exception as e:
            print(e)

    def export_result_excel_table(self, flag):
        label_error = self.comparison_page.findChild(QtWidgets.QLabel, "error_message")
        if self.pdf_file is None:
            label_error.setText("""<html><head/>
                        <body><p><span style=' font-size:10pt;
                        font-weight:600;'>Перед выгрузкой данных нужно отправить номенклатуру</span></p></body></html>
                    """)
            return

        save_path, _ = QtWidgets.QFileDialog.getSaveFileName()
        try:
            save_path = save_path.split("/")
            name_file = save_path[-1]
            directory = save_path[:-1]

            directory_excel = "/".join(settings.excel_result_file.split("/")[:-1])

            name_file += ".xlsx"
            new_path_file = directory_excel + name_file
            os.rename(settings.excel_result_file, new_path_file)
            shutil.move(new_path_file, "/".join(directory))
            self.pdf_file = None
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())