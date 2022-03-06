import os
import time
import pandas as pd
import urllib.request
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup as soup
from Initialization import Database, FilePath, MetaData, GeneWithMap
import json
import re

"""
Global variable
"""

class CreateNcbi(Thread, Database, FilePath):
    # initialize value
    nameMetadata = ""
    listGenesID = []
    indexStart = 0
    indexStop = 0
    pathGeneWithMap = ''
    textFile = None

    def __init__(self, ThreadNumber, ListGenesID, IndexStart, IndexStop):
        Thread.__init__(self)
        FilePath.__init__(self)
        self.nameMetadata = "NCBI_CREATE_THREAD_" + str(ThreadNumber)
        self.listGenesID = ListGenesID
        self.indexStart = IndexStart
        self.indexStop = IndexStop
        self.pathGeneWithMap = self.GetPathToNCBI() + '/NCBI_CREATE_' + str(IndexStart + 1) + "_" + str(IndexStop + 1) + ".csv"

        # Create NCBI Log
        self.textFile = open(self.GetPathToNCBILogs() + "/NCBI_CREATE_THREAD_" + str(ThreadNumber) + ".txt","w+")
        return
    
    def SendRequestToNcbi(self, geneID):
        isCompleted = False
        count = 0
        while ( isCompleted == False):
            if ( count == 5 ):
                self.textFile.write("%s \r\n" % ("Status Gene " + str(geneID) + " : Request Fail") )
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
        # return geneID[0]
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

    # 11-Jun-2021 => 1623344400.0
    def ConvertDatetimeToTimeStamp(self, timeInput):
        timeOutput = datetime.strptime(timeInput, "%d-%b-%Y")
        timeOutput = datetime.timestamp(timeOutput)
        return timeOutput
    
    def FetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def CheckDiscontinue(self, GeneID):
        response = self.SendRequestToNcbi(GeneID)
        if ( response == False ):
            self.textFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneID) + " : Error", "Description : Data retrieved fails") )
            return False, []
        else:
            try:
                resHeader = response.find('span', {"class": "geneid"})
                if "discontinued" in str(resHeader.text):

                    resDiscontinue = response.find('ul', {"class": "gene-record-status"})
                    GeneID = (re.findall(r'(?<=\s)\d+', resDiscontinue.text))[0]

                    return self.CheckDiscontinue(GeneID)

                return str(GeneID), response
            except:
                self.textFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneID) + " : Error", "Description : Website Structure may change from origin") )
                return False, []

    def run(self):
        objectMapSnpWithNcbi = MetaData()
        objectThread = MetaData()

        dataMetaThread = self.FetchDataOnMetaData(objectThread, self.nameMetadata)

        startAt = dataMetaThread['count']
        if ( startAt == 0): self.indexStart = self.indexStart
        else: self.indexStart = self.indexStart + startAt - 1

        for _Index in range(self.indexStart, self.indexStop + 1):

            CurrentGeneID = self.FetchGeneID(_Index)
            OldGeneID = CurrentGeneID
            dataMetaThread['currentNumberOfGene'] = CurrentGeneID

            newGeneID, response = self.CheckDiscontinue(CurrentGeneID)
            if (int(newGeneID) != int(CurrentGeneID)):
                CurrentGeneID = newGeneID

            if ( response == False ):
                self.textFile.write("%s \n%s \n\r" % ("Status Gene " + str(CurrentGeneID) + " : Error", "Description : Data retrieved fails") )
                continue
            else:
                try:    
                    resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website

                    officialSymbol = self.FetchOfficialSymbol(resSummaryDl)

                    UpdateOn = self.ConvertDatetimeToTimeStamp(self.FetchUpdateOn(response))

                    if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ): # Does the website contain "Also known as" ?
                        alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
                    else:
                        alsoKnownAs = ['']
                except:
                    self.textFile.write("%s \n%s \n\r" % ("Status Gene " + str(CurrentGeneID) + " : Error", "Description : Website Structure may change from origin") )
                    continue

                data = GeneWithMap(CurrentGeneID = CurrentGeneID, OldGeneID = OldGeneID, GeneSymbol = officialSymbol, AlsoKnowAs = alsoKnownAs, UpdatedAt = UpdateOn)
                dataFromWeb = pd.DataFrame(data.__dict__)
                dataFromWeb.to_csv( self.pathGeneWithMap , mode='a', index = False, header=False)

            dataMetaThread['count'] = dataMetaThread['count'] + 1

            dataInMapSnpWithNcbi = self.FetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
            dataInMapSnpWithNcbi['technical']['createMeta']['amountOfFinished'] = dataInMapSnpWithNcbi['technical']['createMeta']['amountOfFinished'] + 1
            self.textFile.write("%s \n%s \n\r" % ("Status Gene " + str(CurrentGeneID) + " : successful", "Description : Data retrieved successfully") )

            if dataInMapSnpWithNcbi['technical']['createMeta']['status'] != 1:
                self.textFile.close()
                return
            else:
                objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
                objectThread.SaveManualUpdateMetadata(dataMetaThread)

        self.textFile.close()
        return

class UpdateNcbi(Thread, Database, FilePath):
    nameMetadata = ""
    listDataUnCheck = []
    startIndex = 0
    
    def __init__(self, ThreadNumber, ListDataUnCheck, IndexStart):
        Thread.__init__(self)
        FilePath.__init__(self)
        self.nameMetadata = "NCBI_UPDATE_THREAD_" + str(ThreadNumber)
        self.listDataUnCheck = ListDataUnCheck
        self.startIndex = IndexStart
        self.CSVPath = self.GetPathToNCBI() + '/NCBI_UPDATE_' + str(IndexStart + 1) + ".csv"

        # Create NCBI Log
        self.logFile = open(self.GetPathToNCBILogs() + "/NCBI_UPDATE_THREAD_" + str(ThreadNumber) + ".txt","w+")
    
    def SendRequestToNcbi(self, geneID):
        isCompleted = False
        count = 0

        while ( isCompleted == False):
            if ( count == 5 ):
                self.logFile.write("%s \r\n" % ("Status Gene " + str(geneID) + " : Request Fail") )
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
        if "discontinued" in str(resHeader.text):
            print('discontinued :', resHeader)
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

    def FetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                print('Except Metadata')
                time.sleep(0.1)
                pass
        return dataInMetaData

    def CheckDiscontinue(self, GeneID):
        response = self.SendRequestToNcbi(GeneID)
        if ( response == False ):
            self.logFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneID) + " : Error", "Description : Data retrieved fails") )
            return False, []
        else:
            try:
                resHeader = response.find('span', {"class": "geneid"})
                if "discontinued" in str(resHeader.text):
                    self.logFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneID) + " : Alert", "Description : Data discontinue update") )
                    resDiscontinue = response.find('ul', {"class": "gene-record-status"})
                    GeneID = (re.findall(r'(?<=\s)\d+', resDiscontinue.text))[0]

                    return self.CheckDiscontinue(GeneID)

                return str(GeneID), response
            except:
                self.logFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneID) + " : Error", "Description : Website Structure may change from origin") )
                return False, []

    def run(self):
        objectMapSnpWithNcbi = MetaData()
        objectThread = MetaData()
        
        dataMetaThread = self.FetchDataOnMetaData(objectThread, self.nameMetadata)

        startAt = dataMetaThread['count']
        if ( startAt == 0): startAt = 0
        else: startAt = startAt - 1

        for CurrentGeneID, UpdateAt in self.listDataUnCheck[ startAt : ]:

            OldGeneID = CurrentGeneID
            dataMetaThread['currentNumberOfGene'] = CurrentGeneID

            newGeneID, response = self.CheckDiscontinue(CurrentGeneID)
            if (int(newGeneID) != int(CurrentGeneID)):
                CurrentGeneID = newGeneID

            if response == False:
                self.logFile.write("%s \n%s \n\r" % ("Status Gene " + str(CurrentGeneID) + " : Error", "Description : Data retrieved fails") )
                continue
            else:
                updatedOn_Website = self.FetchUpdateOn(response)
                updatedOn_OldData = self.ConvertUpdateAtToTimeStamp(UpdateAt)

                if ( updatedOn_OldData != updatedOn_Website):
                    resSummaryDl = response.find('dl', {"id": "summaryDl"}) # fetch all detail of website
                    
                    officialSymbol = self.FetchOfficialSymbol(resSummaryDl)
                    
                    # Check Also Know As
                    if ( len( resSummaryDl.find_all(text = 'Also known as') ) >= 1 ):
                        alsoKnownAs = self.FetchAlsoKnowAs(resSummaryDl)
                    else:
                        alsoKnownAs = ['']
                    
                    data = GeneWithMap(CurrentGeneID = CurrentGeneID, OldGeneID = OldGeneID, GeneSymbol = officialSymbol, AlsoKnowAs = alsoKnownAs, UpdatedAt = updatedOn_Website)
                    dataFromWeb = pd.DataFrame(data.__dict__)
                    dataFromWeb.to_csv( self.CSVPath , mode='a', index = False, header=False)

            dataMetaThread = self.FetchDataOnMetaData(objectThread, self.nameMetadata)
            dataMetaThread['count'] = dataMetaThread['count'] + 1

            dataInMapSnpWithNcbi = self.FetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
            dataInMapSnpWithNcbi['technical']['updateMeta']['amountOfFinished'] = dataInMapSnpWithNcbi['technical']['updateMeta']['amountOfFinished'] + 1
            self.logFile.write("%s \n%s \n\r" % ("Status Gene " + str(CurrentGeneID) + " : successful", "Description : Data retrieved successfully") )

            if dataInMapSnpWithNcbi['technical']['updateMeta']['status'] != 1:
                return
            else:
                objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
                objectThread.SaveManualUpdateMetadata(dataMetaThread)
        
        return

class Ncbi(Database, MetaData, FilePath, GeneWithMap):
    numberOfRow = None
    numberOfThread = 1

    def __init__(self, _NumberOfThread):
        FilePath.__init__(self)
        self.numberOfThread = _NumberOfThread
        return

    def CreateCSVFile(self, FileName):
        ncbiPandas = pd.DataFrame( data=[], columns=[self.ncbiHeader] ) # set Initialize of csv file
        ncbiPandas.to_csv( FileName, index = False ) # create csv file for each multi thread
        return

    def CreateLogFile(self, FileName):
        open(FileName,"w+")
        return
    
    def CreateThreadMetadataFile(self, FileName):
        json_obj = {"currentNumberOfGene" : 0, "count": 0}

        #Write the object to file.
        with open(FileName,'w') as jsonFile:
            json.dump(json_obj, jsonFile)
        return

    def DeleteAllRelateFile(self, type):
        if (type == 'createMeta'):
            typeFile = 'CREATE'
        elif (type == 'updateMeta'):
            typeFile = 'UPDATE'

        csvFileName = 'NCBI_' + typeFile + '_'
        ThreadMetadataFileName = 'NCBI_' + typeFile + '_THREAD_'
        LogFileName = 'NCBI_' + typeFile + '_THREAD_'

        # Delete Thread CSV file
        for (root, dirs, file) in os.walk(self.GetPathToMetadata()):
            for fileName in file:
                if csvFileName in fileName:
                    os.remove(self.GetPathToMetadata() + "/" + fileName)

        # Delete Thread Metadata file
        for (root, dirs, file) in os.walk(self.GetPathToMetadata()):
            for fileName in file:
                if ThreadMetadataFileName in fileName:
                    os.remove(self.GetPathToMetadata() + "/" + fileName)
        
        # Delete Thread Log Folder
        # for (root, dirs, file) in os.walk(self.GetPathToNCBILogs()):
        #     for fileName in file:
        #         if LogFileName in fileName:
        #             os.remove(self.GetPathToNCBILogs() + "/" + fileName)
        
        return

    def SetZeroOnMetadata(self, type):
        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = objectMapSnpWithNcbi.ReadMetadata("MapSnpWithNcbi")

        if type == "createMeta":
            dataInMapSnpWithNcbi['technical']['createMeta']['amountUniqueGene'] == 0
            dataInMapSnpWithNcbi['technical']['createMeta']['amountOfFinished'] == 0
            dataInMapSnpWithNcbi['technical']['createMeta']['status'] == 0
        elif type == "updateMeta":
            dataInMapSnpWithNcbi['technical']['updateMeta']['amountUniqueGene'] == 0
            dataInMapSnpWithNcbi['technical']['updateMeta']['amountOfFinished'] == 0
            dataInMapSnpWithNcbi['technical']['updateMeta']['status'] == 0
            
        objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
        return

    def CombineCreateDataNcbi(self):
        database = Database()
        conn = database.ConnectDatabase()
        
        for filename in os.listdir(self.GetPathToNCBI()):
            if ( filename == ".DS_Store"):
                continue
            elif 'NCBI_CREATE_' in filename:
                data = pd.read_csv(self.GetPathToNCBI() + '/' + filename)
                
                for row_index, row in data.iterrows():

                    CurrentGeneID = row['CurrentGeneID']
                    OldGeneID = row['OldGeneID']
                    GeneSymbol = row['GeneSymbol']
                    UpdatedAt = row['UpdatedAt']

                    if row['CurrentGeneID'] != row['OldGeneID']:
                        print("Gene has discontinue", str(CurrentGeneID), "=>", str(OldGeneID))

                        sqlCommand = """
                            UPDATE gene_snp
                            SET GENE_ID = %s
                            WHERE GENE_ID = %s
                        """
                        database.CreateTask(conn, sqlCommand, (CurrentGeneID, OldGeneID))

                        sqlCommand = """
                            UPDATE gene_snp
                            SET GENE_SYMBOL = %s
                            WHERE GENE_ID = %s
                        """
                        database.CreateTask(conn, sqlCommand, (GeneSymbol, CurrentGeneID))

                    timestamp = datetime.fromtimestamp(UpdatedAt).strftime('%Y-%m-%d %H:%M:%S')
                    sqlCommand = """
                        REPLACE INTO ncbi ( GENE_ID, UPDATE_AT )
                        VALUES ( %s, %s ) 
                    """
                    database.CreateTask(conn, sqlCommand, (CurrentGeneID, timestamp))

                    if ( str(row['AlsoKnowAs']) != 'nan' ):
                        otherSymbol = row['AlsoKnowAs'].split('; ')
                        for eachSymbol in otherSymbol:
                            sqlCommand = """
                                REPLACE INTO other_symbol ( GENE_ID, OTHER_SYMBOL )
                                VALUES ( %s, %s )
                            """
                            self.CreateTask(conn, sqlCommand, (CurrentGeneID, eachSymbol) )
                    
                os.remove(self.GetPathToNCBI() + '/' + filename)
        
        database.CloseDatabase(conn)
        return

    def CombineUpdateDataNcbi(self):
        database = Database()
        conn = database.ConnectDatabase()
        
        for filename in os.listdir(self.GetPathToNCBI()):
            if ( filename == ".DS_Store"):
                continue
            elif 'NCBI_UPDATE_' in filename:
                data = pd.read_csv(self.GetPathToNCBI() + '/' + filename)

                for row_index, row in data.iterrows():

                    CurrentGeneID = row['CurrentGeneID']
                    OldGeneID = row['OldGeneID']
                    GeneSymbol = row['GeneSymbol']
                    UpdatedAt = row['UpdatedAt']

                    if row['CurrentGeneID'] != row['OldGeneID']:
                        print("Gene has discontinue", str(CurrentGeneID), "=>", str(OldGeneID))

                        sqlCommand = """
                            UPDATE gene_snp
                            SET GENE_ID = %s
                            WHERE GENE_ID = %s
                        """
                        database.CreateTask(conn, sqlCommand, (CurrentGeneID, OldGeneID))

                        sqlCommand = """
                            UPDATE gene_snp
                            SET GENE_SYMBOL = %s
                            WHERE GENE_ID = %s
                        """
                        database.CreateTask(conn, sqlCommand, (GeneSymbol, CurrentGeneID))

                    timestamp = datetime.fromtimestamp(UpdatedAt).strftime('%Y-%m-%d %H:%M:%S')
                    sqlCommand = """
                        UPDATE ncbi SET
                        UPDATE_AT = %s
                        WHERE GENE_ID = %s
                    """
                    database.CreateTask(conn, sqlCommand, (timestamp, CurrentGeneID))

                    if ( str(row['AlsoKnowAs']) != 'nan' ):
                        ListOtherSymbol = ( list(map(str, (row['AlsoKnowAs']).split('; '))) )
                        Records = [CurrentGeneID] + ListOtherSymbol
                        FormatStrings = ', '.join(['%s'] * len(str(row['AlsoKnowAs']).split('; ')))

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
                            database.CreateTask(conn, sqlCommand, (CurrentGeneID, OtherSymbol, ) )
                    
                os.remove(self.GetPathToNCBI() + '/' + filename)

        database.CloseDatabase(conn)
        return

    def CreateNcbiInformation(self):
        database = Database()
        objectMapSnpWithNcbi = MetaData()

        threadArray = []

        # Try to connect database
        try: 
            conn = database.ConnectDatabase()
            mysqlCommand = """
                SELECT DISTINCT GENE_ID FROM gene_snp;
            """
            listUniqueGeneID = database.CreateTask(conn, mysqlCommand, ())
            database.CloseDatabase(conn)
        except:
            self.SetZeroOnMetadata("createMeta")
            return

        lengthUniqueGeneID = len( listUniqueGeneID ) - 1
        dataInMapSnpWithNcbi = objectMapSnpWithNcbi.ReadMetadata("MapSnpWithNcbi")
        dataInMapSnpWithNcbi['technical']['createMeta']['amountUniqueGene'] = lengthUniqueGeneID
        lengthEachRound = lengthUniqueGeneID // self.numberOfThread

        # Number of Thread CPU
        for threadNumber in range(self.numberOfThread):

            IndexStart = lengthEachRound * threadNumber
            
            # Create Thread
            if ( threadNumber != ( self.numberOfThread - 1) ): 
                IndexStop = ( ( lengthEachRound * threadNumber ) + lengthEachRound ) - 1
                eachThread = CreateNcbi(ThreadNumber = threadNumber, ListGenesID = listUniqueGeneID, IndexStart = IndexStart, IndexStop = IndexStop)
            else:
                IndexStop = lengthUniqueGeneID
                eachThread = CreateNcbi(ThreadNumber = threadNumber, ListGenesID = listUniqueGeneID, IndexStart = IndexStart, IndexStop = IndexStop)

            # Create thread metadata, csv and log file
            if (dataInMapSnpWithNcbi['technical']['createMeta']['status'] == 1):
                nameThreadMetadata = 'NCBI_CREATE_THREAD_' + str(threadNumber) + '.json'
                nameCSVFile = 'NCBI_CREATE_' + str(IndexStart + 1) + "_" + str(IndexStop + 1) + ".csv"
                nameLogFile = 'NCBI_CREATE_THREAD_' + str(threadNumber) + ".txt"

                # Create Thread Metadata File
                self.CreateThreadMetadataFile(self.GetPathToMetadata() + '/' + nameThreadMetadata)
            
                # Create CSV File
                self.CreateCSVFile(FileName=self.GetPathToNCBI() + '/' + nameCSVFile)

                # Create Log File
                self.CreateLogFile(self.GetPathToNCBILogs() + "/" + nameLogFile)

            threadArray.append(eachThread)

        # Change Status Before Start Thread
        if (dataInMapSnpWithNcbi['technical']['createMeta']['status'] == 2 or dataInMapSnpWithNcbi['technical']['createMeta']['status'] == 3):
            dataInMapSnpWithNcbi['technical']['createMeta']['status'] = 1
            objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
        
        # Start Thread
        for eachThread in threadArray: 
            eachThread.start()

        # Waitting Thread finish  
        for eachThread in threadArray: 
            eachThread.join()

        dataInMetaData = objectMapSnpWithNcbi.ReadMetadata("MapSnpWithNcbi")

        if (dataInMetaData['technical']['createMeta']['status'] != 2):

            # Wait all mutithread has successfully process before start combine all data
            self.CombineCreateDataNcbi()

            # Clear Metadata
            self.SetZeroOnMetadata("createMeta")

            # Clear all related files
            self.DeleteAllRelateFile("createMeta")

        return

    def UpdateNcbiInformation(self):
        database = Database()
        objectMapSnpWithNcbi = MetaData()

        threadArray = []
        IndexStart = 0

        # Try to connect database
        try: 
            conn = database.ConnectDatabase()
            mysqlCommand = """
                SELECT * FROM ncbi;
            """
            ncbiData = database.CreateTask(conn, mysqlCommand, ())
            database.CloseDatabase(conn)
        except:
            self.SetZeroOnMetadata("updateMeta")
            return

        lengthNcbiData = len( ncbiData )

        dataInMapSnpWithNcbi = objectMapSnpWithNcbi.ReadMetadata("MapSnpWithNcbi")
        dataInMapSnpWithNcbi['technical']['updateMeta']['amountUniqueGene'] = lengthNcbiData
        lengthEachRound = lengthNcbiData // self.numberOfThread

        for threadNumber in range( self.numberOfThread ):

            # Create Thread
            if ( threadNumber != ( self.numberOfThread - 1) ):
                updateNcbi = UpdateNcbi(
                    threadNumber,
                    ListDataUnCheck = ncbiData[lengthEachRound * threadNumber : ( lengthEachRound * threadNumber ) + lengthEachRound],
                    IndexStart = IndexStart
                )
            else:
                updateNcbi = UpdateNcbi(
                    threadNumber,
                    ListDataUnCheck = ncbiData[lengthEachRound * threadNumber : lengthNcbiData],
                    IndexStart = IndexStart
                )

            if (dataInMapSnpWithNcbi['technical']['updateMeta']['status'] == 1):
                nameThreadMetadata = 'NCBI_UPDATE_THREAD_' + str(threadNumber) + '.json'
                nameCSVFile = 'NCBI_UPDATE_' + str(IndexStart + 1) + ".csv"
                nameLogFile = 'NCBI_UPDATE_THREAD_' + str(threadNumber) + ".txt"

                # Create Thread Metadata File
                self.CreateThreadMetadataFile(self.GetPathToMetadata() + '/' + nameThreadMetadata)
            
                # Create CSV File
                self.CreateCSVFile(FileName=self.GetPathToNCBI() + '/' + nameCSVFile)

                # Create Log File
                self.CreateLogFile(self.GetPathToNCBILogs() + "/" + nameLogFile)
                
            threadArray.append(updateNcbi)
            IndexStart = IndexStart + lengthEachRound

        # Change Status Before Start Thread
        if (dataInMapSnpWithNcbi['technical']['updateMeta']['status'] == 2 or dataInMapSnpWithNcbi['technical']['updateMeta']['status'] == 3):
            dataInMapSnpWithNcbi['technical']['updateMeta']['status'] = 1
            objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
               
        for eachThread in threadArray:
            eachThread.start()
            
        for eachThread in threadArray:
            eachThread.join()

        dataInMetaData = objectMapSnpWithNcbi.ReadMetadata("MapSnpWithNcbi")

        if (dataInMetaData['technical']['updateMeta']['status'] != 2):

            # Wait all mutithread has successfully process before start combine all data
            self.CombineUpdateDataNcbi()

            # Clear Metadata
            self.SetZeroOnMetadata("updateMeta")

            # Clear all related files
            self.DeleteAllRelateFile("updateMeta")

        return

if __name__ == "__main__":
    ncbi = Ncbi(1)
