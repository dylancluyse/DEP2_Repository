from Controllers.Repositories.KMO_Repository import KMO_Repo as repo
from Controllers.Repositories.FileController import FileController as fc

class KMO_controller():

    def add_locaties():
        repo.locatie_toevoegen(fc.get_locations_excel())

    def add_urbanisation():
        repo.urbanisatieToevoegen(fc.get_inwoners_csv())

    def add_oprichtingsjaar():
        repo.oprichtingsjaarToevoegen(fc.get_companies_sites_excel())

    def add_beursnotatie():
        repo.beursnotatieToevoegen(fc.get_companies_sites_excel())