"""
Vaak gebruikte variabelen.
"""
from Storage.Constant_Variables import VGV as vgv
import time


"""
IMPORTS
"""
from turtle import pd
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import glob, os

"""
Ik verwijs naar een klasse die de verbinding met de databank aanmaakt. 
Op deze manier vermijden we het constant hergebruiken van dezelfde lijnen code. 
Ook moeten we de verbinding niet telkens op ieder bestand aanpassen.
"""
from Controllers.Repositories.ConnectionController import Connection as conn


class KMO_Repo():

    """
    Voor de gebruiker makkelijk maken om nieuwe gegevens in te lezen.
    verplichting --> zelfde formaat als in de prioriteitenlijst
    RETURN: Pandas Dataframe.
    """
    def read_CSV(self):
        if len(os.listdir(vgv.__STORAGE__)) != 0:
            for file in glob.glob('*.csv'):
                return pd.read_csv(file=file)
        else:
            raise Exception('File not found.')

    """
    CSV Importeren
    """
    def locatie_toevoegen(numpy_array):
        for row in numpy_array:
            print(row)
            companynr = row[1].replace(' ', '')
            gemeente = row[0]
            adres = row[3].replace("'", '')
            postcode = row[2]
            urban = row[4]

            db_conn = conn.get_conn()
            cursor = db_conn.cursor()

            cursor = db_conn.cursor()
            cursor.execute(f"""select * from "Locatie" where gemeente = '{gemeente}' and ondernemingsnummer = {companynr}""")

            rows_id_exist = cursor.fetchall()
            cursor.close()

            if len(rows_id_exist) == 0:

                cursor.execute(f"""
                INSERT INTO "Locatie" (ondernemingsnummer, postcode, gemeente, adres, urban) 
                VALUES ('{companynr}', '{postcode}', '{gemeente}', '{adres}', {urban});
                """)

                db_conn.commit()
                cursor.close()

                time.sleep(2)