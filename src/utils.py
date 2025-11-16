import pdfplumber
import pandas as pd
from pprint import pprint
from enum import Enum


class Result(Enum):
    success: str = "success"
    fail: str = "fail"


class ParsePDFTable:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_tables(self):
        tables_dict = {}

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                pprint(len(page_tables))

    def merge_tables(self):
        table_merge = []
        data_tables = list(self.extract_tables().items())
        for i, elem in enumerate(data_tables):
            table_df = elem[1]
            table_name = elem[0]
            if i == 0:
                table_merge.append(str(table_df))
                continue
            if (data_tables[i - 1][1].attrs["page_number"] != table_df.attrs["page_number"]
                    and table_df.attrs["table_number"] == 1):
                print("-" * 50)
                print(str(table_df.attrs["page_number"]))
                table_merge[-1] += "\n" + str(table_df)
                continue
            table_merge.append(str(table_df))

        for el in table_merge:
            elem = el.split("\n")
            data = []
            for line in elem:
                data.append(line.split())

            print(*data, sep="\n")
            print("_"*50)


class Comparison:
    def __init__(self, path_first_table, path_second_table, csv_path_file):
        self.path_first_table = path_first_table
        self.path_second_table = path_second_table
        self.csv_path_file = csv_path_file

    def get_tables(self) -> tuple:
        df_first_table = pd.read_excel(self.path_first_table).values[4:]
        df_second_table = pd.read_excel(self.path_second_table).values[4:]

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

        print(accounting_table)

        return warehouse_table_data, accounting_table

    def comparison_tables(self) -> dict:
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


def main():
    pass


if __name__ == '__main__':
    main()


