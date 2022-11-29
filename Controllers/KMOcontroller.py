from Controllers.Repositories.FileController import FileController as fc
from Controllers.Repositories.KMO_Repository import KMO_Repo as repo


class KMO_controller():

    def add_locaties():
        repo.locatie_toevoegen(fc.get_locations_excel())
