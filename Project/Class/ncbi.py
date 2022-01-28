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
        self.pathGeneWithMap = self.GetPathToNCBI() + '/gene' + str(IndexStart + 1) + "_" + str(IndexStop + 1) + ".csv"
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

    def FetchUpdateOn(self, response):
        resHeader = response.find('span', {"class": "geneid"})
        timeStampUpdateOn = ( ( ( str( resHeader.renderContents ) ).split() )[-1].split('<') )[0]
        return timeStampUpdateOn

    def FetchAlsoKnowAs(self, response):
        resDDArray = response.find_all()
        indexAlsoKnowAs = resDDArray.index( response.find('dt', text = 'Also known as') )
        alsoKnownAs = resDDArray[indexAlsoKnowAs + 1].contents
        return alsoKnownAs

    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
    
    def run(self):
        self.CreateFile() # set initialization

        for _Index in range(self.indexStart, self.indexStop + 1):
        # for _Index in range(self.indexStart, self.indexStart + 5):

            geneID = self.FetchGeneID(_Index)

            # print( '_Index :', _Index, 'GeneID :', geneID )

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

class UpdateNcbi(Thread, Database, FilePath, LinkDataAndHeader):
    listDataUnCheck = []
    startIndex = 0
    
    def __init__(self, ListDataUnCheck, StartIndex):
        Thread.__init__(self)
        FilePath.__init__(self)
        self.listDataUnCheck = ListDataUnCheck
        self.startIndex = StartIndex
    
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

    # From Website to database
    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput

    # From Database to compare with another
    # 11-Jun-2021 => 1623344400.0
    def ConvertUpdateAtToTimeStamp(self, datetimeInput):
        timeOutput = datetime.strptime(str(datetimeInput), "%Y-%m-%d %H:%M:%S")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput

    def run(self):
        for GeneID, UpdateAt in self.listDataUnCheck[:5]:
            
            response = self.SendRequestToNcbi( GeneID )
            updatedOn_Website = self.FetchUpdateOn(response)
            updatedOn_OldData = self.ConvertUpdateAtToTimeStamp(UpdateAt)

            print('GeneID :', GeneID, ':', updatedOn_Website, updatedOn_OldData)

            if ( updatedOn_OldData == updatedOn_Website):
                print('GeneID :', GeneID, 'last updated')
                continue
            else:
                resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website
                
                officialSymbol = self.FetchOfficialSymbol(resSummaryDl)
                
                # Check Also Know As
                if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ):
                    alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
                else:
                    alsoKnownAs = None
                
                new_row = ( GeneID, officialSymbol, alsoKnownAs, updatedOn_Website )
                
                listNcbiUpdated.append(new_row)
                print('GeneID :', GeneID, 'updated ||', new_row)
        
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

                    timestamp = datetime.fromtimestamp(row['UpdatedAt']).strftime('%Y-%m-%d %H:%M:%S')
                    geneID = row['GeneID']
                    sqlCommand = """
                        REPLACE INTO ncbi ( GENE_ID, UPDATE_AT )
                        VALUES ( %s, %s ) 
                    """
                    database.CreateTask(conn, sqlCommand, (geneID, timestamp))

                    if ( str(row['AlsoKnowAs']) != 'nan' ):
                        otherSymbol = row['AlsoKnowAs'].split('; ')
                        for eachSymbol in otherSymbol:
                            sqlCommand = """
                                REPLACE INTO other_symbol ( GENE_ID, OTHER_SYMBOL )
                                VALUES ( %s, %s )
                            """
                            self.CreateTask(conn, sqlCommand, (geneID, eachSymbol) )
                    
                os.remove(self.GetPathToNCBI() + '/' + filename)
        
        database.CloseDatabase(conn)
        
        return
    
    def CreateNcbiInformation(self):
        database = Database()

        conn = database.ConnectDatabase()
        mysqlCommand = """
            SELECT DISTINCT GENE_ID FROM gene_snp;
        """
        listUniqueGeneID = database.CreateTask(conn, mysqlCommand, ())
        database.CloseDatabase(conn)

        lengthUniqueGeneID = len( listUniqueGeneID ) - 1
        lengthEachRound = lengthUniqueGeneID // self.numberOfThread        
        threadArray = []

        for count in range(self.numberOfThread): # Number of Thread CPU
            if ( count != ( self.numberOfThread - 1) ):
                eachThread = CreateNcbi(
                    ListGenesID = listUniqueGeneID,
                    IndexStart = lengthEachRound * count,
                    IndexStop = ( ( lengthEachRound * count ) + lengthEachRound ) - 1
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

    def UpdateNcbiInformation(self):
        database = Database()

        conn = database.ConnectDatabase()
        mysqlCommand = """
            SELECT * FROM ncbi;
        """
        ncbiData = database.CreateTask(conn, mysqlCommand, ())

        lengthNcbiData = len( ncbiData )
        lengthEachRound = lengthNcbiData // self.numberOfThread
        startIndex = 0
        threadArray = []

        for count in range( self.numberOfThread ):
            
            if ( count != ( self.numberOfThread - 1) ):
                updateNcbi = UpdateNcbi(
                    ListDataUnCheck = ncbiData[lengthEachRound * count : ( lengthEachRound * count ) + lengthEachRound],
                    StartIndex = startIndex
                )
            else:
                updateNcbi = UpdateNcbi(
                    ListDataUnCheck = ncbiData[lengthEachRound * count : lengthNcbiData],
                    StartIndex = startIndex
                )
                
            threadArray.append(updateNcbi)
            startIndex = startIndex + lengthEachRound
                
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()

        for ncbiData in listNcbiUpdated:

            GeneID = ncbiData[0]
            UpdateAt = datetime.fromtimestamp(ncbiData[3]).strftime('%Y-%m-%d %H:%M:%S')

            # Update Update_at field on database
            sqlCommand = """
                UPDATE ncbi SET
                UPDATE_AT = %s WHERE
                GENE_ID = %s
            """
            database.CreateTask( conn, sqlCommand, (UpdateAt, GeneID) )

            if ( ncbiData[2] != None ):
                
                ListOtherSymbol = ( list(map(str, (ncbiData[2][0]).split('; '))) )
                Records = [GeneID] + ListOtherSymbol
                FormatStrings = ', '.join(['%s'] * len(str(ncbiData[2]).split('; ')))
                
                # Delete the other symbol if new other symbol list not match with old other symbol field
                sqlCommand = """
                    DELETE FROM other_symbol
                    WHERE other_symbol.GENE_ID = %%s
                    AND other_symbol.OTHER_SYMBOL NOT IN (%s);
                """ % FormatStrings
                
                database.CreateTask(conn, sqlCommand, Records )
                
                # insert new data if other symbol not exist
                sqlCommand = """
                    INSERT IGNORE INTO other_symbol ( GENE_ID, OTHER_SYMBOL )
                    VALUE (%s, %s)
                """
                
                for OtherSymbol in ListOtherSymbol:
                    database.CreateTask(conn, sqlCommand, (GeneID, OtherSymbol, ) )
            
            
        database.CloseDatabase(conn)

        return

if __name__ == "__main__":
    ncbi = Ncbi(5)
    ncbi.UpdateNcbiInformation()
