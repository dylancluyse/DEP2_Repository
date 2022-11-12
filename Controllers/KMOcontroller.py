from Controllers.Repositories.KMO_Repository import KMO_Repo as repo
from Controllers.Repositories.FileController import FileController as fc

class KMO_controller():

    def add_locaties():
        repo.locatie_toevoegen(fc.get_locations_excel())

    def get_ranking(compnr):
        return repo.get_all_scores(compnr)