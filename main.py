from pandas import array
from tqdm import tqdm
import time

from ScrapingTools.AnnualReportsController import NBBScraper as nbs
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
        nbs.download_pdf(companyNr)
        

        """
        TODO WebScraper
        1. Uitschrijven naar tekstbestand. (eventueel weglaten)
        2. Site scrapen.
        3. Log schrijven naar tekstbestand.
        4. Content scraper naar databank.
        """

        wbs.tekstbestandUitschrijven()
        time.sleep(1)

        wbs.siteScraper(site, site, companyNr, set(), set())
        time.sleep(1)

        wbs.logScraper(site)
        time.sleep(1)


    def updateAll():

        app = MainApp()

        """
        1. SQL-query uitvoeren dat alle jaarverslagen van het volgende jaar gaat opzoeken.
        ONDNR + site nodig.

        2. Rijen opslaan onder waarde. row[0] = ondnr / row[1] = site
        """

        rows = []

        if len(rows) != 0:
            for row in tqdm(rows):
                app.updateOne(row[0], row[1])



MainApp.updateOne('0431 852 314', 'https://www.unizo.be/')