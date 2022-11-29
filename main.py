import datetime

from dotenv import load_dotenv
from tqdm import tqdm

from Controllers.AnnualReportsController import NBBScraper as nbs
from Controllers.KMOcontroller import KMO_controller as kmocon
from Controllers.Repositories.ConnectionController import Connection as conn
from Controllers.WebScraperController import WebScraper as wbs

"""
repo objecten
"""
from Controllers.Repositories.FileController import FileController as fcs

CURRENTYEAR = datetime.datetime.now().year

load_dotenv()


class MainApp():

    """
    TODO: Kijken welke bedrijven er een gedateerd jaarverslag hebben.

    Nu wordt een functie YEAR() aangesproken. Met een index misschien beter een extra kolom?

    """
    def get_companies_db():
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        cursor.execute(f"""
        SELECT ondernemingsnummer, website
        FROM "KMO" k
        INNER JOIN "Balans" b on k.ondernemingsnummer = b.ondernemingsnummer
        where date_nbb_report != YEAR({CURRENTYEAR})
        """)


    def updateOne(self, companyNr, site, compname):

        """
        TODO PDF
        1. PDF downloaden.
        2. Gegevens uit PDF halen.
        3. PDF omzetten.
        4. Content PDF naar databank.
        """

        companyNr = companyNr.replace(" ","")

        nbs.download_nbb(companyNr)

        """
        TODO WebScraper
        (1. Uitschrijven naar tekstbestand. (eventueel weglaten))
        1. Site scrapen.
        2. Log schrijven naar tekstbestand.
        3. Webcontents naar databank.
        4. NBB (PDF + CSV) info naar databank.
        """

        if str(site) != 'nan':
            site = 'https://'+str(site)
            wbs.siteScraper(site, site, companyNr, set(), set())
            wbs.logScraper(site)

        """
        TODO
        SQL-queries --> repo functies
        """
        wbs.addWebcontentsToDatabase(compnr=companyNr, website=site, companyname=compname)
        nbs.add_nbb_contents(compnr=companyNr, companyname=compname)


        """
        TODO
        Moving all scrapete files to the backup folder.
        """
        fcs.move_files(companyNr)


    def updateAll(array):

        app = MainApp()

        """
        1. SQL-query uitvoeren dat alle jaarverslagen van het volgende jaar gaat opzoeken.
        ONDNR + site nodig.
        2. Rijen opslaan onder waarde. row[0] = ondnr / row[1] = site
        """
        rows = array

        if len(rows) != 0:
            for row in tqdm(rows):
                compname = row[0]
                compNr = row[1]
                site = row[2]
                app.updateOne(compNr, site, compname=compname)


    def addAll(array):
        app = MainApp()
        rows = array
        if len(rows) != 0:
            teller=0
            for row in tqdm(rows):
                if (teller >= 1618):
                    compname = row[0]
                    compNr = row[1]
                    site = row[2]
                    app.updateOne(compNr, site, compname=compname)
                teller+=1


#MainApp.addAll(fcs.get_companies_sites_excel())

kmocon.add_locaties()
