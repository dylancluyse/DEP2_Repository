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

    @router.get("/admin/keyword/add")
    def add_keywords(category_id: int, keyword: str):
        language = "nl"

        foo = app.state.admin_repository.add_keyword(category_id, keyword, language)
        return foo

    @router.get("/admin/keyword/remove")
    def remove_keywords(category_id: int, keyword: str):
        foo = app.state.admin_repository.remove_keyword(category_id, keyword)
        return foo

    @router.get("/admin/predict")
    def predict_score(urbanisation:float, balance_total:int, revenue:int, employees:int, years:int):

        foo = app.state.admin_repository.predict_score(urbanisation, balance_total, revenue, employees, years)
        return foo



    return router
