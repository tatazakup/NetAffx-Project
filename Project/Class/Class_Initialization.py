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
    
    ncbiHeader = ['geneID', 'geneSymbol', 'alsoKnowAs', 'createAt', 'updatedAt']
    diseaseHeader = pd.DataFrame( data=[], columns=['geneSymbol', 'ganeID'] )
    
    def __init__(self):
        return
    
    def ReadAllUniqueGeneID(self):
        return pd.read_csv( self.pathToDataSet + "/GeneNotSame.csv" )
    
    def ReadNcbiData(self):
        return pd.read_csv( self.pathToDataSet + "/GeneWithMap.csv" )
    
    def ReadListDisease(self):
        return pd.read_csv( self.pathToDataSet + "/ListDisease.csv" )
    
    def GetPathToGeneWithMap(self):
        return self.pathToDataSet + "/GeneWithMap.csv"
    
    def GetPathToListDisease(self):
        return self.pathToDataSet + "/Disease"
    
    def GetPathToGeneData(self):
        return self.pathToDataSet + "/GeneData"
    
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
    
    def UpdateMetadata(self, columnName):
        self.dataOnMetadata['technical']['columnName']
        return
    
    def SaveUpdateMetadata(self):
        self.jsonData.close()
        
        with open( self.pathToMetaData + '/' + self.metadataName + '.json' , 'w') as outfile:
            json.dump( self.dataOnMetadata, outfile)
        return