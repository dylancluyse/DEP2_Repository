#from Repositories.FileController import FileController as fc
#from ConnectionController import Connection as conn

import re

from Controllers.Repositories.ConnectionController import Connection as conn
from Controllers.Repositories.FileController import FileController as fc


class AnnualReportsRepo():

    def __init__(self):
        pass

    """
    TODO 
    Python-code: De nodige info uit het csv-bestand ophalen. Je krijgt een Pandas-dataframe terug van de filecontroller.
    SQL-query: De rij (afhankelijk van het ondernemingsnummer) wordt dan geüpdatet.
    """
    def add_NBB_CSV():
        csv_contents = fc.read_NNB_CSV()
        d = dict(zip(csv_contents.iloc[:, 0], csv_contents.iloc[:, 1]))
        
        """
        10/49 --> Balanstotaal
        9145 --> Netto toegevoegde waarde
        6.10 --> omzet
        """
        arr_types = ['Language', 'Entity name', 'Entity number', 'Accounting period end date', 'Legal form', '10/49', '9145', '70', '12011', '12012', '12021', '12022', '12111', '12112', '12121', '12122']
        output = []
        for elem in arr_types:
            try:
                var=d[elem]
                output.append(var)
            except:
                var=0
                output.append(var)

        """
        TODO
        PostgreSQL-queries schrijven:
        * Toevoegen aan balanstotaal
        * Toevoegen aan KMO
        """
        db_conn = conn.get_conn()


        companynr=output[2]


        """
        KMO-TABLE
        Hebben we al gegevens van dit ondernemingsnummer?
            -- Zo ja --> rij updaten.
            -- Zo nee --> rij aanmaken en dan de cellen updaten.
        """
        cursor = db_conn.cursor()
        cursor.execute(f'SELECT * FROM "KMO" WHERE ondernemingsnummer = {companynr};')

        rows_id_exist = cursor.fetchall()
        cursor.close()

        if len(rows_id_exist) != 0:
            cursor = db_conn.cursor()
            cursor.execute(f"""
            UPDATE "KMO"
            SET naam='{output[1]}', beursnotatie='{output[4]}'
            WHERE ondernemingsnummer = {output[2]}
            """)

            print(f"""
            65 UPDATE "KMO"
            SET naam='{output[1]}', beursnotatie='{output[4]}'
            WHERE ondernemingsnummer = {output[2]}
            """)

            db_conn.commit()
            cursor.close()
        else:
            cursor = db_conn.cursor()
            cursor.execute(f"""
            INSERT INTO "KMO" (ondernemingsnummer) 
            VALUES (0{output[2]});
            """)

            print(f"""
            81 INSERT INTO "KMO" (ondernemingsnummer) 
            VALUES (0{output[2]});
            """)

            db_conn.commit()
            cursor.close()

            cursor = db_conn.cursor()
            cursor.execute(f"""
            UPDATE "KMO"
            SET naam='{output[1]}', beursnotatie='{output[4]}'
            WHERE ondernemingsnummer = {output[2]}
            """)

            print(f"""
            95 UPDATE "KMO"
            SET naam='{output[1]}', beursnotatie='{output[4]}'
            WHERE ondernemingsnummer = {output[2]}
            """)

            db_conn.commit()
            cursor.close()
    
        """
        BALANS-TABLE
        """
        cursor = db_conn.cursor()
        cursor.execute(f"""SELECT * FROM "Balans" WHERE ondernemingsnummer = '{output[2]}';""")

        print(f"""113 SELECT * FROM "Balans" WHERE ondernemingsnummer = '{output[2]}';""")

        rows_id_exist = cursor.fetchall()


        cursor.close()

        if len(rows_id_exist) != 0:
                cursor = db_conn.cursor()
                cursor.execute(f"""
                    UPDATE "Balans"
                    SET language_report = '{output[0]}', omzet = {output[7]}, balanstotaal = {output[5]}, net_add_val = {output[6]}, date_nbb_report = '{output[3]}', ondernemingsnummer = {output[2]}
                    WHERE ondernemingsnummer = '{output[2]}';
                """)

                print(f"""
                134 UPDATE "Balans"
                    SET language_report = '{output[0]}', omzet = {output[7]}, balanstotaal = {output[5]}, net_add_val = {output[6]}, date_nbb_report = {output[3]}, ondernemingsnummer = {output[2]}
                    WHERE ondernemingsnummer = '{output[2]}';
                """)

                db_conn.commit()
                cursor.close()
        else:
                cursor = db_conn.cursor()
                cursor.execute(f"""
                    INSERT INTO "Balans"
                    (ondernemingsnummer) VALUES ('0{output[2]}');
                """)

                print(f"""
                151 INSERT INTO "Balans"
                    (ondernemingsnummer) VALUES ('{output[2]}');
                """)
                db_conn.commit()
                cursor.close()

                cursor = db_conn.cursor()
                cursor.execute(f"""
                    UPDATE "Balans"
                    SET language_report = '{output[0]}', omzet = {output[7]}, balanstotaal = {output[5]}, net_add_val = {output[6]}, date_nbb_report = {output[3]}, ondernemingsnummer = {output[2]}
                    WHERE ondernemingsnummer = '{output[2]}';
                """)

                print(f"""
                164 UPDATE "Balans"
                    SET language_report = '{output[0]}', omzet = {output[7]}, balanstotaal = {output[5]}, net_add_val = {output[6]}, date_nbb_report = {output[3]}, ondernemingsnummer = {output[2]}
                    WHERE ondernemingsnummer = '{output[2]}';
                """)
                db_conn.commit()
                cursor.close()
                
        

    """
    TODO
    De plaintekst met een SQL-query gaan invoeren in de databank (afhankelijk van het ondernemingsnummer).
    """
    def add_NBB_PDF(companyNr):
        pdf_contents = fc.read_NBB_PDF()

        print(companyNr)
       
        db_conn = conn.get_conn()
        cursor = db_conn.cursor()

        cursor.execute(f"""SELECT * FROM "Balans" WHERE ondernemingsnummer = '0{companyNr}';""")

        rows_id_exist = cursor.fetchall()

        print(rows_id_exist)

        cursor.close()

        if len(rows_id_exist) != 0:
            cursor = db_conn.cursor()
            cursor.execute(f"""
                UPDATE "Balans"
                SET content_nbb_report = '{pdf_contents}'
                WHERE ondernemingsnummer = '{companyNr}';
            """)

            db_conn.commit()
            cursor.close()

        else:
            cursor = db_conn.cursor()
            cursor.execute(f"""
                INSERT INTO "Balans"
                (ondernemingsnummer) VALUES ('{companyNr}');
            """)


            db_conn.commit()
            cursor.close()

            cursor = db_conn.cursor()
            cursor.execute(f"""
                UPDATE "Balans"
                SET content_nbb_report = '{pdf_contents}'
                WHERE ondernemingsnummer = '{companyNr}';
            """)

            db_conn.commit()
            cursor.close()

