"""
IMPORTS
"""
# Gebruik voor pad
import os
# Generatie van willekeurige waarden (merendeel testen)
import re
# Gebruik voor timer
import time
# Gebruik voor testen van website-URLs.
from urllib.parse import urlparse

# Gebruik voor omzetten van CSV-files.
import pandas as pd
# Gebruik van ophalen van webpagina's.
import requests as req
#Gebruik voor de bulk van web scraping.
from bs4 import BeautifulSoup, Comment
# Gebruik van wiskundige berekening voor gelijkenissen in web-URLs.
from numpy import mean

from Controllers.Repositories.WebScraper_Repository import WebScraperRepo as wsr

# Gebruik van de Progress bar
# Opmerking: installeer hiervoor de laatste versie van 'ipywidgets'. Gebruik hiervoor m.a.w. 'pip install ipywidgets'.


"""
END IMPORTS
"""

contentDIR = 'Storage/'

"""

"""

# Useragent aanmaken
useragent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

class WebScraper():

    """
    CSV-bestanden aanmaken op basis van het Excel-bestand
    """
    def xlsxToCSV():
        provincies = ['Oost-Vl', 'West-Vl', 'Antwerpen', 'Limburg',  'Vl-Brabant']
        for prov in provincies:
            read_file = pd.read_excel (r'prioriteitenlijst.xlsx', sheet_name=prov)
            read_file.to_csv (r'{}.csv'.format(prov), index=None, header=True)


    """
    Creating logs specifically for the webscraper.
    """
    def logScraper(site):
        txt_file = open("logs/logScraper.txt", "a+")
        txt_file.seek(0)
        txt_file.write(str(site))
        txt_file.write('\n')
        txt_file.close()


    """
    Used for retrieving all the combos (Ondernemingsnummer & website)
    """
    def tekstbestandUitschrijven():
        try:
            oldpwd=os.getcwd()

            path = "c:/Users/dylan/DEP2_Repository/ScrapingTools/csv/"
            os.chdir(path)

            df = pd.DataFrame()

            for file in os.listdir():
                if file.endswith('.csv'):
                    aux=pd.read_csv(file, error_bad_lines=False, delimiter=',')
                    df=df.append(aux)

            os.chdir(oldpwd)

            df.to_csv(f"all.csv")

            file = 'all.csv'
            df = pd.read_csv(file)

            cols = ['Ondernemingsnummer', 'Web adres']
            df = df[cols]
            filter = df['Web adres'].notnull()

            df = df[filter]

            df['Ondernemingsnummer'] = df['Ondernemingsnummer'].str.replace(" ", "")

            df.to_csv('ScrapingTools/csv/websites.csv', index=False)
        except:
            print('Niet gelukt om tekstbestand uit te schrijven.')




    # Alle informatie van één website (inclusief alle resterende webpages) opslaan in een tekstbestand.
    # Gold is de verzamelde data van de website.
    def saveAsFile(naam, gold):
        try:
            # Opslaan onder /contents/
            path = contentDIR
            file = naam + '.txt'

            # sommige tekens kunnen niet in een tekstbestand worden opgeslaan
            # speciale tekens verwijderen
            gold = re.sub('[^a-zA-Z0-9 \n\.]', '', gold)

            with open(os.path.join(path,file), "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)

                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0 :
                    file_object.write("\n")

                # Append text at the end of file
                file_object.write(str(gold))
        except:
            # Niet gelukt om bestand op te slaan
            print(f'Niet gelukt om bestand voor {naam} een bestand aan te maken.')

        # Pauze van drie seconden.
        time.sleep(1)

    """
    We'll be excluding tags that only add filler to the webcontentsfiles.
    """
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'nav']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    """
    This function will look up if a webpage falls within the same reach as the other. How similar is the hyperlink to the original site?
    """
    def compareSite(adres1, adres2):
        n = mean(len(adres1) + len(adres2))
        t = 0
        for a, b in zip(adres1, adres2):
            if a == b:
                t += 1
        return t/n > 0.4


    """
    The one and only.
    """
    def siteScraper(adres, og, ondnr, arr=set(), visited=set()):
        try:
            # Op het einde van de rit
            # Resultaten opslaan in een tekstbestand;
            if len(arr) == len(visited) and len(visited) != 0:
                og.split('.')[1]
            elif len(visited) > 20:
                pass
            else:
                #Huidige site op 'bezoekt' plaatsen
                visited.add(adres)

                #Pagina ophalen en soup aanmaken.
                page = req.get(adres, headers=useragent, timeout=10)
                soup = BeautifulSoup(page.content, 'html.parser')

                links = soup.select('a[href]')

                #Alle links ophalen
                for link in links:
                    parsed_url = urlparse(link.get('href')).scheme

                    #mail-links uitsluiten
                    if parsed_url:
                        if WebScraper.compareSite(adres, link.get('href')):
                            arr.add(link.get('href'))
                    else:
                        link = og + link.get('href')
                        arr.add(link)

                soup = BeautifulSoup(page.content, 'html.parser')

                texts = soup.body.findAll(text=True)
                visible_texts = filter(WebScraper.tag_visible, texts)
                collectedData = " ".join(t.strip() for t in visible_texts)
                collectedData = ' '.join(collectedData.split())

                WebScraper.saveAsFile(ondnr.replace(' ', ''), collectedData)

                #Volgende site doorlopen
                for site in arr:
                    if site not in visited:
                        WebScraper.siteScraper(site, og, ondnr, arr, visited)

        except:
            pass


    """
    TODO
    """
    def addWebcontentsToDatabase(compnr, website, companyname):
        wsr.adding_Content(companynr=compnr, website=website)
