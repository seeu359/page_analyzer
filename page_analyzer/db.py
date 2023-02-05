import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class BaseDatabase:
    url = None

    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = psycopg2.connect(self.url)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.session.close()
        else:
            self.session.rollback()
            self.session.close()


class Database(BaseDatabase):
    url = DATABASE_URL
