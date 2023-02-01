import os

import psycopg2
from psycopg2.errors import UniqueViolation
from loguru import logger
from dotenv import load_dotenv

from page_analyzer.exceptions import DuplicateURL

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class BaseDatabase:
    url = None

    def __init__(self):
        self.session = psycopg2.connect(self.url)
        self.cursor = self.session.cursor()
        self.__object_id = None


class Database(BaseDatabase):
    url = DATABASE_URL

    @property
    def object_id(self):
        return self.__object_id

    @object_id.setter
    def object_id(self, _id):
        self.__object_id = _id

    def insert(self, query: str, params: tuple) -> int | None:
        try:
            self.cursor.execute(query, params)
        except UniqueViolation:
            select_query = """SELECT id FROM urls WHERE name=%s;"""
            name = (params[0],)
            logger.info(name)
            data = self.select(select_query, name)
            self.object_id = data[0][0]
            raise DuplicateURL

        try:
            _id = self.cursor.fetchone()
            self.session.commit()
            self.object_id = _id[0]
        except psycopg2.ProgrammingError:
            self.session.commit()
            return

    def select(self, query: str, params: str | tuple):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def update(self, query):
        pass
