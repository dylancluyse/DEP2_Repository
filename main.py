from pandas import array
from tqdm import tqdm
import time

from Controllers.AnnualReportsController import NBBScraper as nbs
from Controllers.WebScraperController import WebScraper as wbs

"""
repo objecten
"""
from Controllers.Repositories.WebScraper_Repository import WebScraperRepo as wsr
from Controllers.Repositories.ConnectionController import Connection as conn
from Controllers.Repositories.AnnualReports_Repository import AnnualReportsRepo as arr
from Controllers.Repositories.FileController import FileController as fcs


class MainApp():

    def updateOne(self, companyNr, site):

        """
        TODO PDF
        1. PDF downloaden.
        2. Gegevens uit PDF halen.
        3. PDF omzetten. 
        4. Content PDF naar databank.
        """
        nbs.download_nbb(companyNr)

        """
        TODO WebScraper
        (1. Uitschrijven naar tekstbestand. (eventueel weglaten))
        1. Site scrapen.
        2. Log schrijven naar tekstbestand.
        3. Webcontents naar databank.
        4. NBB (PDF + CSV) info naar databank.
        """
        wbs.tekstbestandUitschrijven()
        time.sleep(1)

        wbs.siteScraper(site, site, companyNr, set(), set())
        time.sleep(1)

        wbs.logScraper(site)
        time.sleep(1)

        """
        TODO
        SQL-queries --> repo functies
        """
        wbs.addWebcontentsToDatabase(compnr=companyNr, email=site)
        nbs.add_nbb_contents(compnr=companyNr)


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
                compNr = row[0]
                site = row[1]
                app.updateOne(compNr, site)


#MainApp.updateOne('0431 852 314', 'https://www.unizo.be/')


MainApp.updateAll(
    [['0431852314', 'https://www.unizo.be/'], ['0404935507', 'https://www.ibrefinery.be'], ['0404534540', 'https://www.ibrefinery.be']]
)