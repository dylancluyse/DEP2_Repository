from app.repositories import BaseRepository


class SectorRepository(BaseRepository):

    def fetch_sectors(self):
        result, description = self.fetch_all('''SELECT sectornaam from "Sector"''', [])
        return result

    # def fetch_sector(self, sector_naam):
    #     result = self.fetch_all('''SELECT * from "Sector" where "sectornaam" = (%s)''',[sector_naam])
    #     return result

    def fetch_company_by_sector(self, sector_naam):
        result, description = self.fetch_all('''select naam, ondernemingsnummer from "KMO" join "Sector" ON "Sector".sectornummer = "KMO".sectorid WHERE "Sector".sectornaam = (%s)''',[sector_naam])
        # return [company[0] for company in result]
        return [{"naam": company[0], "ondernemingsnummer": company[1]} for company in result]
        # return resrlt


    def fetch_sector_overview(self, naam):
        q = '''SELECT * from "view_sector_overview" WHERE sectornaam = (%s)'''
        v = [naam]
        result, description = self.fetch_all(q, v)

        if result:
            column_names = [column_description[0] for column_description in description]
            res = {k: v for k, v in zip(column_names, result[0])}
            return res
        return {}


    def fetch_subdomain_information(self):
        q = '''SELECT * from "view_categorie_per_domein"'''
        v = []
        result, description = self.fetch_all(q, v)

        if result:
            return {k:v for k,v in result} # {foo: [fizz, buzz], bar: [alice, bob, charlie]}
        return {}

