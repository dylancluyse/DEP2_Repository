
from app.database import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.repositories.company import CompanyRespository
from app.repositories.sector import SectorRepository

app = FastAPI()
app.state.db = DB()
app.state.db.setup()
app.state.company_repository = CompanyRespository(db=app.state.db)
app.state.sector_repository = SectorRepository(db=app.state.db)


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
    ondernemingsnummer = "419119578"
    company = app.state.company_repository.fetch_company_view(ondernemingsnummer)
    print(company)
    return {"data": company}

@app.get("/sector") # alle sectors
def get_all_sectors():
    sectors = app.state.sector_repository.fetch_sectors()
    return {"data": sectors}

@app.get("/sector/{sector_name}") # specifieke sectors
def get_sector_by_name(sector_name: str, alphabetical: bool = False):
    print(alphabetical)
    if alphabetical:
        sector = app.state.sector_repository.fetch_company_by_sector_by_name(sector_name)
    else:
        sector = app.state.sector_repository.fetch_company_by_sector_by_score(sector_name)
    return {"data": sector}

@app.get("/sector/data/{sector_name}") # specifieke sectors
def get_sector_data_by_name(sector_name: str):
    sector = app.state.sector_repository.fetch_sector_overview(sector_name)
    return {"data": sector}

@app.get("/company") # alle companies
def get_all_companies():
    companylist = app.state.company_repository.fetch_all_company_names()
    return {"data": companylist}

@app.get("/company/{company_id}") # specifieke company
def get_company_by_name(company_id: str):
    company = app.state.company_repository.fetch_company_view(company_id)
    # print(company)
    return {"data": company}

@app.get("/data/subdomains") # specifieke company
def get_subdomain_information():
    subdomain_information = app.state.sector_repository.fetch_subdomain_information()
    # print(company)
    return {"data": subdomain_information}


@app.get("/sector/{company_id}")
def read_items(company_id: str):
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
