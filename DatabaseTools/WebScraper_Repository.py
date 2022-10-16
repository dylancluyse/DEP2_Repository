from turtle import pd
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import glob, os

from DatabaseTools import ConnectionController
from DatabaseTools.ConnectionController import Connection as conn
from ScrapingTools.FileController import FileController
from Storage.Constant_Variables import VGV as vgv

class WebScraperRepo():

    def __init__(self) -> None:
        pass
    
    """
    Main-function for this repository. It will follow these steps:
    1. Check if there's a webcontents file and save the contents as a variable 'webcontents'.
    TODO
    2. Store the webcontents to the database using a Postgres-query.
        2.1. Verbinding opstarten
        2.2. UPDATE-query uitvoeren op databank. Content-veld invullen als het niet bestaat. --> EERD
        2.3. Commit + close.
    """
    def adding_Content(ondnr):
        webcontents = FileController().read_Web_Contents



            


