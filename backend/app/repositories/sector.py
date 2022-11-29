from app.repositories import BaseRepository


class SectorRepository(BaseRepository):

    def fetch_sectors(self):
        result = self.fetch_all('''SELECT sectornaam from "Sector"''', [])
        return result

    # def fetch_sector(self, sector_naam):
    #     result = self.fetch_all('''SELECT * from "Sector" where "sectornaam" = (%s)''',[sector_naam])
    #     return result

    def fetch_company_by_sector(self, sector_naam):
        result = self.fetch_all('''select naam, ondernemingsnummer from "KMO" join "Sector" ON "Sector".sectornummer = "KMO".sectorid WHERE "Sector".sectornaam = (%s)''',[sector_naam])
        # return [company[0] for company in result]
        return [{"naam": company[0], "ondernemingsnummer": company[1]} for company in result]
        # return resrlt
