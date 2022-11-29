import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('Web_Application/.env')
load_dotenv(dotenv_path=dotenv_path)


#establishing the connection
conn = psycopg2.connect(
    host=os.environ.get("host"),
    database=os.environ.get("database"),
    port = os.environ.get("port"),
    user=os.environ.get("user"),
    password=os.environ.get("password"))

#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Retrieving data
#cursor.execute('''SELECT * from "Locatie" where "locatieID" = 207''')

sectornaam = "Bouw";

cursor.execute('''SELECT * from "Sector" where "sectornaam" = (%s)''',[sectornaam])


#Fetching 1st row from the table
result = cursor.fetchone();
print(result)

#Fetching 1st row from the table
result = cursor.fetchall();
print(result)

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()
