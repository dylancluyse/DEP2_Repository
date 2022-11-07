from pymysql import Connect
import pyodbc, psycopg2

#pg_engine = create_engine('postgresql://postgres:DEPgroep1@vichogent.be:40033/testdb')
class Connection():
    def get_conn():
        return psycopg2.connect(database="depdatabase", user="postgres", password="DEPgroep1", host="vichogent.be", port="40033")