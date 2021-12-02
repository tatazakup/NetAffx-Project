import pandas as pd
import mysql.connector
from mysql.connector import Error

class Database():
    host = 'localhost'
    database = 'DemoDatabase'
    user = 'root'
    password = 'password'

    listDisease = [
        ("Type 1 Diabete", "T1D"),
        ("Type 2 Diabetes", "T2D"),
        ("Bipolar Disorde", "BD"),
        ("Coronary Artery Disease", "CAD"),
        ("Crohn’s Disease", "CD"),
        ("Hypertension", "HT"),
        ("Rheumatoid Arthritis", "RA"),
    ]

    def __init__(self):
        return

    def ConnectDatabase(self):
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )

        except Error as e:
            print("Error while connecting to MySQL", e)
            
        return connection
    
    def CloseDatabase(self, conn):
        try:
            if conn.is_connected():
                cur = conn.cursor()
                cur.close()
                conn.close()
        except Error as e:
            print("Error while connecting to MySQL", e)       
            
        return 

    def InitialDatabase(self):
        conn = self.ConnectDatabase()
        for disease in self.listDisease:
            
            sqlCommand = """
                INSERT INTO DISEASE ( DISEASE_NAME, DISEASE_ABBREVIATION ) 
                VALUES ( %s, %s ) 
            """
            
            self.CreateTask(conn, sqlCommand, disease)
            
        self.CloseDatabase(conn)
        return

    def CreateTask(self, conn, sqlCommand, records):
        cur = conn.cursor()
        cur.execute(sqlCommand, records)
        myresult = cur.fetchall()
        conn.commit()
        
        return myresult

if __name__ == "__main__":
    database = Database()
    conn = database.ConnectDatabase()
    mysqlCommand = """
        SELECT * FROM snp_an WHERE RS_ID = %s
    """
    result = database.CreateTask(conn, mysqlCommand, ('rs10000012', ))
    print('result :', result)
    database.CloseDatabase(conn)
