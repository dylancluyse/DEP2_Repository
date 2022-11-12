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

    def replace_haakjes(zoekterm):
        # vervang de , en spatie tussen de haakjes in naar een pijl
        # verwijder de haakjes
        pass

    def get_search_string(cat):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        cursor.execute(f"""
                select zoekterm_description
                from "zoektermen"
                where categorie_id = {cat}
        """)

        zoektermen = [list[0] for list in cursor.fetchall()]

        string = ""
        for i, zt in enumerate(zoektermen):
            if i == 0:
                string += str(zt)
            else:
                string += " | " + str(zt)

        return string

    
    def get_score(cat, compnr):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        search_string = KMO_Repo.get_search_string(cat)

        cursor.execute(f"""
                select ts_rank(ts_document, query) as rank 
	            from "KMO", to_tsquery('dutch','({search_string})') query 
	            where query @@ ts_document and ondernemingsnummer = {compnr}
        """)

        resultweb = cursor.fetchone()

        cursor.execute(f"""
                select ts_rank(ts_document, query) as rank 
	            from "Balans", to_tsquery('dutch','({search_string})') query 
                where query @@ ts_document and ondernemingsnummer = {compnr}
        """)

        resultnbb = cursor.fetchone()

        return sum(resultnbb) + sum(resultweb)

    def calc_score(arr):
        n = len(arr)
        for i in range(n):
            if(arr[i] > 0):
                arr[i] = 1
            else:
                arr[i] = 0
        return arr

    def get_all_scores(compnr):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()
        
        cursor.execute(f"""
            SELECT max(categorie_id) FROM categorie_zoektermen
        """)

        max = sum(cursor.fetchone())
        
        arr = []

        for i in range(1, max + 1):
            try:
                arr.append(KMO_Repo.get_score(i, compnr=compnr))
            except:
                arr.append(0)

        E = KMO_Repo.calc_score(arr[0:4])
        S = KMO_Repo.calc_score(arr[5:9])
        G = KMO_Repo.calc_score(arr[9:11])

        return [E, S, G]


