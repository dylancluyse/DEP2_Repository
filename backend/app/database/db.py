from typing import Any
from config import config
import psycopg2

class DB():
    conn: Any

    def setup(self):
        self.conn = psycopg2.connect(
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD,
            host=config.HOST, 
            port=config.PORT
        )

