import os
import re
import json
import pandas as pd
import mysql.connector
from pathlib import Path
from mysql.connector import Error

class Database():
    host = 'localhost'
    # host = '192.168.1.128'
    database = ''
    database = 'test_automap1'
    user = 'root'
    # password = 'password'
    password = '1234'

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
        objectMetaData = MetaData()
        dataInMetaData = objectMetaData.ReadMetadata("config")
        self.host = dataInMetaData['database']['hostIP']
        self.database = dataInMetaData['database']['database']
        self.user = dataInMetaData['database']['authentication']['user']
        self.password = dataInMetaData['database']['authentication']['password']
        return

    def ConnectDatabase(self):
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )
            return connection

        except Error as e:
            print("Error while connecting to MySQL", e)
            return
    
    def CloseDatabase(self, conn):
        try:
            if conn.is_connected():
                cur = conn.cursor()
                cur.close()
                conn.close()
        except Error as e:
            print("Error while connecting to MySQL", e)         
            
        return

    def CreateNewDatabase(self, databaseName):
        self.database = ''
        conn = self.ConnectDatabase()

        sqlCommand = """
            DROP SCHEMA IF EXISTS %s
        """ % ( databaseName )

        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE SCHEMA %s
        """ % ( databaseName )

        self.CreateTask(conn, sqlCommand, ())
        self.CloseDatabase(conn)
        return

    def InitialDatabase(self, newDatabaseName):

        try:
            self.CreateNewDatabase(newDatabaseName)
            self.database = newDatabaseName

            # Save new database to a database metadata
            objectMetaData = MetaData()
            dataInMetaData = objectMetaData.ReadMetadata("config")
            dataInMetaData['database']['database'] = newDatabaseName
            objectMetaData.SaveManualUpdateMetadata(dataInMetaData)
        except Error as e:
            print(e)

        conn = self.ConnectDatabase()

        # Create tables
        sqlCommand = """
            CREATE TABLE disease
            (
                DISEASE_ID           INT          NOT NULL AUTO_INCREMENT,
                DISEASE_NAME         VARCHAR(100) NOT NULL,
                DISEASE_ABBREVIATION VARCHAR(10)  NOT NULL,
                PRIMARY KEY (DISEASE_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE gene_detail
            (
                DETAIL_ID    INT         NOT NULL AUTO_INCREMENT,
                GENE_ID      INT         NOT NULL,
                RS_ID        VARCHAR(25) NOT NULL,
                DISTANCE     INT         NOT NULL,
                RELATIONSHIP VARCHAR(25) NOT NULL,
                PRIMARY KEY (DETAIL_ID, GENE_ID, RS_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE gene_disease
            (
                GENE_SYMBOL VARCHAR(20) NOT NULL,
                DISEASE_ID  INT         NOT NULL,
                GENE_ID     INT         NULL    ,
                PRIMARY KEY (GENE_SYMBOL, DISEASE_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE gene_disease_source
            (
                GENE_SYMBOL    VARCHAR(20) NOT NULL,
                SOURCE_WEBSITE VARCHAR(20) NOT NULL,
                PRIMARY KEY (GENE_SYMBOL, SOURCE_WEBSITE)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE gene_snp
            (
                GENE_ID     INT         NOT NULL,
                RS_ID       VARCHAR(25) NOT NULL,
                GENE_SYMBOL VARCHAR(20) NOT NULL,
                PRIMARY KEY (GENE_ID, RS_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE matching_snp_disease
            (
                RS_ID      VARCHAR(25)  NOT NULL,
                DISEASE_ID INT          NOT NULL,
                MatchBy    VARCHAR(100) NOT NULL,
                GENE_ID    INT          NOT NULL,
                PRIMARY KEY (RS_ID, DISEASE_ID, MatchBy, GENE_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE ncbi
            (
                GENE_ID   INT      NOT NULL,
                UPDATE_AT DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (GENE_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE other_symbol
            (
                GENE_ID      INT          NOT NULL,
                OTHER_SYMBOL VARCHAR(100) NOT NULL,
                PRIMARY KEY (GENE_ID, OTHER_SYMBOL)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE pathway
            (
                DISEASE_ID INT         NOT NULL,
                PATHWAY_ID VARCHAR(20) NOT NULL,
                GENE_ID    INT         NOT NULL,
                PRIMARY KEY (DISEASE_ID, PATHWAY_ID, GENE_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            CREATE TABLE snp
            (
                RS_ID           VARCHAR(25) NOT NULL,
                PROBESET_ID     VARCHAR(25) NOT NULL,
                CHROMOSOME      VARCHAR(5)  NOT NULL,
                POSITION        INT         NOT NULL,
                SOURCE_GENECHIP VARCHAR(25) NOT NULL,
                PRIMARY KEY (RS_ID)
            );
        """
        self.CreateTask(conn, sqlCommand, ())

        # Create CONSTRAINT
        sqlCommand = """
            ALTER TABLE gene_snp
            ADD CONSTRAINT FK_SNP_TO_GENE_SNP
                FOREIGN KEY (RS_ID)
                REFERENCES snp (RS_ID)
                ON UPDATE CASCADE;
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE gene_disease
            ADD CONSTRAINT FK_DISEASE_TO_GENE_DISEASE
                FOREIGN KEY (DISEASE_ID)
                REFERENCES disease (DISEASE_ID);
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE matching_snp_disease
            ADD CONSTRAINT FK_DISEASE_TO_MATCHING_SNP_DISEASE
                FOREIGN KEY (DISEASE_ID)
                REFERENCES disease (DISEASE_ID);
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE matching_snp_disease
            ADD CONSTRAINT FK_SNP_TO_MATCHING_SNP_DISEASE
                FOREIGN KEY (RS_ID)
                REFERENCES snp (RS_ID);
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE ncbi
            ADD CONSTRAINT FK_GENE_SNP_TO_NCBI
                FOREIGN KEY (GENE_ID)
                REFERENCES gene_snp (GENE_ID)
                ON UPDATE CASCADE;
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE other_symbol
            ADD CONSTRAINT FK_NCBI_TO_OTHER_SYMBOL
                FOREIGN KEY (GENE_ID)
                REFERENCES ncbi (GENE_ID)
                ON UPDATE CASCADE;
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE gene_detail
            ADD CONSTRAINT FK_GENE_SNP_TO_GENE_DETAIL
                FOREIGN KEY (GENE_ID, RS_ID)
                REFERENCES gene_snp (GENE_ID, RS_ID)
                ON UPDATE CASCADE;
        """
        self.CreateTask(conn, sqlCommand, ())

        sqlCommand = """
            ALTER TABLE pathway
            ADD CONSTRAINT FK_DISEASE_TO_PATHWAY
                FOREIGN KEY (DISEASE_ID)
                REFERENCES disease (DISEASE_ID);
        """
        self.CreateTask(conn, sqlCommand, ())

        # Import an initial data
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
    pathToDiseaseLogs = os.getcwd() + "/Project/DiseaseLogs"
    pathToAnnotationFile = os.getcwd() + "/Project/AnnotationFile"
    pathToUI = os.getcwd() + "/Project/ui"

    def __init__(self):
        Path( os.getcwd() + "/Project/Dataset" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/Dataset/NCBI" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/TestCase" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/NCBILogs" ).mkdir(parents=True, exist_ok=True)
        Path( os.getcwd() + "/Project/DiseaseLogs" ).mkdir(parents=True, exist_ok=True)
        return

    def GetPathToNCBI(self): return self.pathToDataSet + "/NCBI"
    def GetPathToTestCase(self): return self.pathToTestCase
    def GetPathToChromeDriver(self): return self.pathToChrome
    def GetPathToMetadata(self): return self.pathToMetaData
    def GetPathToNCBILogs(self): return self.pathToNCBILogs
    def GetPathToDiseaseLogs(self): return self.pathToDiseaseLogs
    def GetPathToAnnotationFile(self): return self.pathToAnnotationFile
    def GetPathToUI(self): return self.pathToUI

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
    database.InitialDatabase("test_create_1")
            
