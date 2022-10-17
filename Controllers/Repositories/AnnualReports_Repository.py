#from Repositories.FileController import FileController as fc
#from ConnectionController import Connection as conn

class AnnualReportsRepo():

    def __init__(self):
        pass

    """
    TODO 
    Python-code: De nodige info uit het csv-bestand ophalen. 
    SQL-query: De rij (afhankelijk van het ondernemingsnummer) wordt dan geüpdatet.
    """
    def add_NBB_CSV(self, fileRepo):
        csv_contents = fileRepo.read_NNB_CSV()

    """
    TODO
    De plaintekst met een SQL-query gaan invoeren in de databank (afhankelijk van het ondernemingsnummer).
    """
    def add_NBB_PDF(self, fileRepo):
        pdf_contents = fileRepo.read_NBB_PDF()