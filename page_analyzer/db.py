import os
from psycopg2.extras import RealDictCursor
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class DB:

    def __init__(self, url=''):
        self.url = url
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def connect(self):
        return self.cur

    def save(self, url):
        sql_command = f"INSERT INTO urls (name) VALUES ('{url}')"
        self.cur.execute(sql_command)
        self.conn.commit()

    def execute(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
