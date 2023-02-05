import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class BaseDatabase:
    url = None

    def __init__(self):
        self.session = psycopg2.connect(self.url)
        self.cursor = self.session.cursor()


class Database(BaseDatabase):
    url = DATABASE_URL
