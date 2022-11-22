import enum
import os
import shutil
import pandas as pd
from tika import parser
import re

BACKUPFOLDER="Storage/backup"
SCRAPED_FILES="Storage/"
INPUT="Input/"

class FileController():
    def get_companies_sites_excel():
        return pd.read_excel(INPUT+"kmo's_Vlaanderen_2021.xlsx", index_col=0, sheet_name="Lijst").iloc[: , [0, 6, 10]].to_numpy()

    def get_company_nrs():
        return pd.read_excel(INPUT+"kmo's_Vlaanderen_2021.xlsx", index_col=0, sheet_name="Lijst").iloc[: , [6]].to_numpy()

    def get_locations_excel():
        df = pd.read_excel("Input/kmo's_Vlaanderen_2021.xlsx", index_col=0, sheet_name="Lijst")
        return df.iloc[: , [1, 6, 7, 8]].to_numpy()

    def get_inwoners_csv():
        return pd.read_csv("inwoners.csv").to_numpy()

    """
    Eventueel enkel meegeven als parameter?
    """
    def read_NNB_CSV():
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.csv'):
                return pd.read_csv(SCRAPED_FILES+'/'+file)

    """
    Opgehalen jaarverslag gaan teruggeven als plaintekst.
    """
    def read_NBB_PDF():
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.pdf'):
                raw = parser.from_file(SCRAPED_FILES+'/'+file)
                return re.sub('\W+',' ', raw['content'])

    """
    Tekstbestand inlezen.
    """
    def read_Web_Contents():
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.txt'):
                with open(SCRAPED_FILES + '/' + file, 'r') as file:
                    return re.sub('\W+',' ', file.read().replace('\n', ''))


    """
    Enkel de benodigde bestanden gaan we tijdelijk in de 'Storage' map houden.
    Uiteindelijk moeten alle bestanden ook naar de backupfolder gaan.

    TODO
    Check toevoegen waarbij er wordt gekeken naar de drie subdirs: csv, txt en pdf. Nu wordt er enkel gekeken naar de backupfolder.
    Ervoor zorgen dat alle te downloaden bestanden naar de /Storage folder worden gedownload.
    """
    def move_files(companynr):
        if not os.path.isdir(BACKUPFOLDER):
            for elem in ['/csv', '/txt', '/pdf']:
                os.makedirs(BACKUPFOLDER+elem)

        for file_to_move in os.listdir(SCRAPED_FILES):
            arr_types = ['txt', 'csv', 'pdf']
            if str(file_to_move[-3:]) in arr_types:
                filename = str(companynr).replace(' ','')+'.'+file_to_move[-3:]
                shutil.move(SCRAPED_FILES + file_to_move, BACKUPFOLDER +'/'+file_to_move[-3:]+'/'+filename)

        