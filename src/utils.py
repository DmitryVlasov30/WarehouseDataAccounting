import pdfplumber
import pandas as pd


class ParsePDFTable:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_tables(self):
        tables_dict = {}

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()

                for table_num, table in enumerate(page_tables):
                    if table and len(table) > 1:
                        df_data = pd.DataFrame(table)
                        table_name = f"page_{page_num + 1}_table_{table_num + 1}"

                        df_data.attrs['page_number'] = page_num + 1
                        df_data.attrs['table_number'] = table_num + 1
                        df_data.attrs['source_file'] = self.pdf_path

                        tables_dict[table_name] = df_data

        # print("-" * 50)
        # print(str(list(tables_dict.values())[0]))
        # print("-" * 50)

        return tables_dict

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
        #
        # for el in table_merge:
        #     elem = el.split("\n")
        #     data = []
        #     for line in elem:
        #         data.append(line.split())
        #
        #     print(*data, sep="\n")
        #     print("_"*50)


class Comparison:
    def __init__(self, path_first_table, path_second_table, csv_path_file):
        self.path_first_table = path_first_table
        self.path_second_table = path_second_table
        self.csv_path_file = csv_path_file

    def get_tables(self) -> tuple:
        df_first_table = pd.read_excel(self.path_first_table)
        df_second_table = pd.read_excel(self.path_second_table)

        warehouse_table_data, accounting_table = {}, {}
        for warehouse_data in df_first_table:
            warehouse_table_data[warehouse_data[0]] = warehouse_data[1:]

        for accounting_data in df_second_table:
            accounting_table[accounting_data[0]] = accounting_data[1:]

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


