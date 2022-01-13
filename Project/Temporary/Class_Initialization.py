import os
import pandas as pd
import json
import sqlite3
import datetime
from sqlite3 import Error
from contextlib import closing
import mysql.connector
from mysql.connector import Error

"""
Class detail
"""
class Initialize():
    
    host = 'localhost'
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
                
    def InsertOldDataToDatabase(self):
        
        ##### SNP Annotations
        # data_NSP = pd.read_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/Annotation_Nsp_addposition.csv')
        # data_STY = pd.read_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/Annotation_Sty_addposition.csv')
        
        ### SNP_AN
        # conn = self.ConnectDatabase()
        
        # for row_index, row in data_NSP.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN ( RS_ID, PROBE_ID, CHROMOSOME, POSITION, SOURCE_NAME ) 
        #         VALUES ( %s, %s, %s, %s, %s ) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['RSID'], row['ProbeSetID'], row['Chromosome'], row['Physical Position'], 'Nsp') )
            
        # for row_index, row in data_STY.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN ( RS_ID, PROBE_ID, CHROMOSOME, POSITION, SOURCE_NAME )
        #         VALUES ( %s, %s, %s, %s, %s ) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['RSID'], row['ProbeSetID'], row['Chromosome'], row['Physical Position'], 'Sty') )
            
        # self.CloseDatabase(conn)
        
        
        ### SNP_AN_AS
        # conn = self.ConnectDatabase()
        
        # for row_index, row in data_NSP.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN_AS ( GENE_ID, RS_ID, GENE_SYMBOL ) 
        #         VALUES ( %s, %s, %s, %s, %s ) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['GeneID'], row['RSID'], row['GeneSymbol']) )
            
        # for row_index, row in data_STY.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN_AS ( GENE_ID, RS_ID, GENE_SYMBOL ) 
        #         VALUES ( %s, %s, %s, %s, %s ) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['GeneID'], row['RSID'], row['GeneSymbol']) )
            
        # self.CloseDatabase(conn)
        
        
        ### SNP_AN_AS_DETAIL
        # conn = self.ConnectDatabase()
        
        # for row_index, row in data_NSP.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN_AS_DETAIL ( GENE_ID, RS_ID, DISTANCE, RELATIONSHIP ) 
        #         VALUES ( %s, %s, %s, %s ) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['GeneID'], row['RSID'], row['distance'], row['relationship']) )
            
        # for row_index, row in data_STY.iterrows():
        #     print(row)
            
        #     sqlCommand = """
        #         REPLACE INTO SNP_AN_AS_DETAIL ( GENE_ID, RS_ID, DISTANCE, RELATIONSHIP ) 
        #         VALUES ( %s, %s, %s, %s) 
        #     """
            
        #     self.CreateTask(conn, sqlCommand, (row['GeneID'], row['RSID'], row['distance'], row['relationship']) )
            
        # self.CloseDatabase(conn)
        
        
        ##### Also Know As
        # data = pd.read_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/GeneWithMapBK-2.csv')
        
        # for row_index, row in data.iterrows():
        #     timestamp = datetime.datetime.fromtimestamp(row['updatedAt']).strftime('%Y-%m-%d %H:%M:%S')
        #     print( str(row['alsoKnowAs']), str(row['updatedAt']), timestamp )
            
        #     conn = self.ConnectDatabase()
            
        #     sqlCommand = """
        #             REPLACE INTO NCBI ( GENE_ID, UPDATE_AT ) 
        #             VALUES ( %s, %s ) 
        #         """
        #     self.CreateTask(conn, sqlCommand, ((row['geneID']), timestamp))
            
        #     if ( str(row['alsoKnowAs']) != 'nan' ):
        #         otherSymbol = row['alsoKnowAs'].split('; ')
            
        #         for eachSymbol in otherSymbol:
        #             sqlCommand = """
        #                 REPLACE INTO OTHER_SYMBOL ( GENE_ID, OTHER_SYMBOL ) 
        #                 VALUES ( %s, %s ) 
        #             """
        #             self.CreateTask(conn, sqlCommand, (row['geneID'], eachSymbol) )

        # self.CloseDatabase(conn)
        
        
        
        ##### Disease
        # self.InsertDiseaseName()
        
        ##### Disease_AS and AS_SOURCE
        data = pd.read_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/Disease/Bipolar Disorde.csv')
        
        for row_index, row in data.iterrows():
            
            conn = self.ConnectDatabase()
            sources = row['Source'].split('; ')
            
            if ( str(row['GeneID']) != 'nan' ):
                sqlCommand = """
                    INSERT IGNORE INTO DISEASE_AS ( GENE_SYMBOL, DISEASE_ID, GENE_ID ) 
                    VALUES ( %s, %s, %s )
                """
                
                self.CreateTask(conn, sqlCommand, (row['GeneSymbol'], 3, row['GeneID']))
            else:
                sqlCommand = """
                    INSERT IGNORE INTO DISEASE_AS ( GENE_SYMBOL, DISEASE_ID ) 
                    VALUES ( %s, %s ) 
                """
                
                self.CreateTask(conn, sqlCommand, (row['GeneSymbol'], 3))
            
            for source in sources:
                
                sqlCommand = """
                    INSERT IGNORE INTO AS_SOURCE ( GENE_SYMBOL, SOURCE_WEBSITE ) 
                    VALUES ( %s, %s ) 
                """
                
                self.CreateTask(conn, sqlCommand, (row['GeneSymbol'], source))
                
        self.CloseDatabase(conn)
        
        
        
        ##### SNP_AN_DISEASE
        # data = pd.read_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/rsidT2D.csv')
        
        # for row_index, row in data.iterrows():
        #     print( row )
        #     conn = self.ConnectDatabase()
            
        #     sqlCommand = """
        #             REPLACE INTO SNP_AN_DISEASE ( RS_ID, DISEASE_ID ) 
        #             VALUES ( %s, %s ) 
        #         """
        #     self.CreateTask(conn, sqlCommand, (row['RSID'], 2))

        # self.CloseDatabase(conn)
        
        return
    
    def InsertDiseaseName(self):
        for disease in self.listDisease:
            conn = self.ConnectDatabase()
            
            sqlCommand = """
                INSERT INTO DISEASE ( DISEASE_NAME, DISEASE_ABBREVIATION ) 
                VALUES ( %s, %s ) 
            """
            
            self.CreateTask(conn, sqlCommand, disease)
            
        self.CloseDatabase(conn)
            
    def CreateTask(self, conn, sqlCommand, records):
        cur = conn.cursor()
        cur.execute(sqlCommand, records)
        myresult = cur.fetchall()
        conn.commit()
        
        return myresult
    
    def CreateManyTask(self, conn, sqlCommand, records):
        cur = conn.cursor()
        cur.executemany(sqlCommand, records)
        myresult = cur.fetchall()
        conn.commit()
        
        return myresult
    
    def ToolSearchWithRSID(self):
        conn = self.ConnectDatabase()
        
        # rs9272219
        RSID_INPUT = str(input('Search with RS_ID : '))
        
        sqlCommand = """
            SELECT 
                SNP_AN.RS_ID,
                SNP_AN.PROBE_ID,
                SNP_AN.CHROMOSOME,
                SNP_AN.POSITION,
                SNP_AN.SOURCE_NAME,
                SNP_AN_AS_DETAIL.RELATIONSHIP, 
                SNP_AN_AS_DETAIL.DISTANCE,
                SNP_AN_AS.GENE_SYMBOL,
                OTHER_SYMBOL.OTHER_SYMBOL,
                DISEASE.DISEASE_NAME,
                DISEASE.DISEASE_ABBREVIATION,
                DISEASE_AS.GENE_ID,
                AS_SOURCE.SOURCE_WEBSITE
            FROM ( ( ( ( ( ( ( ( SNP_AN 
            INNER JOIN SNP_AN_DISEASE ON SNP_AN_DISEASE.RS_ID = SNP_AN.RS_ID )
            INNER JOIN SNP_AN_AS ON SNP_AN_AS.RS_ID = SNP_AN.RS_ID)
            INNER JOIN SNP_AN_AS_DETAIL ON SNP_AN_AS_DETAIL.RS_ID = SNP_AN_AS.RS_ID AND SNP_AN_AS_DETAIL.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID)
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            INNER JOIN DISEASE ON DISEASE.DISEASE_ID = SNP_AN_DISEASE.DISEASE_ID)
            INNER JOIN DISEASE_AS ON DISEASE_AS.DISEASE_ID = DISEASE.DISEASE_ID AND ( DISEASE_AS.GENE_SYMBOL = SNP_AN_AS.GENE_SYMBOL OR DISEASE_AS.GENE_SYMBOL = OTHER_SYMBOL.OTHER_SYMBOL ) )
            INNER JOIN AS_SOURCE ON AS_SOURCE.GENE_SYMBOL = DISEASE_AS.GENE_SYMBOL)
            WHERE SNP_AN.RS_ID = %s
            ORDER BY SNP_AN.CHROMOSOME ASC, SNP_AN.POSITION ASC;
        """
        
        myresult = self.CreateTask(conn, sqlCommand, (RSID_INPUT, ))
        
        self.CloseDatabase(conn)
        
        for x in myresult:
            print(x)
            
    def ToolSearchWithProbeID(self):
        conn = self.ConnectDatabase()
        
        # SNP_A-2214036
        PBID_INPUT = str(input('Search with Probe set ID : '))
        
        sqlCommand = """
            SELECT 
                SNP_AN.RS_ID,
                SNP_AN.PROBE_ID,
                SNP_AN.CHROMOSOME,
                SNP_AN.POSITION,
                SNP_AN.SOURCE_NAME,
                SNP_AN_AS_DETAIL.RELATIONSHIP, 
                SNP_AN_AS_DETAIL.DISTANCE, 
                SNP_AN_AS.GENE_SYMBOL,
                OTHER_SYMBOL.OTHER_SYMBOL,
                DISEASE.DISEASE_NAME,
                DISEASE.DISEASE_ABBREVIATION,
                DISEASE_AS.GENE_ID,
                AS_SOURCE.SOURCE_WEBSITE
            FROM ( ( ( ( ( ( ( ( SNP_AN 
            INNER JOIN SNP_AN_DISEASE ON SNP_AN_DISEASE.RS_ID = SNP_AN.RS_ID )
            INNER JOIN SNP_AN_AS ON SNP_AN_AS.RS_ID = SNP_AN.RS_ID)
            INNER JOIN SNP_AN_AS_DETAIL ON SNP_AN_AS_DETAIL.RS_ID = SNP_AN_AS.RS_ID AND SNP_AN_AS_DETAIL.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID)
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            INNER JOIN DISEASE ON DISEASE.DISEASE_ID = SNP_AN_DISEASE.DISEASE_ID)
            INNER JOIN DISEASE_AS ON DISEASE_AS.DISEASE_ID = DISEASE.DISEASE_ID AND ( DISEASE_AS.GENE_SYMBOL = SNP_AN_AS.GENE_SYMBOL OR DISEASE_AS.GENE_SYMBOL = OTHER_SYMBOL.OTHER_SYMBOL ) )
            INNER JOIN AS_SOURCE ON AS_SOURCE.GENE_SYMBOL = DISEASE_AS.GENE_SYMBOL)
            WHERE SNP_AN.PROBE_ID = %s
            ORDER BY SNP_AN.CHROMOSOME ASC, SNP_AN.POSITION ASC;
        """
        
        myresult = self.CreateTask(conn, sqlCommand, (PBID_INPUT, ))
        
        self.CloseDatabase(conn)
        
        for x in myresult:
            print(x)
            
    def NotFoundDiseaseWithRSID(self):
        conn = self.ConnectDatabase()
        
        # rs17794090
        RSID_INPUT = str(input('Search with RS_ID : '))
        
        sqlCommand = """
            SELECT 
                SNP_AN.RS_ID,
                SNP_AN.PROBE_ID,
                SNP_AN.CHROMOSOME,
                SNP_AN.POSITION,
                SNP_AN.SOURCE_NAME,
                SNP_AN_AS_DETAIL.RELATIONSHIP, 
                SNP_AN_AS_DETAIL.DISTANCE, 
                SNP_AN_AS.GENE_SYMBOL,
                OTHER_SYMBOL.OTHER_SYMBOL
            FROM ( ( ( ( SNP_AN 
            INNER JOIN SNP_AN_AS ON SNP_AN_AS.RS_ID = SNP_AN.RS_ID)
            INNER JOIN SNP_AN_AS_DETAIL ON SNP_AN_AS_DETAIL.RS_ID = SNP_AN_AS.RS_ID AND SNP_AN_AS_DETAIL.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID)
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            WHERE SNP_AN.RS_ID = %s
            ORDER BY SNP_AN.CHROMOSOME ASC, SNP_AN.POSITION ASC;
        """
        
        myresult = self.CreateTask(conn, sqlCommand, (RSID_INPUT, ))
        
        self.CloseDatabase(conn)
        
        for x in myresult:
            print(x)
            
    def ToolSearchWithListRSID(self):
        
        conn = self.ConnectDatabase()
        
        RSID_INPUT = str(input('Search with list RS_ID : '))
        listRSID = ['rs12709430', 'rs12709426', 'rs4351']
        
        sqlCommand = """
            SELECT 
                SNP_AN.RS_ID,
                SNP_AN.PROBE_ID,
                SNP_AN.CHROMOSOME,
                SNP_AN.POSITION,
                SNP_AN.SOURCE_NAME,
                SNP_AN_AS_DETAIL.RELATIONSHIP, 
                SNP_AN_AS_DETAIL.DISTANCE, 
                SNP_AN_AS.GENE_SYMBOL,
                OTHER_SYMBOL.OTHER_SYMBOL,
                DISEASE.DISEASE_NAME,
                DISEASE.DISEASE_ABBREVIATION,
                DISEASE_AS.GENE_ID,
                AS_SOURCE.SOURCE_WEBSITE
            FROM ( ( ( ( ( ( ( ( SNP_AN 
            INNER JOIN SNP_AN_DISEASE ON SNP_AN_DISEASE.RS_ID = SNP_AN.RS_ID )
            INNER JOIN SNP_AN_AS ON SNP_AN_AS.RS_ID = SNP_AN.RS_ID)
            INNER JOIN SNP_AN_AS_DETAIL ON SNP_AN_AS_DETAIL.RS_ID = SNP_AN_AS.RS_ID AND SNP_AN_AS_DETAIL.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID)
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            INNER JOIN DISEASE ON DISEASE.DISEASE_ID = SNP_AN_DISEASE.DISEASE_ID)
            INNER JOIN DISEASE_AS ON DISEASE_AS.DISEASE_ID = DISEASE.DISEASE_ID AND ( DISEASE_AS.GENE_SYMBOL = SNP_AN_AS.GENE_SYMBOL OR DISEASE_AS.GENE_SYMBOL = OTHER_SYMBOL.OTHER_SYMBOL ) )
            INNER JOIN AS_SOURCE ON AS_SOURCE.GENE_SYMBOL = DISEASE_AS.GENE_SYMBOL)
            WHERE SNP_AN.RS_ID IN ('rs9273363', 'rs12709430', 'rs12709426')
            ORDER BY SNP_AN.CHROMOSOME DESC, SNP_AN.POSITION ASC;
        """
        
        myresult = self.CreateTask(conn, sqlCommand, '')
        
        self.CloseDatabase(conn)
        
        for x in myresult:
            print(x)
            
    def ToolSearchWithRSIDViaPathWay(self):
        conn = self.ConnectDatabase()
        
        # rs9272219
        RSID_INPUT = str(input('Search with RS_ID : '))
        
        sqlCommand = """
            SELECT 
                SNP_AN.RS_ID,
                SNP_AN.PROBE_ID,
                SNP_AN.CHROMOSOME,
                SNP_AN.POSITION,
                SNP_AN.SOURCE_NAME,
                SNP_AN_AS_DETAIL.RELATIONSHIP, 
                SNP_AN_AS_DETAIL.DISTANCE,
                SNP_AN_AS.GENE_SYMBOL,
                OTHER_SYMBOL.OTHER_SYMBOL,
                DISEASE.DISEASE_NAME,
                PATHWAY.PATHWAY_ID,
                PATHWAY.GENE_ID
            FROM ( ( ( ( ( ( ( SNP_AN 
            INNER JOIN SNP_AN_DISEASE ON SNP_AN_DISEASE.RS_ID = SNP_AN.RS_ID )
            INNER JOIN SNP_AN_AS ON SNP_AN_AS.RS_ID = SNP_AN.RS_ID)
            INNER JOIN SNP_AN_AS_DETAIL ON SNP_AN_AS_DETAIL.RS_ID = SNP_AN_AS.RS_ID AND SNP_AN_AS_DETAIL.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID)
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            INNER JOIN DISEASE ON DISEASE.DISEASE_ID = SNP_AN_DISEASE.DISEASE_ID)
            INNER JOIN PATHWAY ON PATHWAY.GENE_ID = SNP_AN_AS.GENE_ID )
            WHERE SNP_AN.RS_ID = %s
            ORDER BY SNP_AN.CHROMOSOME ASC, SNP_AN.POSITION ASC;
        """
        
        myresult = self.CreateTask(conn, sqlCommand, (RSID_INPUT, ))
        
        self.CloseDatabase(conn)
        
        for x in myresult:
            print(x)
        
    # 11-Jun-2021 => 1623344400.0
    def ConvertUpdateAtToTimeStamp(self, datetimeInput):
        timeOutput = datetime.datetime.strptime(str(datetimeInput), "%Y-%m-%d %H:%M:%S")
        timeOutput = datetime.datetime.timestamp(timeOutput)
        return timeOutput
        
    def CloseDatabase(self, conn):
        try:
            if conn.is_connected():
                cur = conn.cursor()
                cur.close()
                conn.close()
        except Error as e:
            print("Error while connecting to MySQL", e)       
            
        return 

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
    
    def ReadUpdateNcbiData(self):
        return pd.read_csv( self.pathToDataSet + "/UpdateGeneWithMap.csv" )
    
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
    
    def GetPathToUpdateGeneWithMap(self):
        return self.pathToDataSet + "/UpdateGeneWithMap.csv"
    
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
        return self.dataOnMetadata
    
    def UpdateMetadata(self, columnName, inputData):
        self.dataOnMetadata['technical'][columnName] = inputData
        return
    
    def SaveUpdateMetadata(self):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( self.dataOnMetadata, outfile)
        return
    
    def SaveManualUpdateMetadata(self, inputData):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( inputData, outfile)
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
    
    # database = Database()
    
    # database.CreateDatabase()
    # database.InitializeData()
    # database.SwapNcbiToALSO_KNOW_AS('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/GeneWithMapBK-2.csv')
    # database.SwapMainDataToSNP_AN('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/Project/Dataset/MainCSV/MainData_Nsp.csv')
    
    database = Initialize()
    # database.InsertOldDataToDatabase()
    # database.ToolSearchWithRSID()
    # database.ToolSearchWithProbeID()
    # database.NotFoundDiseaseWithRSID()
    # database.ToolSearchWithListRSID()
    database.ToolSearchWithRSIDViaPathWay()
    
    print('Main')