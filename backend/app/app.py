from typing import Union

from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ "http://localhost:3000", "https://localhost:3000", "https://localhost", "http://localhost" ]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/foo")
def read_item():
    # sleep(3)
    out = {
            "items": [
                {"id": 1, "name": "Jannsens Inc."},
                {"id": 2, "name": "Colruyt Groep"},
                {"id": 3, "name": "Willy Naessens"},
                {"id": 4, "name": "Matexi"},
                {"id": 5, "name": "In The Pocket"},
                {"id": 6, "name": "HOGENT"},
            ]
        }
    return {"data": out}

@app.get("/sector/{company_id}")
def read_item(company_id: str):
    out = {
            "items": [
                {"id": 1, "name": company_id},
                {"id": 2, "name": "Colruyt Groep"},
                {"id": 3, "name": "Willy Naessens"},
                {"id": 4, "name": "Matexi"},
                {"id": 5, "name": "In The Pocket"},
                {"id": 6, "name": "HOGENT"},
            ]
        }
    return {"data": out}
