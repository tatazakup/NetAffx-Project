import os
import pandas as pd

class GetDataFromFile():
    
    sourceNcbiWebsite = r'https://www.ncbi.nlm.nih.gov/gene'
    
    pathToDataSet = os.getcwd() + "/Project/Dataset"
    pathToMetaData = os.getcwd() + "/GetDataOnWe/MetaData"
    
    ncbiHeader = pd.DataFrame( data=[], columns=['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'CreateAt', 'UpdatedAt'] )
    
    def __init__(self):
        return
    
    def ReadAllUniqueGeneID(self):
        return pd.read_csv( self.pathToDataSet + "/GeneNotSame.csv" )
    
    def ReadNcbiData(self):
        return pd.read_csv( self.pathToDataSet + "/GeneWithMap.csv" )
    
    def GetPathToGeneWithMap(self):
        return self.pathToDataSet + "/GeneWithMap.csv"
    
    def GetPathToGeneData(self):
        return self.pathToDataSet + "/GeneData"
    
    def GetPathToMetaData(self):
        return self.pathToMetaData
    
    def GetSourceNcbiWebsite(self):
        return self.sourceNcbiWebsite
