from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    path_log: str = rf"{BASE_DIR}\all_logs.log"
    path_sql_database: str = rf"{BASE_DIR}\units_data.db"
    name_table: str = "main_table"
    invoices_table: str = "invoices_table"
    csv_path_file: str = rf"{BASE_DIR}\output_pdf.csv"
    excel_result_file: str = rf"{BASE_DIR}\result_file.xlsx"
    csv_path_comp: str = rf"{BASE_DIR}\comp_file.csv"
    excel_comp_result: str = rf"{BASE_DIR}\result_file_comp2.xlsx"


settings = Settings()
