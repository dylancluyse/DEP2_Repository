from Controllers.Repositories.ConnectionController import Connection as conn

class ScoreRepository():
    def update_all_scores():
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        cursor.execute(f"""
        select domein, count(*)
        from categorie_zoektermen
        group by domein
        """)

        domeinen = cursor.fetchall()

        cursor.execute(f"""
        select categorie_id, domein
        from categorie_zoektermen
        """)

        categories = cursor.fetchall()        

        for row in domeinen:
            domein = str(row[0]).lower()
            totaal = row[1]
            teller = 1
            string = f""" UPDATE "KMO" k SET """

            for row in categories:
                categorie=row[0]
                domein_c=str(row[1]).lower()
                
                if (domein_c == domein):
                    search_string = ScoreRepository.get_search_string(row[0])
                    string += f"""{domein}[{teller}] = (select ts_rank_cd(ts_document, query) as rank from "KMO" k2, to_tsquery('dutch','({search_string})') query where query @@ ts_document and k2.ondernemingsnummer = k.ondernemingsnummer), """
                    teller += 1


            query = string[:-2]
            
            cursor.execute(query)




    def get_search_string(cat):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        cursor.execute(f"""
                select zoekterm_description
                from "zoektermen"
                where categorie_id = {cat}
        """)

        zoektermen = [list[0] for list in cursor.fetchall()]

        string = ""
        for i, zt in enumerate(zoektermen):
            if i == 0:
                string += str(zt).replace(' ', ' <-> ')
            else:
                string += " | " + str(zt).replace(' ', ' <-> ')
        return string

    def get_score(cat, compnr):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        search_string = ScoreRepository.get_search_string(cat)

        cursor.execute(f"""
                select ts_rank_cd(ts_document, query) as rank 
	            from "KMO", to_tsquery('dutch','({search_string})') query 
	            where query @@ ts_document and ondernemingsnummer = {compnr}
        """)

        resultweb = cursor.fetchone()

        print(f"""
        select ts_rank_cd(ts_document, query) as rank 
	            from "Balans", to_tsquery('dutch','({search_string})') query 
                where query @@ ts_document and ondernemingsnummer = {compnr}
        """)

        cursor.execute(f"""
                select ts_rank_cd(ts_document, query) as rank 
	            from "Balans", to_tsquery('dutch','({search_string})') query 
                where query @@ ts_document and ondernemingsnummer = {compnr}
        """)

        resultnbb = cursor.fetchone()

        if (resultnbb == None):
            resultnbb = 0
        
        if(resultweb == None):
            resultweb = 0

        return sum(resultnbb + resultweb)

    def calc_score(arr):
        n = len(arr)
        for i in range(n):
            if(arr[i] > 0):
                arr[i] = 1
            else:
                arr[i] = 0
        return arr


    def get_all_scores(compnr):
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()
        
        cursor.execute(f"""
            SELECT max(categorie_id) FROM categorie_zoektermen
        """)

        max = sum(cursor.fetchone())
        print(max)
        arr = []

        for i in range(1, max + 1):
            try:
                arr.append(ScoreRepository.get_score(i, compnr=compnr))
            except:
                arr.append(0)

        print(arr)