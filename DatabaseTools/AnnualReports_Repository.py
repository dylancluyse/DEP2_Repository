from ScrapingTools.FileController import FileController
from Connection_Object import Connection




class AnnualReportsRepo():

    def __init__(self):
        pass

    """
    TODO 
    Python-code: De nodige info uit het csv-bestand ophalen. 
    SQL-query: De rij (afhankelijk van het ondernemingsnummer) wordt dan geüpdatet.
    """
    def add_NBB_CSV():
        csv_contents = fc.read_NNB_CSV()

    """
    TODO
    De plaintekst met een SQL-query gaan invoeren in de databank (afhankelijk van het ondernemingsnummer).
    """
    def add_NBB_PDF():
        pdf_contents = fc.read_NBB_PDF()

fc = FileController()