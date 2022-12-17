from app.repositories import BaseRepository


class CompanyRespository(BaseRepository):

    def __init__(self, db):
        self.db = db

    def fetch_all_company_names(self):
        q = '''SELECT naam from "KMO"'''
        v = []
        result, description = self.fetch_all(q, v)
        return result

    def fetch_company(self, naam):
        q = '''SELECT ondernemingsnummer, naam, website, wcm, vennootschap, soortbusiness, sectorid, personeelsbestanden, beursgenoteerd, foundingdate, environment, social, governance from "KMO" where "naam" = (%s)'''
        v = [naam]
        result, description= self.fetch_all(q, v)
        if result:
            result = result[0]
            result = {
                    "ondernemingsnummer":result[0],
                    "naam":result[1],
                    "website":result[2],
                    "wcm":result[3],
                    "vennootschap":result[4],
                    "soortbusiness":result[5],
                    "sectorid":result[6],
                    "personeelsbestanden":result[7],
                    "beursgenoteerd":result[8],
                    "foundingdate":result[9],
                    "environment":result[10],
                    "social":result[11],
                    "governance":result[12],
                    }
        return result

    def fetch_company_view(self, naam):
        q = '''SELECT * from "view_website_data" WHERE ondernemingsnummer = (%s)'''
        v = [naam]
        result, description = self.fetch_all(q, v)

        column_names = [column_description[0] for column_description in description]
        res = {k: v for k, v in zip(column_names, result[0])}
        return res
