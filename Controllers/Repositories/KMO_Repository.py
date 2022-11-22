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
            try:
                companynr = row[1].replace(' ', '')
                gemeente = row[0]
                adres = row[3].replace('\W', '')
                postcode = row[2]
                urban = row[4]

                db_conn = conn.get_conn()
                cursor = db_conn.cursor()

                cursor = db_conn.cursor()
                cursor.execute(f"""select * from "Locatie" where gemeente = '{gemeente}' and ondernemingsnummer = {companynr}""")

                rows_id_exist = cursor.fetchall()

                if len(rows_id_exist) == 0:

                    cursor.execute(f"""
                    INSERT INTO "Locatie" (ondernemingsnummer, postcode, gemeente, adres, urban) 
                    VALUES ('{companynr}', '{postcode}', '{gemeente}', '{adres}', {urban});
                    """)

                    db_conn.commit()
            except:
                print(f"Niet gelukt!")

    def urbanisatieToevoegen(numpy_array):
        df = pd.read_csv('gemeente_verstedelijking.csv')
        df = df.to_numpy()
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        for row in df:
            gemeente = str(row[0]).upper()
            urbanisatie = row[1]

            print(f"""
                update "Locatie"
                set urban = '{urbanisatie}'
                where gemeente = {gemeente}
            """)

            cursor.execute(f"""
                update "Locatie"
                set urban = {urbanisatie}
                where gemeente = '{gemeente}'
            """)
            db_conn.commit()
        cursor.close()

    def oprichtingsjaarToevoegen():
        """
        VATS = pd.read_excel("C:/DEP2_Repository/Input/kmo's_Vlaanderen_2021.xlsx", index_col=0, sheet_name="Lijst").iloc[: , [6]].to_numpy()
        f = open("test.csv", "a")
        f2 = open("nonexistent.csv","a")
        f.write("companyvat,startdate,")
        for company_VAT in VATS:
            for e in company_VAT:
                e = str(e).replace(' ','')
                f.write(f"{e},")
                r = requests.get(f"https://www.btw-opzoeken.be/VATSearch/Search?KeyWord={e}&currentSite=www.btw-opzoeken.be")
                
                if(r.json()):
                    startdate = r.json()[0].get("StartDate")
                    f.write(f"{startdate}\n")
                    print(f"{e}: {startdate}" )
                else:
                    f2.write(f"{e}")
                    print(f"{e} is stopgezet")
        f.close()
        f2.close()
        """
        df = pd.read_csv('alle_oprichtingsjaren.csv')
        df['startdate'] = pd.to_datetime(df['startdate'], format="%d-%m-%Y")
        df = df.to_numpy()

        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        for row in df:
            companynr = row[0]
            date = row[1]
            cursor.execute(f"""
                update "KMO"
                set foundingdate = '{date}'
                where ondernemingsnummer = {companynr}
            """)
            db_conn.commit()
        cursor.close()

    def beursnotatieToevoegen():
        df = pd.read_csv('convertcsv.csv').to_numpy()
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        for row in df:
            ondnr = str(row[2]).replace('.','')

            cursor.execute(f"""
            UPDATE "KMO" 
            SET beursgenoteerd = true
            where ondernemingsnummer = {ondnr}
            """)
            db_conn.commit()
        cursor.close()