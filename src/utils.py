from PyPDF2 import PdfReader
import pandas as pd
from enum import Enum
import re
from csv import writer

from config import settings
from sql_requests import Database


class Result(Enum):
    success: str = "success"
    fail: str = "fail"


class ParsePDFTable:
    def __init__(self, pdf_path, csv_path, excel_output_path):
        self.pdf_path = pdf_path
        self.csv_path = csv_path
        self.excel_output_path = excel_output_path

        self.split_number = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"
        self.russian_al = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    def parse_page_data(self, text) -> list:
        records = re.split(r'\n(?=\d+~\d+~\d+~\d+\s*/)', text.strip())

        parsed_data = []
        for record in records:
            if "Total items released" in record:
                record = record.split("Total items released")[0].strip()
            data = record.replace("\n", "").split()
            released = data[-1]
            to_be_released = data[-2]
            name = data[-3]
            code = data[-4]
            nomenclature = data[-5]
            string_info = " ".join([nomenclature, code, name, to_be_released, released])
            information = ""
            model = ""
            if record.split(string_info)[0]:
                information = record.split(string_info)[0]
                if information[-1] + information[-2] != "  ":
                    split_information = information.split()
                    model = split_information[-1]
                    information = information.split(model)[0]
            information = information.strip().replace("\n", "")

            idx_sep = -1
            for idx, char in enumerate(information):
                if char.lower() in self.russian_al:
                    idx_sep = idx
                    break
            russia = information[idx_sep:]
            account_id = information.split("/")[0].strip()
            parsed_data.append({
                "account": account_id,
                "info": russia.replace("\n", ""),
                "model": model,
                "nomenclature": nomenclature,
                "code": code,
                "name": name,
                "to_be_released": to_be_released,
                "released": released
            })
        return parsed_data

    def parse_pages(self):
        pages_table = []
        with open(self.pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                info = page.extract_text().split(self.split_number)[1][1:]
                for item in self.parse_page_data(info):
                    pages_table.append(item)
        return pages_table

    @staticmethod
    def translate_unit(unit):
        return unit

    def process_info(self):
        output_data = self.parse_pages()
        with open(self.csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer_info = writer(csv_file)
            writer_info.writerow(["no", "название", "номер номенклатуры", "единица измерения", "кол-во"])
            for number, item in enumerate(output_data):
                unit_name = self.translate_unit(unit=item["name"])
                writer_info.writerow([number + 1, item["info"], item["nomenclature"], unit_name, item["released"]])

    def transform_pdf_to_excel(self):
        self.process_info()
        dataframe = pd.read_csv(self.csv_path)
        dataframe.to_excel(self.excel_output_path, index=False)


class Comparison:
    def __init__(self, path_first_table, path_second_table):
        self.path_first_table = path_first_table
        self.path_second_table = path_second_table

    def get_tables(self) -> tuple:
        df_first_table = pd.read_excel(self.path_first_table).values[4:]
        df_second_table = pd.read_excel(self.path_second_table).values[3:]

        warehouse_table_data, accounting_table = {}, {}
        for warehouse_data in df_first_table:
            warehouse_data = list(warehouse_data)
            if warehouse_data[1] in warehouse_table_data:
                warehouse_table_data[warehouse_data[1]][-1] += warehouse_data[-1]
                continue
            warehouse_table_data[warehouse_data[1]] = warehouse_data[2:]

        for accounting_data in df_second_table:
            accounting_data = list(accounting_data)
            if accounting_data[1] in accounting_table:
                accounting_table[accounting_data[1]][-1] += accounting_data[-1]
                continue
            new_array = [accounting_data[2], accounting_data[4], accounting_data[5]]
            accounting_table[accounting_data[1]] = new_array

        return warehouse_table_data, accounting_table

    def transformation_tables(self) -> dict:
        warehouse_table_data, accounting_table = self.get_tables()
        mismatch_elems = set()
        result = {}

        for name, data in warehouse_table_data.items():
            if name not in accounting_table or accounting_table[name] != data:
                mismatch_elems.add(name)

        for name, data in accounting_table.items():
            if name not in warehouse_table_data or warehouse_table_data[name] != data:
                mismatch_elems.add(name)

        for name in mismatch_elems:
            result[name] = [
                warehouse_table_data.get(name, "Not found"),
                accounting_table.get(name, "Not found")
            ]

        return result

    def comparison_data(self):
        tables = self.transformation_tables()
        mismatch_elems = []

        db = Database(settings.path_sql_database, settings.name_table)
        swap_data = dict([(data[1], data[2]) for data in db.get_data()])

        for name, data in tables.items():
            warehouse_data, accounting_data = data
            if warehouse_data == "Not found":
                warehouse_table = ["N/A", "N/A", "N/A"]
                accounting_table = data[1]
                mismatch_elems.append(accounting_table + warehouse_table)
                continue
            if accounting_data == "Not found":
                accounting_table = ["N/A", "N/A", "N/A"]
                warehouse_table = data[0]
                mismatch_elems.append(accounting_table + warehouse_table)
                continue

            if accounting_data[1].replace(".", "").replace(",", "").strip() in swap_data:
                accounting_data[1] = swap_data[accounting_data[1]]
            print(swap_data)
            print(accounting_data, warehouse_data)
            if accounting_data != warehouse_data:
                mismatch_elems.append(accounting_data + warehouse_data)
                print(1)
        return mismatch_elems


if __name__ == '__main__':
    pass

