import os
import pandas as pd
import json

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