import os
import time
import pandas as pd
import urllib.request
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup as soup
from Initialization import Database, FilePath, LinkDataAndHeader, MetaData, GeneWithMap


"""
Global variable
"""
listNcbiUpdated = []

class CreateNcbi(Thread, Database, FilePath, LinkDataAndHeader):
    # initialize value
    listGenesID = []
    indexStart = 0
    indexStop = 0
    pathGeneWithMap = ''

    def __init__(self, ListGenesID, IndexStart, IndexStop):
        Thread.__init__(self)
        FilePath.__init__(self)
        self.listGenesID = ListGenesID
        self.indexStart = IndexStart
        self.indexStop = IndexStop
        self.pathGeneWithMap = self.GetPathToNCBI() + '/gene' + str(IndexStart) + "_" + str(IndexStop) + ".csv"
        return

    def CreateFile(self):
        ncbiPandas = pd.DataFrame( data=[], columns=[self.ncbiHeader] ) # set Initialize of csv file
        ncbiPandas.to_csv( self.pathGeneWithMap, index = False ) # create csv file for each multi thread
        return
    
    def SendRequestToNcbi(self, geneID):
        isCompleted = False
        count = 0
        while ( isCompleted == False):
            if ( count == 5 ):
                return False
            try:
                urlNcbi = self.sourceWebsite['ncbi'] + '/' + str(geneID)
                res = soup(urllib.request.urlopen( urlNcbi ), 'html.parser')
                isCompleted = True
            except:
                count = count + 1
                pass
        
        return res
    
    def FetchGeneID(self, index):
        geneID = self.listGenesID[index]
        return geneID[0]

    def FetchOfficialSymbol(self, response):
        resDDArray = response.find_all('dd')
        officialSymbol = resDDArray[0].contents[0]
        return officialSymbol

    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput

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
        self.CreateFile() # set initialization

        for _Index in range(self.indexStart, self.indexStart + 2):

            geneID = self.FetchGeneID(_Index)

            response = self.SendRequestToNcbi(geneID)

            if ( response == False ):
                continue
            else:                
                resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website

                officialSymbol = self.FetchOfficialSymbol(resSummaryDl)

                UpdateOn = self.ConvertDatetimeToTimeStamp(self.FetchUpdateOn(response))

                if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ): # Does the website contain "Also known as" ?
                    alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
                else:
                    alsoKnownAs = ['']

                data = GeneWithMap(
                    GeneID = geneID,
                    GeneSymbol = officialSymbol,
                    AlsoKnowAs = alsoKnownAs,
                    UpdatedAt = UpdateOn
                )

                dataFromWeb = pd.DataFrame(data.__dict__)
                dataFromWeb.to_csv( self.pathGeneWithMap , mode='a', index = False, header=False)

        return

class Ncbi(Database, MetaData, FilePath):
    numberOfRow = None
    numberOfThread = 1

    def __init__(self, _NumberOfThread):
        self.numberOfThread = _NumberOfThread
        return
    
    def CombineDataNcbi(self):
        database = Database()
        conn = database.ConnectDatabase()
        
        for filename in os.listdir(self.GetPathToNCBI()):
            if ( filename == ".DS_Store"):
                continue
            else:
                data = pd.read_csv(self.GetPathToNCBI() + '/' + filename)
                
                for row_index, row in data.iterrows():
                    if ( str(row['AlsoKnowAs']) == 'nan' ):
                        sqlCommand = ''' INSERT INTO ALSO_KNOW_AS(GENEID,UPDATE_AT) VALUES(?,?) '''
                        database.CreateTask(conn, sqlCommand, (row['GeneID'], row['UpdatedAt']))
                    else:
                        sqlCommand = ''' INSERT INTO ALSO_KNOW_AS(GENEID,OTHER_SYMBOL,UPDATE_AT) VALUES(?,?,?) '''
                        database.CreateTask(conn, sqlCommand, (row['GeneID'], row['AlsoKnowAs'], row['UpdatedAt']))
                    
                os.remove(self.GetPathToNCBI() + '/' + filename)
        
        database.CloseDatabase(conn)
        
        return
    
    def CreateNcbiInformation(self):
        metaData = MetaData()
        database = Database()

        conn = database.ConnectDatabase()
        mysqlCommand = """
            SELECT DISTINCT GENE_ID FROM snp_an_as;
        """
        listUniqueGeneID = database.CreateTask(conn, mysqlCommand, ())
        database.CloseDatabase(conn)

        lengthUniqueGeneID = len( listUniqueGeneID )
        lengthEachRound = lengthUniqueGeneID // self.numberOfThread        

        threadArray = []

        for count in range(self.numberOfThread): # Number of Thread CPU
            if ( count != ( self.numberOfThread - 1) ):
                eachThread = CreateNcbi(
                    ListGenesID = listUniqueGeneID,
                    IndexStart = lengthEachRound * count,
                    IndexStop = ( lengthEachRound * count ) + lengthEachRound
                )
            else:
                eachThread = CreateNcbi(
                    ListGenesID = listUniqueGeneID,
                    IndexStart = lengthEachRound * count,
                    IndexStop = lengthUniqueGeneID
                )
                
            threadArray.append(eachThread)
        
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()
        
        # Wait all mutithread has successfully process before start combine all data
        self.CombineDataNcbi()

        return

if __name__ == "__main__":
    ncbi = Ncbi(5)
    ncbi.CreateNcbiInformation()
