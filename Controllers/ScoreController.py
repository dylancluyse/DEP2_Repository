from Controllers.Repositories.ScoreRepository import ScoreRepository as repo
class ScoreController():
    def updateScores():
        return repo.update_all_scores()

    def get_ranking(compnr):
        return repo.get_all_scores(compnr)