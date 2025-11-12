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
