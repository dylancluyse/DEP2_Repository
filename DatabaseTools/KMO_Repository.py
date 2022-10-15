"""
Vaak gebruikte variabelen.
"""
from Storage.Constant_Variables import VGV as vgv


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

from DatabaseTools.Connection_Object import Connection as conn

class KMO(conn.Base):
    __table__ = conn.Base.metadata.tables['KMO']


class Sector(conn.Base):
    __table__ = conn.Base.metadata.tables['Sector']


Session = sessionmaker(bind=conn.engine)
pg_session = Session()


class KMO_Repo():

    """
    Voor de gebruiker makkelijk maken om nieuwe gegevens in te lezen.
    verplichting --> zelfde formaat als in de prioriteitenlijst
    RETURN: Pandas Dataframe.
    """
    def read_CSV():
        if len(os.listdir(vgv.__STORAGE__)) != 0:
            for file in glob.glob('*.csv'):
                return pd.read_csv(file=file)
        else:
            raise Exception('File not found.')

    """
    CSV Importeren
    """
    def KMO_toevoegen(dataframe):
        ...



