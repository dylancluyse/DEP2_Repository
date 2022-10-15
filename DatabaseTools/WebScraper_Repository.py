from turtle import pd
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import glob, os

from DatabaseTools import Connection_Object
from Connection_Object import Connection as conn
from Storage.Constant_Variables import VGV as vgv

class WebScraperRepo():
    """
    RETURNS: The contents of the given filename if it exists.
    """
    def readContents(filename):
        f = open(filename, "r")
        return f.read()

    """
    Deletes the file after the contents has been succesfully uploaded to the database.
    """
    def deleteContents(filename):
        ...


    def contents_To_Database(ondnr, content):
        """
        1. Verbinding opstarten
        2. UPDATE-query uitvoeren op databank. Content-veld invullen als het niet bestaat. --> TODO EERD
        3. Commit + close.
        """




    def adding_Content(ondnr):
        filename = ondnr + ".txt"
        if filename not in os.listdir(vgv.__CONTENTS_PATH__):
            raise Exception('File not found.')
        else:

            wsr = WebScraperRepo()

            try:
                content = wsr.readContents(filename)
            except:
                raise Exception('Failed to read data from file.')
            
            """
            
            """
            try:
                wsr.contents_To_Database(ondnr, content)
            except:
                raise Exception('Failed to send data to database.')


            """
            Check if data has been sent to database.
            If so --> delete file to make sure storage doesn't get too hefty.
            """
            wsr.deleteContents(filename)

            


