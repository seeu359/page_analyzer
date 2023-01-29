import os
from datetime import date

import psycopg2
from dotenv import load_dotenv
from psycopg2.errors import UniqueViolation

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class BaseDB:

    url = None

    def __init__(self):
        self.session = psycopg2.connect(self.url)

    def insert(self, table_name, name) -> int:
        """Insert record into database. Return id of record which has
        been added in database"""
        cursor = self.session.cursor()

        try:
            cursor.execute(
                """INSERT INTO %s (name, created_at) 
                VALUES (%s, %s) RETURNING id;""",
                (table_name, name, date.today())
            )

            record_id = cursor.fetchone()[0]
            self.session.commit()
            return record_id

        except UniqueViolation:  # Подумать, что делать с обработкой ошибок, так как тут может быть куча всего
            self.session.rollback()
            raise UniqueViolation()

    def select(self, _id: int | None = None):
        cursor = self.session.cursor()

        if not _id:
            cursor.execute("""SELECT * FROM urls""")
            data = cursor.fetchall()
            return data

        cursor.execute(
            """SELECT * FROM urls WHERE id=%s;""",
            (_id,)
        )

        data = cursor.fetchone()
        return data if data is not None else None


class Database(BaseDB):

    url = DATABASE_URL
