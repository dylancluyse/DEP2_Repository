from app.database import DB


class BaseRepository():
    db = DB

    def __init__(self, db):
        self.db = db

    def get_db(self):
        print(self.db)
        return self.db

    def fetch_all(self, query, values):
        #Creating a cursor object using the cursor() method
        cursor = self.db.conn.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result
