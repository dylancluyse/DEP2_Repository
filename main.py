from pandas import array
from tqdm import tqdm
import time

from ScrapingTools.nbbscraper import NBBScraper as nbs
from ScrapingTools.webscraper import WebScraper as wbs


class MainApp():

    def updateOne(companyNr, site):
        nbs.download_pdf(companyNr)
        
        wbs.siteScraper
        time.sleep(1)

        wbs.tekstbestandUitschrijven()
        time.sleep(1)

        wbs.siteScraper(site, site, companyNr, set(), set())
        time.sleep(1)

        wbs.logScraper(site)
        time.sleep(1)


    def updateMany():
        """
        (^-^*)/ TODO
        """


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



MainApp.updateOne('0431 852 314', 'https://www.nedgame.nl')