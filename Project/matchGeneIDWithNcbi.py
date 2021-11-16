import pandas as pd
import urllib.request
import os
import time
from bs4 import BeautifulSoup as soup
from threading import Thread
from datetime import datetime
import json
import logging

"""
Class ncbi uses to fetch data from ncbi website by that will send each a geneID to website or suffix back.
After send request to website, this class will use urllib to get some data in HTML such as AlsoKnowAs.

** Any data must store at ** sourceForStore **
"""
class ncbi(Thread):
    
    # initialize value
    ncbiHeader = pd.DataFrame( data=[], columns=['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'FoundStatus', 'UpdatedAt'] )
    sourceWebsite = r'https://www.ncbi.nlm.nih.gov/gene'
    sourceForStoreGene = ( os.getcwd() )
    sourceForStore = ( os.getcwd() )
    sourceMetadata = ( os.getcwd() )
    
    genesID = []
    indexStart = 0
    indexStop = 0
    officialSymbol = ''
    alsoKnownAs = []
    dataNcbi = None
    
    def __init__(self, _GeneID, _IndexStart, _IndexStop, _SourceForStore, _SourceMetadata):
        Thread.__init__(self)
        
        self.genesID = _GeneID
        self.indexStart = _IndexStart
        self.indexStop = _IndexStop
        self.sourceForStore = _SourceForStore
        self.sourceMetadata = _SourceMetadata
        self.sourceForStoreGene = _SourceForStore + "/GeneData"
        
        jsonData = open(self.sourceMetadata + '/' + 'MapSnpWithNcbi.json', 'r')
        
    def CreateCSVAlsoKnowAs(self):
        self.ncbiHeader.to_csv( self.sourceForStoreGene + '/gene' + str(self.indexStart) + "_" + str(self.indexStop) + ".csv")
        return 
    
    def ReadDataNcbi(self):
        self.dataNcbi = pd.read_csv( self.sourceForStoreGene + '/gene' + str(self.indexStart) + "_" + str(self.indexStop) + ".csv")
        return
    
    def ClearTemporaryVariable(self):
        self.officialSymbol = ''
        self.alsoKnownAs = []
        
    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
    
    # 1623344400.0 => 11-Jun-2021
    def ConvertTimeStampToDatetime(self, TimeStamp):
        
        return TimeStamp
        
    def CreateDataParallel(self):
        self.CreateCSVAlsoKnowAs()
        self.ReadDataNcbi()
        
        for _Index in range(self.indexStart, self.indexStop + 1):
            self.ClearTemporaryVariable()
            geneID = self.genesID['GeneID'][_Index]
            
            # Try send request to Ncbi website
            isCompleted = False
            while ( isCompleted == False):
                try :
                    res = soup(urllib.request.urlopen(self.sourceWebsite + '/' + str(geneID) ), 'html.parser')
                    isCompleted = True
                except:
                    pass
            
            resSummaryDl = res.find('dl', {"id": "summaryDl"})
            resDDArray = resSummaryDl.find_all('dd')
            
            self.officialSymbol = resDDArray[0].contents[0]
            
            resHeader = res.find('span', {"class": "geneid"})
            resUpdateOn = ( ( ( str( resHeader.renderContents ) ).split() )[-1].split('<') )[0]
            
            if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ):
                
                resDDArray = resSummaryDl.find_all()
                indexOldSymbol = resDDArray.index( resSummaryDl.find('dt', text = 'Also known as') )
                self.alsoKnownAs = resDDArray[indexOldSymbol + 1].contents
                
            data = {
                '' : '',
                'GeneID': geneID,
                'GeneSymbol': self.officialSymbol,
                'AlsoKnowAs': [self.alsoKnownAs],
                'FoundStatus': 1,
                'UpdatedAt': self.ConvertDatetimeToTimeStamp(resUpdateOn)
            }
            
            print( data )
            
            self.dataNcbi = pd.DataFrame(data)
            self.dataNcbi.to_csv( self.sourceForStoreGene + '/gene' + str(self.indexStart) + "_" + str(self.indexStop) + ".csv" , mode='a', index = False, header=False)
            
        return
        
    def run(self):
        self.CreateDataParallel()
            
        return
    
"""
Detail of Class
"""
class UpdateInformation():
    numberOfRow = None
    rangeEachRound = 19176
    startat = 0
    numberOfThread = 1
    sourceForStore = ( os.getcwd() )
    sourceMetadata = ( os.getcwd() )
    
    def __init__(self, _NumberOfThread, _RangeEachRound, _Startat, _SourceForStore, _SourceMetadata):
        self.startat = _Startat
        self.numberOfThread = _NumberOfThread
        self.rangeEachRound = _RangeEachRound
        self.sourceForStore = os.getcwd() + _SourceForStore
        self.sourceMetadata = os.getcwd() + _SourceMetadata
    
    def ReadDataFormap(self):
        data = pd.read_csv( self.sourceForStore + "/GeneNotSame.csv" )
        return data

    def CreateNcbiInformation(self):
        datas = self.ReadDataFormap()
        df = pd.DataFrame(datas)
    
        threadArray = []
        for count in range(self.numberOfThread): # Number of Thread CPU
            eachThread = ncbi(
                _GeneID = df,
                _IndexStart = self.startat + ( count * self.rangeEachRound ),
                _IndexStop = self.startat + ( count * self.rangeEachRound + (self.rangeEachRound - 1) ),
                _SourceForStore = self.sourceForStore,
                _SourceMetadata = self.sourceMetadata
            )
            threadArray.append(eachThread)
            
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
            
    def UpdateNcbiInformation(self):
        
        return
    
    def UpdateMetaDataNcbi(self):
        jsonData = open(self.sourceMetadata + '/' + 'MapSnpWithNcbi.json', 'r')
        metaData = json.load( jsonData )
        
        metaData['technical']['lastMedoficationTime'] = time.time()
        
        print( 'last modication time :', datetime.datetime.fromtimestamp( metaData['technical']['lastMedoficationTime'] ).strftime('%Y-%m-%d %H:%M:%S') )
        
        jsonData.close()
        
        with open( self.sourceMetadata + '/' + 'MapSnpWithNcbi.json' , 'w') as outfile:
            json.dump( metaData, outfile)
        return
    
    # Concatenate all data into one DataFrame
    def CombineDataNcbi(self):
        dfs = []
        for filename in os.listdir(self.sourceForStore + '/GeneData'):
            if ( filename == ".DS_Store"):
                continue
            else:
                dfs.append(pd.read_csv(self.sourceForStore + '/GeneData/' + filename))
            
        big_frame = pd.concat(dfs, ignore_index=True)
        Header = pd.DataFrame( big_frame, columns=['GeneID', 'GeneSymbol', 'AlsoKnowAs', 'FoundStatus', 'UpdatedAt'] )
        Header.to_csv( self.sourceForStore + '/GeneWithMap' + ".csv" , mode='a', index = False, header=True)
        # big_frame.to_csv( self.sourceForStore + '/GeneWithMap' + ".csv" , mode='a', index = False, header=False)
        
        return

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
    
    updateInformation = UpdateInformation(
        _NumberOfThread = 5,
        _RangeEachRound = 20,
        _Startat = 17600,
        _SourceForStore = "/GetDataOnWe/Dataset",
        _SourceMetadata = "/GetDataOnWe/MetaData" 
    )
    
    updateInformation.UpdateNcbiInformation()
    
    print('run main')

