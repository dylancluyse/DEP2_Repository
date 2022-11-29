import psycopg2

#establishing the connection
conn = psycopg2.connect(
    host="vichogent.be",
    database="depdatabase",
    port = 40033,
    user="postgres",
    password="DaddyDylan123")

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
