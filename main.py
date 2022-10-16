from pandas import array
from tqdm import tqdm
import time

from ScrapingTools.AnnualReportsController import NBBScraper as nbs
from ScrapingTools.FileController import FileController as fcs
from ScrapingTools.WebScraperController import WebScraper as wbs


class MainApp():

    def updateOne(companyNr, site):
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
        1. Uitschrijven naar tekstbestand. (eventueel weglaten)
        2. Site scrapen.
        3. Log schrijven naar tekstbestand.
        4. Webcontents naar databank.
        5. NBB (PDF + CSV) info naar databank.
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

        wbs.addWebcontentsToDatabase()
        nbs.add_nbb_contents()


        """
        TODO
        Moving all scrapete files to the backup folder.
        """
        fcs.move_files()


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



MainApp.updateOne('0431 852 314', 'https://www.unizo.be/')