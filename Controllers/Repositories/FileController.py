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
    """
    def move_files(self):
        if not os.path.isdir(BACKUPFOLDER):
            os.makedirs(BACKUPFOLDER)

        for file_to_move in os.listdir(SCRAPED_FILES):
            arr_types = ['.txt', '.csv', '.pdf']
            if file_to_move.endswith(tuple(arr_types)):
                shutil.move(SCRAPED_FILES + file_to_move, BACKUPFOLDER)