import os
import pandas as pd
import json
import sqlite3
from sqlite3 import Error
from contextlib import closing

"""
Class detail
"""
class GetDataFromFile():
    
    sourceNcbiWebsite = r'https://www.ncbi.nlm.nih.gov/gene'
    sourceWebsite = {
        'ncbi' : r'https://www.ncbi.nlm.nih.gov/gene',
        'kegg' : r'https://www.kegg.jp/entry',
        'huge' : {
            'first' : r'https://phgkb.cdc.gov/PHGKB/phenoPedia.action?firstQuery=Diabetes%20Mellitus,%20Type%202&cuiID=',
            'second': r'&typeSubmit=GO&check=y&which=2&pubOrderType=pubD'
        }
    }
    
    pathToDataSet = os.getcwd() + "/Project/Dataset"
    
    ncbiHeader = ['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'UpdatedAt']
    
    def __init__(self):
        return
    
    def ReadAllUniqueGeneID(self):
        return pd.read_csv( self.pathToDataSet + "/GeneNotSame.csv" )
    
    def ReadNcbiData(self):
        return pd.read_csv( self.pathToDataSet + "/GeneWithMap.csv" )
    
    def ReadListDisease(self):
        return pd.read_csv( self.pathToDataSet + "/ListDisease.csv" )
    
    def ReadDiseaseType2(self):
        return pd.read_csv( self.pathToDataSet + "/Disease/Type 2 diabetes mellitus.csv" )
        
    def ReadListSNP_Nsp(self):
        return pd.read_csv( self.pathToDataSet + "/Mapping250K_Nsp.na32.annot.csv" )
    
    def ReadListSNP_Sty(self):
        return pd.read_csv( self.pathToDataSet + "/Mapping250K_Sty.na32.annot.csv" )
    
    def ReadMain_Nsp(self):
        return pd.read_csv( self.pathToDataSet + "/MainCSV/MainData_Nsp.csv" )
    
    def ReadMain_Sty(self):
        return pd.read_csv( self.pathToDataSet + "/MainCSV/MainData_Sty.csv" )
    
    def GetPathToGeneWithMap(self):
        return self.pathToDataSet + "/GeneWithMap.csv"
    
    def GetPathToListDisease(self):
        return self.pathToDataSet + "/Disease"
    
    def GetPathToGeneData(self):
        return self.pathToDataSet + "/GeneData"
    
    def GetPathToMainCSV(self):
        return self.pathToDataSet + "/MainCSV"
    
"""
Class detail
"""
class MetaData():
    pathToMetaData = os.getcwd() + "/Project/MetaData"
    jsonData = None
    metadataName = ''
    dataOnMetadata = None
    
    def __init__(self):
        return
    
    def ReadMetadata(self, inputMetadataName):
        self.metadataName = inputMetadataName
        self.jsonData = open(self.pathToMetaData + '/' + self.metadataName + '.json', 'r')
        self.dataOnMetadata = json.load( self.jsonData )
        return
    
    def UpdateMetadata(self, columnName, inputData):
        self.dataOnMetadata['technical'][columnName] = inputData
        return
    
    def SaveUpdateMetadata(self):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( self.dataOnMetadata, outfile)
        return
    
"""
Class detail
"""
class Database():
    
    def __init__(self):
        return
    
    def CreateDatabase(self):
        conn = sqlite3.connect('NetAffx.db') 
        c = conn.cursor()

        # SNP Annotation (SNP_AN)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS SNP_AN
            (
                RS_ID          CHAR(25)     NOT NULL    PRIMARY KEY,
                PROBE_ID       CHAR(25)     NOT NULL,
                CHROMOSOME     INT          NOT NULL,
                SOURCE         CHAR(20)     NOT NULL
            );
            '''
        )

        # SNP annotation file has AssociatedGene (SNP_AN_AS)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS SNP_AN_AS
            (
                RS_ID          CHAR(25)     NOT NULL,
                GENE_ID        INT          NOT NULL,
                GENE_SYMBOL    CHAR(20)     NOT NULL,
                PRIMARY KEY (RS_ID, GENE_ID),
                FOREIGN KEY(RS_ID) REFERENCES SNP_AN(RS_ID)
            );
            '''
        )

        # Annotation AssociatedGene details (AN_AS_DETAIL)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS AN_AS_DETAIL
            (
                DETAIL_ID      INT          NOT NULL    PRIMARY KEY,
                RS_ID          CHAR(25)     NOT NULL,
                GENE_ID        INT          NOT NULL,
                DISTANCE       INT          NOT NULL,
                RELATIONSHIP   CHAR(10)     NOT NULL,
                FOREIGN KEY(RS_ID, GENE_ID) REFERENCES SNP_AN_AS(RS_ID, GENE_ID)
            );
            '''
        )

        # AlsoKnownAs (ALSO_KNOW_AS)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS ALSO_KNOW_AS
            (
                GENE_ID        INT          NOT NULL    PRIMARY KEY,
                OTHER_SYMBOL   INT          NULL,
                UPDATE_AT      DATETIME     NOT NULL,
                FOREIGN KEY(GENE_ID) REFERENCES SNP_AN_AS(GENE_ID)
            );
            '''
        )

        # Disease (DISEASE)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS DISEASE
            (
                DISEASE_ID     INT          NOT NULL   PRIMARY KEY,
                DISEASE_NAME   CHAR(100)    NOT NULL,
                DISEASE_ABBREVIATION     CHAR(10)     NOT NULL
            );
            '''
        )

        # Disease has AssociatedGene (DISEASE_AS)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS DISEASE_AS
            (
                GENE_SYMBOL    CHAR(20)     NOT NULL,
                GENE_ID        INT          NULL,
                DISEASE_ID     INT          NOT NULL,
                PRIMARY KEY (DISEASE_ID, GENE_SYMBOL),
                FOREIGN KEY(DISEASE_ID) REFERENCES DISEASE(DISEASE_ID)
            );
            '''
        )

        # AssociatedGene From Source (AS_SOURCE)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS AS_SOURCE
            (
                GENE_SYMBOL    CHAR(20)     NOT NULL    PRIMARY KEY,
                SOURCE         INT          NOT NULL,
                FOREIGN KEY(GENE_SYMBOL) REFERENCES DISEASE_AS(GENE_SYMBOL)
            );
            '''
        )

        # SNP anotation rerated to Diseas (SNP_AN_DISEASE)
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS SNP_AN_DISEASE
            (
                RS_ID            CHAR(25)    NOT NULL,
                DISEASE_ID       INT         NOT NULL,
                PRIMARY KEY (RS_ID, DISEASE_ID),
                FOREIGN KEY(RS_ID) REFERENCES SNP_AN(RS_ID),
                FOREIGN KEY(DISEASE_ID) REFERENCES DISEASE(DISEASE_ID)
            );
            '''
        )

        conn.commit()
        
        conn.close()
    
    def InitializeData(self):
        conn = self.ConnectDatabase()
        listDisease = [
            (1, "Type 1 Diabete", "T1D"),
            (2, "Type 2 Diabetes", "T2D"),
            (3, "Bipolar Disorde", "BD"),
            (4, "Coronary Artery Disease", "CAD"),
            (5, "Crohn’s Disease", "CD"),
            (6, "Hypertension", "HT"),
            (7, "Rheumatoid Arthritis", "RA"),
        ]
        
        sqlCommand = ''' 
            INSERT INTO DISEASE( DISEASE_ID, FULL_NAME, SHORT_NAME ) 
            VALUES( ?, ?, ? )
        '''
        
        self.CreateManyTask(conn, sqlCommand, listDisease)
    
    def ConnectDatabase(self):
        try:
            conn = sqlite3.connect("Project/NetAffx.db")
        except Error as e:
            print(e)

        return conn
    
    def CreateTask(self, conn, command, task):
        # cur = conn.cursor()
        # cur.execute(command, task)
        with closing(conn.cursor()) as cur:
            try:
                cur.execute(command, task)
                conn.commit()
                return cur.fetchall()
            finally:
                cur.close() 
        # conn.commit()
        # rows = cur.fetchall()
        # return rows
    
    def CreateManyTask(self, conn, command, task):
        # cur = conn.cursor()
        # cur.executemany(command, task)
        # conn.commit()
        # rows = cur.fetchall()
        
        with closing(conn.cursor()) as cur:
            try:
                cur.executemany(command, task)
                conn.commit()
                return cur.fetchall()
            finally:
                cur.close() 
                
        # return rows
    
    def InsertDataToALSO_KNOW_AS(self, PathFileNcbi):
        conn = self.ConnectDatabase()
        data = pd.read_csv(PathFileNcbi)
        
        for row_index, row in data.iterrows():
            print( str(row['alsoKnowAs']), type(row['alsoKnowAs']) )
            geneID = row['geneID']
            if ( str(row['alsoKnowAs']) == 'nan' ):
                sqlCommand = ''' 
                    INSERT OR REPLACE INTO ALSO_KNOW_AS( GENE_ID, UPDATE_AT ) 
                    VALUES( ?, ? )
                '''
                self.CreateTask(conn, sqlCommand, (row['geneID'], row['updatedAt']))
            else:
                sqlCommand = ''' 
                    INSERT OR REPLACE INTO ALSO_KNOW_AS( GENE_ID, OTHER_SYMBOL, UPDATE_AT ) 
                    VALUES( ?, ?, ? )
                '''
                self.CreateTask(conn, sqlCommand, (row['geneID'], row['alsoKnowAs'], row['updatedAt']))
                
        return
    
    def SwapMainDataToSNP_AN(self, PathFileNcbi):
        conn = self.ConnectDatabase()
        data = pd.read_csv(PathFileNcbi)
        
        for row_index, row in data.iterrows():
            print(
                str(row['ProbeSetID']),
                str(row['dbSNPRSID']),
                str(row['Chromosome']),
                str(row['relationship']),
                str(row['distance']),
                str(row['GeneSymbol']),
                str(row['NCBIGeneID']),
                str(row['AlsoKnowAs']),
            )
            continue
        
    
if __name__ == "__main__":
    
    database = Database()
    
    database.CreateDatabase()
    # database.InitializeData()
    # database.SwapNcbiToALSO_KNOW_AS('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/GeneWithMapBK-2.csv')
    # database.SwapMainDataToSNP_AN('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/MainCSV/MainData_Nsp.csv')
    
    print('Main')