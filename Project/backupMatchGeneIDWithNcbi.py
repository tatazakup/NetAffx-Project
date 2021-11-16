import pandas as pd
import urllib.request
import os
import time
from bs4 import BeautifulSoup as soup
from threading import Thread
from datetime import datetime

class ncbi(Thread):
    
    # initialize value
    ncbiHeader = pd.DataFrame( data=[], columns=['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'CreateAt', 'UpdatedAt'] )
    genesID = []
    indexStart = 0
    indexStop = 0
    officialSymbol = ''
    alsoKnownAs = []
    dataNcbi = None
    
    def __init__(self, _geneID, _indexStart, _indexStop):
        Thread.__init__(self)
        
        self.genesID = _geneID
        self.indexStart = _indexStart
        self.indexStop = _indexStop
        
    def CreateFileCSV(self):
        self.ncbiHeader.to_csv( os.getcwd() + "/GetDataOnWe/Dataset/gene" + str(self.indexStart) + "_" + str(self.indexStop) + ".csv")
        return
    
    def ReadDataFormap(self):
        dataFormap = pd.read_csv(os.getcwd() + "/GetDataOnWe/Dataset/GeneNotSame.csv")
        return dataFormap
    
    def ReadDataNcbi(self):
        self.dataNcbi = pd.read_csv(os.getcwd() + "/GetDataOnWe/Dataset/gene" + str(self.indexStart) + "_" + str(self.indexStop) + ".csv")
    
    def ClearTemporaryVariable(self):
        self.officialSymbol = ''
        self.alsoKnownAs = []
        
    def run(self):
        self.CreateFileCSV()
        self.ReadDataNcbi()
        
        for _Index in range(self.indexStart, self.indexStop + 1):
            self.ClearTemporaryVariable()
            geneID = self.genesID['GeneID'][_Index]
            
            try :
                resp_text = soup(urllib.request.urlopen('https://www.ncbi.nlm.nih.gov/gene/' + str(geneID)), 'html.parser').find('dl', {"id": "summaryDl"})
            except:
                try:
                    resp_text = soup(urllib.request.urlopen('https://www.ncbi.nlm.nih.gov/gene/' + str(geneID)), 'html.parser').find('dl', {"id": "summaryDl"})
                except:
                    resp_text = soup(urllib.request.urlopen('https://www.ncbi.nlm.nih.gov/gene/' + str(geneID)), 'html.parser').find('dl', {"id": "summaryDl"})
            
            resp_text_array = resp_text.find_all('dd')
            
            self.officialSymbol = resp_text_array[0].contents[0]
            
            if ( len( resp_text.find_all(text = 'Also known as') ) >= 1 ):
                
                resp_text_array = resp_text.find_all()
                indexOldSymbol = resp_text_array.index( resp_text.find('dt', text = 'Also known as') )
                self.alsoKnownAs = resp_text_array[indexOldSymbol + 1].contents
                
            symbols = " " 
            data = {
                '' : '',
                'GeneID': geneID,
                'GeneSymbol': self.officialSymbol,
                'AlsoKnowAs': [self.alsoKnownAs],
                'CreateAt': datetime.now(),
                'UpdatedAt': datetime.now(),
            }
            
            self.dataNcbi = pd.DataFrame(data)
            self.dataNcbi.to_csv( os.getcwd() + "/GetDataOnWe/Dataset/gene" + str(self.indexStart) + "_" + str(self.indexStop) + ".csv" , mode='a', index = False, header=False)
            
            print(data)
            
            print('\n')
            
        return


def CreateFileCSV():
    ncbi = pd.DataFrame( data=[], columns=['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'CreateAt', 'UpdatedAt'] )
    ncbi.to_csv( os.getcwd() + "/GetDataOnWe/Dataset/ncbi.csv" )
    return
    
def ReadDataFormap():
    data = pd.read_csv(os.getcwd() + "/GetDataOnWe/Dataset/miss.csv")
    return data

if __name__ == "__main__":
    # CreateFileCSV()
    datas = ReadDataFormap()
    df = pd.DataFrame(datas)
    print(df)
    FT = 252
    startat = 0
    
    tempThreadArray = []
    for count in range(1): 
        tempThread = ncbi(df, startat + (count * FT) , startat + ( count * FT + (FT - 1) ) )
        tempThreadArray.append(tempThread)
        
    for eachThread in tempThreadArray:
        eachThread.start()
        
    for eachThread in tempThreadArray:
        eachThread.join()
    
    
    # resp_text = soup(urllib.request.urlopen('https://www.ncbi.nlm.nih.gov/gene/' + str(2565)), 'html.parser').find('dl', {"id": "summaryDl"})
    # resp_text_array = resp_text.find_all()
    
    # print( resp_text_array.index( resp_text.find('dt', text = 'Also known as') ) )
    # print( resp_text_array[21].contents )