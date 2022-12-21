from app.repositories import BaseRepository

from deep_translator import GoogleTranslator

from app.models.loader import load_model_ann_ult_score, load_model_linear_regression, load_model_rfr_general_score

import pandas as pd




class AdminRespository(BaseRepository):

    def __init__(self, db):
        self.db = db


    def fetch_keywords(self):
        domains = ["Environment", "Social", "Governance"]
        out = {}

        def _parse_categories(result, ids):
            return {k: {"value": sorted(v), "id":ids.get(k)} for k,v in sorted(result)}

        def _create_domain_words(domain, output, category_ids):
            q = "SELECT categorie_naam, zoektermen from view_zoekterm_per_domein where domein = (%s)"
            v = [domain]
            result, _ = self.fetch_all(q, v)
            output[domain] = _parse_categories(result, category_ids)
            return output

        q = f"SELECT categorie_naam, categorie_id  FROM view_zoekterm_per_domein order by categorie_naam asc"
        result, _ = self.fetch_all(q, [])
        category_ids = {k:v for k,v in result}

        for domain in domains: out = _create_domain_words(domain, out, category_ids)
        return {"domains": out, "categories": category_ids}


    def add_keyword(self, category_id, keyword, language):
        source = str(language).lower()
        keyword = str(keyword).lower()

        if source == "nl":
            target = "en"
        elif source == "en":
            target = "nl"
        else:
            print(f"Unknown language: {source}")
            return ""

        keyword_translated = GoogleTranslator(source=source, target=target).translate(keyword)

        q = 'SELECT zoekterm_description FROM zoektermen WHERE "categorie_id" = (%s) AND "zoekterm_description" = (%s)'
        v = [category_id, keyword]
        res, _ = self.fetch_all(q, v)
        keyword_already_exists = bool(res)

        if not keyword_already_exists:
            q = "INSERT INTO zoektermen (categorie_id, zoekterm_description, language) VALUES ((%s), (%s), (%s)) RETURNING zoekterm_description"
            v = [category_id, keyword, source]
            res, des = self.insert(q, v)
            print(f"inserted {res}")

            if keyword_translated != keyword:

                q = "INSERT INTO zoektermen (categorie_id, zoekterm_description, language) VALUES ((%s), (%s), (%s)) RETURNING zoekterm_description"
                v = [category_id, keyword_translated, target]
                res, des = self.insert(q, v)
                print(f"inserted {res}")

        return {"status": "ok"}


    def remove_keyword(self, category_id, keyword):
        keyword = str(keyword).lower()

        q = 'DELETE FROM zoektermen WHERE "categorie_id" = (%s) AND "zoekterm_description" = (%s) RETURNING zoekterm_description'
        v = [category_id, keyword]
        res, _ = self.insert(q, v)
        removed = [x[0] for x in res]

        return {"removed": removed, "status": "ok"}

    
    def predict_score(self, urbanisation, balance_total, revenue, employees, years):
        ann = load_model_ann_ult_score()

        q = 'SELECT * FROM view_machine_learning_max'
        result, description = self.insert(q, [])

        maximum = pd.DataFrame(result, columns=['urb', 'bt','omzet','pb', 'jaren']).to_numpy()

        urb = urbanisation / float(maximum[0][0])
        bt = balance_total / float(maximum[0][1])
        omzet = revenue / float(maximum[0][2])
        pb = employees / float(maximum[0][3])
        jaren = years / float(maximum[0][4])

        score = ann.predict([[float(urb), float(bt), float(omzet), float(pb), float(jaren)]])

        env = score[0][0] * 100
        soc = score[0][1] * 100
        gov = score[0][2] * 100

        lr = load_model_linear_regression()
        lr_score = lr.predict([[float(urbanisation), float(balance_total), float(revenue), float(employees), float(years)]])[0]

        rfr = load_model_rfr_general_score()
        rfr_score = rfr.predict([[float(urbanisation), float(balance_total), float(revenue), float(employees), float(years)]])[0]

        env=int(env)
        soc=int(soc)
        gov=int(gov)
        lr_score=int(lr_score)
        linregcalc=str(lr.coef_)
        rfr=int(rfr_score)

        return {"data": { "env": env, "soc": soc, "gov": gov, "lr_score": lr_score, "max": str(maximum), "linregcalc": linregcalc, "rfr": rfr } }




