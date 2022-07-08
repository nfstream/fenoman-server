import pymysql
from patterns.singleton import singleton
from configuration.database_configuration import *
import csv


@singleton
class Database:
    def __init__(self):
        self.__connection = None

    def connect(self):
        self.__connection = pymysql.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE
        )

    def query_tables(self):
        # végig kell iterálni és lekérdezni a táblákat és elhozni az adatokat
        for table in TABLES:
            query_str = f"SELECT * FROM {table}"

            cursor = self.__connection.cursor()
            cursor.execute(query_str)

            rows = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            data_file = open(f"./data/{table}.csv", 'w', encoding='UTF-8')

            data_file_csv = csv.writer(data_file, lineterminator='\n')
            data_file_csv.writerow(column_names)
            data_file_csv.writerows(rows)

            data_file.close()

    def close(self) -> None:
        self.__connection.close()
