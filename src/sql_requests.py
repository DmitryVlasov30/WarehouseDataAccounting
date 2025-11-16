from utils import Result

from sqlite3 import connect
from loguru import logger


class Database:
    def __init__(self, database_path, name_table):
        self.database_path = database_path
        self.connection = connect(database_path)
        self.cursor = self.connection.cursor()
        self.name_table = name_table

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS {self.name_table} (
                "id"	INTEGER NOT NULL UNIQUE,  
                "full_name"  TEXT NOT NULL,
                "short_name"  TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

    def get_data(self):
        return self.cursor.execute(f"""SELECT full_name, short_name FROM {self.name_table}""").fetchall()

    def insert_data(self, full_name, short_name) -> Result:
        try:
            self.cursor.execute(f"""INSERT INTO {self.name_table} ({full_name}, {short_name})""")
            logger.info(f"добавлено сокращение {full_name}, {short_name}")
            return Result.success
        except Exception as ex:
            logger.error(ex)
            return Result.fail

    def delete_data(self, full_name, short_name) -> Result:
        try:
            self.cursor.execute(f"""
                DELETE FROM {self.name_table}
                WHERE full_name = '{full_name}' AND short_name = '{short_name}'""")
            logger.info(f"удалено сокращение {full_name}, {short_name}")
            return Result.success
        except Exception as ex:
            logger.error(ex)
            return Result.fail

