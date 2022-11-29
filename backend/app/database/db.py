from typing import Any

import psycopg2

from app.config import config


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
