import os
from pymysql import Connect
import pyodbc, psycopg2
from config import config

class Connection():
    def get_conn(self):
        return psycopg2.connect(database=config.DATABASE, user=config.USER, password=config.PASSWORD, host=config.HOST, port=config.PORT)
