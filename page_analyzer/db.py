import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class BaseDB:
    url = None

    def __init__(self):
        self.session = psycopg2.connect(self.url)


class Database(BaseDB):
    url = DATABASE_URL
