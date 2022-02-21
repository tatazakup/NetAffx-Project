import os
import json
import pandas as pd
import mysql.connector
from pathlib import Path
from mysql.connector import Error

class Database():
    # host = 'localhost'
    host = '192.168.1.128'
    # database = 'test_automap1'
    database = 'demo_automap3'
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
                INSERT INTO disease ( DISEASE_NAME, DISEASE_ABBREVIATION ) 
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

class FilePath():

    pathToChrome = os.getcwd() + "/Project/ChromeDriver"
    pathToDataSet = os.getcwd() + "/Project/Dataset"
    pathToMetaData = os.getcwd() + "/Project/MetaData"
    pathToTestCase = os.getcwd() + "/Project/TestCase"
    pathToNCBILogs = os.getcwd() + "/Project/NCBILogs"

    def __init__(self):
        Path( os.getcwd() + "/Project/Dataset" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/Dataset/NCBI" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/TestCase" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/NCBILogs" ).mkdir(parents=True, exist_ok=True)
        return

    def GetPathToNCBI(self):        
        return self.pathToDataSet + "/NCBI"

    def GetPathToTestCase(self):
        return self.pathToTestCase

    def GetPathToChromeDriver(self):
        return self.pathToChrome

    def GetPathToMetadata(self):
        return self.pathToMetaData
    
    def GetPathToNCBILogs(self):
        return self.pathToNCBILogs

class LinkDataAndHeader():
    sourceWebsite = {
        'ncbi' : r'https://www.ncbi.nlm.nih.gov/gene',
        'kegg' : r'https://www.kegg.jp/entry',
        'huge' : {
            'first' : r'https://phgkb.cdc.gov/PHGKB/phenoPedia.action?firstQuery=Diabetes%20Mellitus,%20Type%202&cuiID=',
            'second': r'&typeSubmit=GO&check=y&which=2&pubOrderType=pubD'
        }
    }

    def __init__(self):
        return

class MetaData(FilePath):
    jsonData = None
    metadataName = ''
    dataOnMetadata = None

    def __init__(self):
        FilePath.__init__(self)
        return
    
    def ReadMetadata(self, metadataName):
        self.metadataName = metadataName
        self.jsonData = open(self.pathToMetaData + '/' + self.metadataName + '.json', 'r')
        self.dataOnMetadata = json.load( self.jsonData )
        return self.dataOnMetadata
    
    def UpdateMetadata(self, columnName, data):
        self.dataOnMetadata['technical'][columnName] = data
        return
    
    def SaveUpdateMetadata(self):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( self.dataOnMetadata, outfile)
        return
    
    def SaveManualUpdateMetadata(self, data):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( data, outfile)
        return

"""
Model of GeneWithMap
"""
class GeneWithMap():
    ncbiHeader = ['CurrentGeneID', 'OldGeneID', 'GeneSymbol', 'AlsoKnowAs', 'UpdatedAt']
    def __init__(self, CurrentGeneID, OldGeneID, GeneSymbol, AlsoKnowAs, UpdatedAt):
        self.CurrentGeneID = CurrentGeneID
        self.OldGeneID = OldGeneID
        self.GeneSymbol = GeneSymbol
        self.AlsoKnowAs = AlsoKnowAs
        self.UpdatedAt = UpdatedAt

if __name__ == "__main__":
    database = Database()
    conn = database.ConnectDatabase()
    mysqlCommand = """
        SELECT * FROM snp WHERE RS_ID = %s
    """
    result = database.CreateTask(conn, mysqlCommand, ('rs10000012', ))
    print('result :', result)
    database.CloseDatabase(conn)
