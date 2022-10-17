import enum
import os
import shutil
import pandas as pd
from PyPDF2 import PdfReader

BACKUPFOLDER="Storage/backup"
SCRAPED_FILES="Storage/"

class FileController():
    """
    Eventueel enkel meegeven als parameter?
    """
    def read_NNB_CSV(self):
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.csv'):
                return pd.read_csv(file)

    """
    Opgehalen jaarverslag gaan teruggeven als plaintekst.
    """
    def read_NBB_PDF(self):
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.pdf'):
                reader = PdfReader("example.pdf")
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text

    """
    Tekstbestand inlezen.
    """
    def read_Web_Contents(self):
        for file in os.listdir(SCRAPED_FILES):
            if file.endswith('.txt'):
                with open(file, 'r') as file:
                    return file.read().replace('\n', '')


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