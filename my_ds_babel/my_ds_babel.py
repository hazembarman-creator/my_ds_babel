import sqlite3 as sql
from io import StringIO
import csv

def sql_to_csv(database, table_name):
    connection = sql.connect(database)
    cursor = connection.cursor()

    # executer la requette
    cursor.execute(f"SELECT * FROM {table_name}")

    # avoir les noms des colonnes
    column_names = [col[0] for col in cursor.description]

    # creation du csv par ligne
    csv_data = ""
    # ajout des noms de colonnes en premiere ligne
    csv_data += ",".join(column_names) + "\n"

    # ecrire le restant des lignes
    for row in cursor:
        row_data = ",".join([str(value) for value in row])
        csv_data += row_data + "\n"

    # fermer le curseur et la connexion
    cursor.close()
    connection.close()

    # Enlever le dernier \n
    csv_data = csv_data.rstrip('\n')

    return csv_data

def csv_to_sql(csv_content, database, table_name):
    #connexion a la base de donnee
    connection = sql.connect(database)
    cursor = connection.cursor()

    #Lecture du fichier et converstion en string
    read = csv.reader(StringIO(csv_content.read()))

    # get la premiere ligne qui respresentes les differents colonnes
    columns = next(read) #fichier

    # get toutes les colonnes de notre 
    columns_names = ','.join([f"'{column}' TEXT" for column in columns]) 
        
    #creating a table with the first column of the file
        
    create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " (" +  columns_names +");"
    cursor.execute(create_table)
   

    #inserting values in the created table
    for row in read:
        val_label = ','.join('?'* len(row))
        insertion_query = "INSERT INTO " + table_name + " VALUES " + "(" + val_label + ")"
        cursor.execute(insertion_query, row)
          

    connection.commit()
    connection.close()