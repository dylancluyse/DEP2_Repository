from fastapi import APIRouter
from tensorflow import keras
from keras.models import load_model
import pickle


def get_admin_router(app):
    router = APIRouter()

    @router.get("/admin/keywords")
    def fetch_keywords():
        foo = app.state.admin_repository.fetch_keywords()
        return foo

    @router.get("/admin/foo")
    def add_keywords():
        category_id = 5
        keyword = "FIZZ"
        language = "nl"

        foo = app.state.admin_repository.add_keyword(category_id, keyword, language)
        return foo

    @router.get("/admin/bar")
    def remove_keywords():
        category_id = 5
        keyword = "FIZZ"

        foo = app.state.admin_repository.remove_keyword(category_id, keyword)
        return foo

    @router.get("/admin/predict")
    def predict_score():

        foo = app.state.admin_repository.predict_score(0, 100000, 1000000, 25, 10)
        return foo



    return router
