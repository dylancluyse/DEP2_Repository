from app.repositories import BaseRepository


class CompanyRespository(BaseRepository):

    def __init__(self, db):
        self.db = db

    def fetch_all_company_names(self):
        q = '''SELECT naam from "KMO"'''
        v = []
        result = self.fetch_all(q, v)
        return result

    def fetch_company(self, naam):
        q = '''SELECT * from "KMO" where "naam" = (%s)'''
        v = [naam]
        result = self.fetch_all(q, v)
        return result
