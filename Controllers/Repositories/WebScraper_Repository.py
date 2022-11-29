
from Controllers.Repositories.ConnectionController import Connection as conn
from Controllers.Repositories.FileController import FileController as fc


class WebScraperRepo():

    def __init__(self) -> None:
        pass

    """
    Main-function for this repository. It will follow these steps:
    1. Check if there's a webcontents file and save the contents as a variable 'webcontents'.
    TODO
    2. Store the webcontents to the database using a Postgres-query.
        2.1. Verbinding opstarten
        2.2. UPDATE-query uitvoeren op databank. Content-veld invullen als het niet bestaat. --> EERD
        2.3. Commit + close.
    """

    def adding_Content(companynr, website):
        webcontents = fc.read_Web_Contents()
        db_conn = conn.get_conn()

        cursor = db_conn.cursor()

        cursor.execute(f"""
        SELECT ondernemingsnummer
        FROM "KMO"
        WHERE ondernemingsnummer = {companynr};
        """)

        rows = cursor.fetchall()

        if len(rows) != 0:
            cursor = db_conn.cursor()
            cursor.execute(f"""
            UPDATE "KMO"
            SET webcontents = '{webcontents}', website = '{website}'
            WHERE ondernemingsnummer = {companynr}
            """)
            db_conn.commit()
            cursor.close()

        else:
            cursor = db_conn.cursor()
            cursor.execute(f"""
            INSERT INTO "KMO" (ondernemingsnummer)
            VALUES ({companynr});
            """)
            db_conn.commit()
            cursor.close()

            cursor = db_conn.cursor()
            cursor.execute(f"""
            UPDATE "KMO"
            SET webcontents = '{webcontents}', website = '{website}'
            WHERE ondernemingsnummer = {companynr}
            """)
            db_conn.commit()
            cursor.close()
