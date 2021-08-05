import pandas as pd
import urllib.request
import os
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup as soup
from Class_Initialization import GetDataFromFile
import time
import requests

"""
Class Createncbi uses to fetch data from ncbi website by that will send each a geneID to website or suffix back.
After send request to website, this class will use urllib to get some data in HTML such as AlsoKnowAs.

** Any data must store at ** sourceForStore **
"""
class Createncbi(Thread, GetDataFromFile):
    
    # initialize value
    genesID = []
    indexStart = 0
    indexStop = 0
    
    dataNcbi = None
    geneID = None
    officialSymbol = ''
    alsoKnownAs = []
    timeStampUpdateOn = None
    
    def __init__(self, _GeneID, _IndexStart, _IndexStop):
        Thread.__init__(self)
        GetDataFromFile.__init__(self)
        
        self.genesID = _GeneID
        self.indexStart = _IndexStart
        self.indexStop = _IndexStop
        
    def ClearTemporaryVariable(self):
        self.officialSymbol = ''
        self.alsoKnownAs = []
        self.timeStampUpdateOn = None
        self.geneID = None
        
    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
        
    def run(self):
        pathDefault = self.GetPathToGeneData() + '/gene' + str(self.indexStart) + "_" + str(self.indexStop) + ".csv"
        self.ncbiHeader.to_csv( pathDefault )
        self.dataNcbi = pd.read_csv( pathDefault )
        
        for _Index in range(self.indexStart, self.indexStop + 1):
            self.geneID = self.genesID['GeneID'][_Index]
            
            # Try send request to Ncbi website
            isCompleted = False
            while ( isCompleted == False):
                try :
                    res = soup(urllib.request.urlopen(self.sourceNcbiWebsite + '/' + str(self.geneID) ), 'html.parser')
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
                'geneID': self.geneID,
                'geneSymbol': self.officialSymbol,
                'alsoKnowAs': [self.alsoKnownAs],
                'foundStatus': 1,
                'updatedAt': self.ConvertDatetimeToTimeStamp(resUpdateOn)
            }
            
            self.dataNcbi = pd.DataFrame(data)
            self.dataNcbi.to_csv( pathDefault , mode='a', index = False, header=False)
        
        return
    

"""
Class UpdateNcbi is used to update information through each thread on the computer by will separate the data and check each data.
If the date of the website does not match the old date of the data, it will fetch the new data and replace it.
"""
class UpdateNcbi(Thread, GetDataFromFile):
    listDataUnCheck = []
    startIndex = 0
    geneID = None
    officialSymbol = ''
    alsoKnownAs = []
    timeStampUpdateOn = None
    listDataUpdate = []
    
    def __init__(self, _ListDataUnCheck, _StartIndex):
        Thread.__init__(self)
        GetDataFromFile.__init__(self)
        self.listDataUnCheck = _ListDataUnCheck
        self.startIndex = _StartIndex
        
    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, datetimeInput):
        timeOutput = datetime.strptime(datetimeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
    
    # 1623344400.0 => 11-Jun-2021
    def ConvertTimeStampToDatetime(self, TimeStampInput):
        timeOutput = datetime.fromtimestamp(TimeStampInput).strftime('%d-%b-%Y')
        return timeOutput
    
    def ClearTemporaryVariable(self):
        self.officialSymbol = ''
        self.alsoKnownAs = []
        self.timeStampUpdateOn = None
        self.geneID = None
        
    def run(self):
        for _Index in range(len(self.listDataUnCheck)):
            self.ClearTemporaryVariable()
            
            self.geneID = self.listDataUnCheck['geneID'][_Index + self.startIndex]
            updatedAt = self.listDataUnCheck['updatedAt'][_Index + self.startIndex]
            
            # Try send request to Ncbi website
            isCompleted = False
            while ( isCompleted == False):
                try :                   
                    res = soup(urllib.request.urlopen(self.sourceNcbiWebsite + '/' + str(self.geneID) ), 'html.parser')
                    isCompleted = True
                except:
                    pass
                
            # check UpdatedAt
            resHeader = res.find('span', {"class": "geneid"})
            resUpdateOn = ( ( ( str( resHeader.renderContents ) ).split() )[-1].split('<') )[0]
            self.timeStampUpdateOn = self.ConvertDatetimeToTimeStamp(resUpdateOn)
            
            print( self.timeStampUpdateOn, '<==>', updatedAt)
            if ( self.timeStampUpdateOn == updatedAt):
                print('Not update yet\n')
                continue
            else:
                print('Let\'s update')
                
                resSummaryDl = res.find('dl', {"id": "summaryDl"})
                resDDArray = resSummaryDl.find_all('dd')
                
                self.officialSymbol = resDDArray[0].contents[0]
                
                if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ):
                
                    resDDArray = resSummaryDl.find_all()
                    indexOldSymbol = resDDArray.index( resSummaryDl.find('dt', text = 'Also known as') )
                    self.alsoKnownAs = resDDArray[indexOldSymbol + 1].contents
                
                data = {
                    'geneID': self.geneID,
                    'geneSymbol': self.officialSymbol,
                    'alsoKnowAs': [self.alsoKnownAs],
                    'foundStatus': 1,
                    'updatedAt': self.timeStampUpdateOn
                }
                print( data )
                
                df = self.ReadNcbiData()
                df.loc[_Index + self.startIndex] = data
                df.to_csv( self.GetPathToGeneWithMap(), index=False)
        
        return

class NcbiInfo(GetDataFromFile):
    numberOfRow = None
    numberOfThread = 1
    
    # ---------------------------- #
    
    def __init__(self, _NumberOfThread):
        GetDataFromFile.__init__(self)
        self.numberOfThread = _NumberOfThread
    
    def ChangeNumberOfThread(self, _NumberOfThread):
        self.numberOfThread = _NumberOfThread
        return
    
    # ---------------------------- #
    
    def UpdateNcbiInformation(self):
        listUncheckData = self.ReadNcbiData()
        
        lengthUncheckData = len( listUncheckData )
        lengthEachRound = lengthUncheckData // self.numberOfThread
        startIndex = 0
        threadArray = []
        for count in range( self.numberOfThread ):
            
            if ( count != ( self.numberOfThread - 1) ):
                updateNcbi = UpdateNcbi(
                    _ListDataUnCheck = listUncheckData[lengthEachRound * count : ( lengthEachRound * count ) + lengthEachRound],
                    _StartIndex = startIndex
                )
            else:
                updateNcbi = UpdateNcbi(
                    _ListDataUnCheck = listUncheckData[lengthEachRound * count : lengthUncheckData],
                    _StartIndex = startIndex
                )
                
            threadArray.append(updateNcbi)
            startIndex = startIndex + lengthEachRound
                
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
            
        return
    
    def CreateNuciInformation(self):
        listUniqueGeneID = self.ReadAllUniqueGeneID()
        
        lengthUniqueGeneID = len( listUniqueGeneID )
        lengthEachRound = lengthUniqueGeneID // self.numberOfThread
    
        threadArray = []
        for count in range(self.numberOfThread): # Number of Thread CPU
            if ( count != ( self.numberOfThread - 1) ):
                print(lengthEachRound * count, ( lengthEachRound * count ) + lengthEachRound)
                eachThread = Createncbi(
                    _GeneID = listUniqueGeneID,
                    _IndexStart = lengthEachRound * count,
                    _IndexStop = ( lengthEachRound * count ) + lengthEachRound
                )
            else:
                print(lengthEachRound * count, lengthUniqueGeneID)
                eachThread = Createncbi(
                    _GeneID = listUniqueGeneID,
                    _IndexStart = lengthEachRound * count,
                    _IndexStop = lengthUniqueGeneID
                )
                
            threadArray.append(eachThread)
            
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
            
        return



if __name__ == "__main__":
    ncbiInfo = NcbiInfo(
        _NumberOfThread = 1
    )
    
    ncbiInfo.UpdateNcbiInformation()
    
    print('run main')