import pandas as pd
import urllib.request
import os
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup as soup
from Class_Initialization import GetDataFromFile, MetaData, Database, Initialize
import time
import sqlite3

"""
Global variable
"""
listNcbiUpdated = []

"""
Model of GeneWithMap
"""
class GeneWithMap():
    def __init__(self, _GeneID, _GeneSymbol, _AlsoKnowAs, _UpdatedAt):
        self.GeneID = _GeneID
        self.GeneSymbol = _GeneSymbol
        self.AlsoKnowAs = _AlsoKnowAs
        self.UpdatedAt = _UpdatedAt

"""
Class Createncbi uses to fetch data from ncbi website by that will send each a geneID to website or suffix back.
After send request to website, this class will use urllib to get some data in HTML such as AlsoKnowAs.

** Any data must store at ** pathToDataSet **
"""
class Createncbi(Thread, GetDataFromFile, Database):
    
    # initialize value
    listGenesID = []
    indexStart = 0
    indexStop = 0
    pathGeneWithMap = ''
    
    def __init__(self, _ListGenesID, _IndexStart, _IndexStop):
        Thread.__init__(self)
        GetDataFromFile.__init__(self)
        Database.__init__(self)
        
        self.listGenesID = _ListGenesID
        self.indexStart = _IndexStart
        self.indexStop = _IndexStop
        self.pathGeneWithMap = self.GetPathToGeneData() + '/gene' + str(_IndexStart) + "_" + str(_IndexStop) + ".csv"
        
    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
    
    def CreateFile(self):
        ncbiPandas = pd.DataFrame( data=[], columns=[self.ncbiHeader] ) # set Initialize of csv file
        ncbiPandas.to_csv( self.pathGeneWithMap, index = False ) # create csv file for each multi thread
    
    def SendRequestToNcbi(self, geneID):
        isCompleted = False
        while ( isCompleted == False):
            try :
                urlNcbi = self.sourceWebsite['ncbi'] + '/' + str(geneID)
                print( urlNcbi )
                res = soup(urllib.request.urlopen( urlNcbi ), 'html.parser')
                isCompleted = True
            except:
                pass
                
        return res
    
    def FetchGeneID(self, index):
        geneID = self.listGenesID['GeneID'][index]
        return geneID
    
    def FetchOfficialSymbol(self, response):
        resDDArray = response.find_all('dd')
        officialSymbol = resDDArray[0].contents[0]
        return officialSymbol
    
    def FetchUpdateOn(self, response):
        resHeader = response.find('span', {"class": "geneid"})
        timeStampUpdateOn = ( ( ( str( resHeader.renderContents ) ).split() )[-1].split('<') )[0]
        return timeStampUpdateOn
    
    def FetchAlsoKnowAs(self, response):
        resDDArray = response.find_all()
        indexAlsoKnowAs = resDDArray.index( response.find('dt', text = 'Also known as') )
        alsoKnownAs = resDDArray[indexAlsoKnowAs + 1].contents
        return alsoKnownAs
        
    def run(self):
        listGene = []
        self.CreateFile() # set initialization
        
        # for _Index in range(self.indexStart, self.indexStop + 1):
        for _Index in range(self.indexStart, self.indexStart + 2):
            geneID = self.FetchGeneID(_Index)
            
            response = self.SendRequestToNcbi(geneID)
            
            resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website
            
            officialSymbol = self.FetchOfficialSymbol(resSummaryDl)
            
            UpdateOn = self.ConvertDatetimeToTimeStamp(self.FetchUpdateOn(response))
            
            if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ): # Does the website contain "Also known as" ?
                alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
            else:
                alsoKnownAs = ['']
                
            data = GeneWithMap(
                _GeneID = geneID,
                _GeneSymbol = officialSymbol,
                _AlsoKnowAs = alsoKnownAs,
                _UpdatedAt = UpdateOn
            )
            
            dataFromWeb = pd.DataFrame(data.__dict__)
            dataFromWeb.to_csv( self.pathGeneWithMap , mode='a', index = False, header=False)
        
        return
    

"""
Class UpdateNcbi is used to update information through each thread on the computer by will separate the data and check each data.
If the date of the website does not match the old date of the data, it will fetch the new data and replace it.
"""
class UpdateNcbi(Thread, GetDataFromFile, Initialize):
    listDataUnCheck = []
    startIndex = 0
    
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
        
    def SendRequestToNcbi(self, geneID):
        # Try send request to Ncbi website
        isCompleted = False
        while ( isCompleted == False):
            try :                   
                res = soup(urllib.request.urlopen(self.sourceWebsite['ncbi'] + '/' + str(geneID) ), 'html.parser')
                isCompleted = True
            except:
                pass
                
        return res
    
    def FetchUpdateOn(self, response):
        resHeader = response.find('span', {"class": "geneid"})
        resUpdateOn = ( ( ( str( resHeader.renderContents ) ).split() )[-1].split('<') )[0]
        timeStampUpdateOn = self.ConvertDatetimeToTimeStamp(resUpdateOn)
        return timeStampUpdateOn
    
    def FetchOfficialSymbol(self, response):
        resDDArray = response.find_all('dd')
        officialSymbol = resDDArray[0].contents[0]
        return officialSymbol
    
    def FetchAlsoKnowAs(self, response):
        resDDArray = response.find_all()
        indexAlsoKnowAs = resDDArray.index( response.find('dt', text = 'Also known as') )
        alsoKnownAs = resDDArray[indexAlsoKnowAs + 1].contents
        return alsoKnownAs
        
    def run(self):
        for GeneID, UpdateAt in self.listDataUnCheck[0:1]:
            
            response = self.SendRequestToNcbi( GeneID )
            updatedOn_Website = self.FetchUpdateOn(response)
            updatedOn_OldData = self.ConvertUpdateAtToTimeStamp(UpdateAt)
            print( updatedOn_OldData, '<==>', updatedOn_Website)
            if ( updatedOn_OldData == updatedOn_Website):
                print('GeneID :', GeneID, 'Not update yet\n')
                continue
            else:
                print('GeneID :', GeneID, 'Let\'s update')
                
                resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website
                
                officialSymbol = self.FetchOfficialSymbol(resSummaryDl)
                
                if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ):
                    alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
                else:
                    alsoKnownAs = None
                
                df = self.ReadUpdateNcbiData()
                
                new_row = ( GeneID, officialSymbol, alsoKnownAs, updatedOn_Website )
                
                listNcbiUpdated.append(new_row)

class NcbiInfo(Initialize):
    numberOfRow = None
    numberOfThread = 1
    
    # ------ Default function ------ #
    
    def __init__(self, _NumberOfThread):
        # GetDataFromFile.__init__(self)
        Initialize.__init__(self)
        self.numberOfThread = _NumberOfThread
    
    def ChangeNumberOfThread(self, _NumberOfThread):
        self.numberOfThread = _NumberOfThread
        return
    
    # ------ Ncbi function ------ #
    
    def UpdateNcbiInformation(self):
        metaData = MetaData()
        
        conn = self.ConnectDatabase()
        print('connect database')
        sqlCommand = """
            SELECT * FROM NCBI;
        """
        ncbiData = self.CreateTask(conn, sqlCommand, () )
        
        lengthNcbiData = len( ncbiData )
        lengthEachRound = lengthNcbiData // self.numberOfThread
        startIndex = 0
        threadArray = []
        for count in range( self.numberOfThread ):
            
            if ( count != ( self.numberOfThread - 1) ):
                updateNcbi = UpdateNcbi(
                    _ListDataUnCheck = ncbiData[lengthEachRound * count : ( lengthEachRound * count ) + lengthEachRound],
                    _StartIndex = startIndex
                )
            else:
                updateNcbi = UpdateNcbi(
                    _ListDataUnCheck = ncbiData[lengthEachRound * count : lengthNcbiData],
                    _StartIndex = startIndex
                )
                
            threadArray.append(updateNcbi)
            startIndex = startIndex + lengthEachRound
                
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
        
        # GET OLD OTHER SYMBOL OF GENE ID
        # SELECT * FROM TestCommand.OTHER_SYMBOL
        # WHERE TestCommand.OTHER_SYMBOL.GENE_ID = 79147 AND
        # TestCommand.OTHER_SYMBOL.OTHER_SYMBOL NOT IN ('MDC1C', 'LGMD2I', 'LGMDR9', 'MDDGA5', 'MDDGB5', 'MDDGC5');
        
        for ncbiData in listNcbiUpdated:
            # print( '\n', ncbiData[0], ncbiData[2])
            if ( ncbiData[2] != None ):
                GeneID = ncbiData[0]
                ListOtherSymbol = ( list(map(str, (ncbiData[2][0]).split('; '))) )
                UpdateAt = datetime.fromtimestamp(ncbiData[3]).strftime('%Y-%m-%d %H:%M:%S')
                
                # Update Update_at field on database
                sqlCommand = """
                    UPDATE NCBI SET
                    UPDATE_AT = %s WHERE
                    GENE_ID = %s
                """
                self.CreateTask( conn, sqlCommand, (UpdateAt, GeneID) )
                
                Records = [GeneID] + ListOtherSymbol
                FormatStrings = ', '.join(['%s'] * len(str(ncbiData[2]).split('; ')))
                
                # Delete the other symbol if new other symbol list not match with old other symbol field
                sqlCommand = """
                    DELETE FROM OTHER_SYMBOL
                    WHERE OTHER_SYMBOL.GENE_ID = %%s
                    AND OTHER_SYMBOL.OTHER_SYMBOL NOT IN (%s);
                """ % FormatStrings
                
                self.CreateTask(conn, sqlCommand, Records )
                
                # insert new data if other symbol not exist
                sqlCommand = """
                    INSERT IGNORE INTO OTHER_SYMBOL ( GENE_ID, OTHER_SYMBOL )
                    VALUE (%s, %s)
                """
                
                for OtherSymbol in ListOtherSymbol:
                    print( GeneID, OtherSymbol )
                    self.CreateTask(conn, sqlCommand, (GeneID, OtherSymbol, ) )
            
            
        self.CloseDatabase(conn)
        
        metaData.ReadMetadata('MapSnpWithNcbi')
        metaData.UpdateMetadata('lastMedoficationTime', time.time())
        metaData.SaveUpdateMetadata()

        return
    
    def CombineDataNcbi(self):
        dfs = []
        conn = self.ConnectDatabase()
        
        for filename in os.listdir(self.GetPathToGeneData()):
            if ( filename == ".DS_Store"):
                continue
            else:
                data = pd.read_csv(self.GetPathToGeneData() + '/' + filename)
                
                for row_index, row in data.iterrows():
                    print( str(row['AlsoKnowAs']), type(row['AlsoKnowAs']) )
                    if ( str(row['AlsoKnowAs']) == 'nan' ):
                        sqlCommand = ''' INSERT INTO ALSO_KNOW_AS(GENEID,UPDATE_AT) VALUES(?,?) '''
                        self.CreateTask(conn, sqlCommand, (row['GeneID'], row['UpdatedAt']))
                    else:
                        sqlCommand = ''' INSERT INTO ALSO_KNOW_AS(GENEID,OTHER_SYMBOL,UPDATE_AT) VALUES(?,?,?) '''
                        self.CreateTask(conn, sqlCommand, (row['GeneID'], row['AlsoKnowAs'], row['UpdatedAt']))
                    
                os.remove(self.GetPathToGeneData() + '/' + filename)
        
        return
    
    def CreateNubiInformation(self):
        metaData = MetaData()
        listUniqueGeneID = self.ReadAllUniqueGeneID()
        
        lengthUniqueGeneID = len( listUniqueGeneID )
        lengthEachRound = lengthUniqueGeneID // self.numberOfThread
    
        threadArray = []
        for count in range(self.numberOfThread): # Number of Thread CPU
            if ( count != ( self.numberOfThread - 1) ):
                eachThread = Createncbi(
                    _ListGenesID = listUniqueGeneID,
                    _IndexStart = lengthEachRound * count,
                    _IndexStop = ( lengthEachRound * count ) + lengthEachRound
                )
            else:
                eachThread = Createncbi(
                    _ListGenesID = listUniqueGeneID,
                    _IndexStart = lengthEachRound * count,
                    _IndexStop = lengthUniqueGeneID
                )
                
            threadArray.append(eachThread)
            
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
        
        # Wait all mutithread has successfully process before start combine all data
        self.CombineDataNcbi()
        
        metaData.ReadMetadata('MapSnpWithNcbi')
        metaData.UpdateMetadata('createionTime', time.time())
        metaData.UpdateMetadata('lastMedoficationTime', time.time())
        metaData.SaveUpdateMetadata()
            
        return



if __name__ == "__main__":
    ncbiInfo = NcbiInfo(
        _NumberOfThread = 5
    )
    
    # ncbiInfo.CreateNubiInformation()
    ncbiInfo.UpdateNcbiInformation()
    
    print('run main')