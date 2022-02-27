from bs4 import BeautifulSoup as soup
import urllib.request
from urllib import parse, response
from Initialization import Database, MetaData, FilePath
import pandas as pd
import time
import os
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class HugeInfo():

    def __init__(self, searchName, urlLink, hugeID, step):
        self.searchName = searchName
        self.urlLink = urlLink
        self.hugeID = hugeID
        self.step = step
        return

    def InitializeChrome(self):
        filePath = FilePath()
        chrome_options = Options()
        ChromeDriverPath = (filePath.GetPathToChromeDriver()).replace("\\", "/")

        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
            # Where you want to store file
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": True
        })
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-software-rasterizer')

        driver = Chrome(ChromeDriverPath + '/chromedriver.exe',
                        options=chrome_options)
        return driver

    def SendRequestToWebsite(self):
        isCompleted = False
        count = 0
        while ( isCompleted == False):
            if ( count == 5 ):
                return False
            try:
                query_args = {
                    'query': 'Bipolar Disorder[original query]', 
                    'firstQuery': 'Bipolar Disorder',
                    'Mysubmit': 'filter',
                    'dbTypeChoice': 'All',
                    'gwas': '',
                    'sortTypeChoice': 'Gene',
                }
                encoded_args = parse.urlencode(query_args).encode('utf-8')
                urlNcbi = "https://phgkb.cdc.gov/PHGKB/startPagePubLit.action"
                UrlHuge = urllib.request.urlopen( urlNcbi, encoded_args )
                print('UrlHuge :', UrlHuge)
                res = soup(urllib.request.urlopen( urlNcbi, encoded_args ), 'html.parser')
                isCompleted = True
            except:
                count = count + 1
                pass
        
        return res
    
    def SeleniumProcess(self, diseaseID):
        listGene = []
        listGeneTest = []
        driver = self.InitializeChrome()

        driver.get(self.urlLink)

        if (self.step == "2"):
            sortTypeChoice = Select(driver.find_element(By.NAME, "sortTypeChoice"))
            sortTypeChoice.select_by_value("Disease")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='checkbox'][@name='selectedTermList'][@value='"+ str(self.hugeID) +"']")
                )
            )
            checkbox = driver.find_element(By.XPATH ,"//input[@type='checkbox'][@name='selectedTermList'][@value='"+ str(self.hugeID) +"']")
            checkbox.click()
            # driver.implicitly_wait(1)
            continueButton = driver.find_element(By.XPATH ,"//a[@onclick='document.searchSummary[1].submit();']")
            continueButton.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//b[contains(text(), 'Query Trace')]")
            )
        )

        sortTypeChoice = Select(driver.find_element(By.NAME, "sortTypeChoice"))
        sortTypeChoice.select_by_value("Gene")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//th[contains(text(), 'Gene')]")
            )
        )

        pageSource = soup(driver.page_source, 'html.parser')
        allGenes = pageSource.find_all('tbody')

        for eachGene in allGenes[len(allGenes) - 1].find_all('tr'):
            geneSymbol = " ".join(re.findall("[a-zA-Z0-9_@-]+", (eachGene.find_all('td'))[0].get_text() ))
            if (len(geneSymbol) != 0):
                listGeneTest.append(geneSymbol)
                listGene.append({
                    'DISEASE_ID': diseaseID,
                    'GENE_ID' : "Not found",
                    'GENE_SYMBOL' : geneSymbol,
                    'SOURCE_WEBSITE' : 'huge'
                })

        return listGene, listGeneTest

class KeggInfo():
    LinkData = None
    
    def __init__(self, linkData):
        self.LinkData = linkData
        return

    def SendRequestToWebsite(self):
        isCompleted = False
        count = 0
        while ( isCompleted == False):
            if ( count == 5 ):
                return False
            try:
                urlNcbi = self.LinkData
                res = soup(urllib.request.urlopen( urlNcbi ), 'html.parser')
                isCompleted = True
            except:
                count = count + 1
                pass
        
        return res
    
    def GetName(self, inputDOM):
        positionDiseaseNameHTML = inputDOM.find("th", string="Name")
        diseaseName = ( (positionDiseaseNameHTML.previous_element).find("td") ).next_element.next_element
        return diseaseName
    
    def GetAllGene(self, inputDOM):
        positionGeneHTML = inputDOM.find("th", string="Gene")
        try:
            allGeneNotSeparate = ( (positionGeneHTML.previous_element).find("td") ).next_element
            allGene = allGeneNotSeparate.get_text().split('\n')
            allGene.pop()
            return allGene
        except:
            return []
    
    def KeggDataset(self, diseaseID):
        listGene = []
        res = self.SendRequestToWebsite()
        
        if ( res == False ):
            return []
        else:
            allGene = self.GetAllGene(res)
            for eachGene in allGene[:]:
                separateWord = eachGene.split('[')
                geneSymbol = ( separateWord[0].split() )[0]
                ganeID = ( ( separateWord[1].split(':')[1] ).split() )[0].replace(']', '')

                listGene.append({
                    'DISEASE_ID' : diseaseID,
                    'GENE_ID' : int(ganeID),
                    'GENE_SYMBOL' : geneSymbol,
                    'SOURCE_WEBSITE' : 'kegg'
                })
        
            return listGene

class Disease(MetaData):
    listNcbiData = []
    pathDisease = ''
    
    def __init__(self):
        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            SELECT DISTINCT GENE_ID FROM gene_snp;
        """
        self.listNcbiData = database.CreateTask(conn, mysqlCommand, ())
        database.CloseDatabase(conn)
        return

    def CreateLogFile(self, FileName):
        textFile = open(FileName,"w+")
        textFile.close()
        return

    def WriteToLogFile(self, FileName, GeneSymbol, Status, Description):
        textFile = open(FileName,"a")
        if (GeneSymbol == None):
            textFile.write("%s \n%s \n\r" % ("Status : " + str(Status), "Description : " + str(Description)) )
        else:    
            textFile.write("%s \n%s \n\r" % ("Status Gene " + str(GeneSymbol) + " : " + str(Status), "Description : " + str(Description)) )
        textFile.close()
        return

    def CheckDiseaseID(self, abbreviation):
        database = Database()
        conn = database.ConnectDatabase()
        
        sqlCommand = '''
            SELECT DISEASE_ID FROM disease WHERE DISEASE_ABBREVIATION = %s
        '''
        
        result = database.CreateTask(conn, sqlCommand, (str(abbreviation), ))
        
        database.CloseDatabase(conn)
        
        try:
            return result[0][0]
        except:
            return 'Not found'

    def FetchGeneID(self, GeneSymbol):
        database = Database()
        conn = database.ConnectDatabase()
        sqlCommand = """
            SELECT gene_snp.GENE_ID
            FROM gene_snp
            WHERE gene_snp.GENE_SYMBOL = %s LIMIT 1;
        """
        
        result = database.CreateTask(conn, sqlCommand, (GeneSymbol, ))
        if ( result == [] ):
            sqlCommand = """
                SELECT other_symbol.GENE_ID
                FROM other_symbol
                WHERE other_symbol.OTHER_SYMBOL = %s LIMIT 1;
            """
            result = database.CreateTask(conn, sqlCommand, (GeneSymbol, ))

        database.CloseDatabase(conn)
        try:
            return result[0][0]
        except:
            return 'Not found'

    def SetZeroOnMetadata(self, type):
        objectDisease = MetaData()
        diseaseInfo = objectDisease.ReadMetadata('Disease')

        if ( diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] != 2 ):
            index = 0
            if type == "createMeta":
                for eachInfo in diseaseInfo['technical']['diseases']:
                    ( (diseaseInfo['technical']['diseases'] )[index] )['createMeta']['amountDisease'] = 0
                    ( (diseaseInfo['technical']['diseases'] )[index] )['createMeta']['amountOfFinished'] = 0
                    index = index + 1

                if ( diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] == 1 or diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] == 3 ):
                    diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] = 0

            elif type == "updateMeta":
                diseaseInfo = objectDisease.ReadMetadata('Disease')
                for eachInfo in diseaseInfo['technical']['diseases']:
                    ( (diseaseInfo['technical']['diseases'] )[index] )['updateMeta']['amountDisease'] = 0
                    ( (diseaseInfo['technical']['diseases'] )[index] )['updateMeta']['amountOfFinished'] = 0

                    index = index + 1

                if ( diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] == 1 or diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] == 3 ):
                    diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] = 0

        objectDisease.SaveManualUpdateMetadata(diseaseInfo)

    def CheckGeneWithMap(self, nameLogFile, diseaseList, keggList ):
        
        listGeneDisease = []
        UniqueList = [] # uses for check unique geneID
        ExcludeList = [eachGene['GENE_SYMBOL'] for eachGene in keggList] # List of gene, Don't have to find gene id
        
        for diseaseGene in diseaseList[:10]:
            Sources = ""
            GeneSymbol = diseaseGene['GENE_SYMBOL'].strip()
            SourceWebsite = diseaseGene['SOURCE_WEBSITE']
            diseaseID = diseaseGene['DISEASE_ID']

            IsFoundUniqueList = GeneSymbol in UniqueList
            IsFoundExcludeList = GeneSymbol in ExcludeList

            if IsFoundUniqueList:                
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 1", "")
                print( 'condition 1 |', GeneSymbol, SourceWebsite)
                continue

            # Condition for What Gene not have gene id on website and must have to find gene id on database ( Huge )
            elif not(IsFoundUniqueList) and not(IsFoundExcludeList):
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 2", "Condition for What Gene not have gene id on website and must have to find gene id on database ( Huge )")
                print( 'condition 2 |', GeneSymbol, SourceWebsite)
                
                GeneID = self.FetchGeneID(GeneSymbol)
                
                listGeneDisease.append({
                    'GENE_ID' : GeneID,
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : SourceWebsite
                })
                
                UniqueList.append(GeneSymbol)

            # Condition for what gene have gene id on website and don't have to find gene id on database ( Kegg )
            elif not(IsFoundUniqueList) and IsFoundExcludeList:
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 2", "Condition for what gene have gene id on website and don't have to find gene id on database ( Kegg )")
                print( 'condition 3 |', GeneSymbol, SourceWebsite)
                
                Matches = (detailDisease for detailDisease in (diseaseList) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                for Match in Matches: Sources = Sources + Match['SOURCE_WEBSITE'] + "; "
                Sources = Sources[:-2]
                
                listGeneDisease.append({
                    'GENE_ID' : diseaseGene['GENE_ID'],
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : Sources
                })
                
                UniqueList.append(GeneSymbol)
            
        print('\n')
        
        return listGeneDisease

    def CreateDiseaseDataset(self):
        objectDisease = MetaData()
        objectMapDisease = MetaData()

        listDisease = objectMapDisease.ReadMetadata('Disease')

        for eachInfo in listDisease['technical']['diseases']:
            listGene = []

            # Kegg variable
            linkKegg = eachInfo['kege']

            # Huge variable
            linkHuge = eachInfo['huge']['link']
            searchHuge = eachInfo['huge']['nameTextBox']
            IDHuge = eachInfo['huge']['idCheckBox']
            StepHuge = eachInfo['huge']['step']

            try: diseaseID = self.CheckDiseaseID(eachInfo['abbreviation'])
            except: continue

            if (diseaseID != 1):
                continue

            diseaseInfo = objectDisease.ReadMetadata('Disease')

            nameLogFile = 'DISEASE_CREATE_DISEASE_ID_' + str(diseaseID) + ".txt"

            # If the status is 0, the process has stopped
            if ( diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] == 0):
                continue

            # If the status is 1, the process has just started
            elif ( diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] == 1):
                self.CreateLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile) # Create Log File

            # If the status is 2, the process has paused
            elif ( diseaseInfo['technical']['diseaseStatus']['createMeta']['status'] == 2):
                return

            # Fetch data from kegg website
            try:
                keggInfo = KeggInfo(linkKegg)
                listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Successful", "Already been fetched a kegg information")
            except Exception as e:
                keggInfo = []
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", str(e))

            # Fetch data from huge website
            try:
                hugeInfo = HugeInfo(searchHuge, linkHuge, IDHuge, StepHuge)
                listGeneFromHuge, listTestGeneFromHuge = hugeInfo.SeleniumProcess(diseaseID)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "successful", "Already been fetched a huge information")
            except Exception as e:
                hugeInfo = []
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", str(e))
            
            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge

            listGene = self.CheckGeneWithMap(self.GetPathToDiseaseLogs() + "/" + nameLogFile, listGeneEachDisease, listGeneFromKegg)

            ( (diseaseInfo['technical']['diseases'] )[diseaseID - 1] )['createMeta']['amountDisease'] = len(listGene)
            objectDisease.SaveManualUpdateMetadata(diseaseInfo)

            # Connect database
            try:
                database = Database()
                conn = database.ConnectDatabase()
            except Exception as e:
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", str(e))
                continue

            for row in listGene:
                diseaseInfo = objectDisease.ReadMetadata('Disease')
                
                geneID = str(row['GENE_ID'])
                geneSymbol = str(row['GENE_SYMBOL'])
                sources = row['SOURCE_WEBSITE'].split('; ')

                # Update new a related gene
                try:
                    if ( str(row['GENE_ID']) == 'Not found' ):
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease ( GENE_SYMBOL, DISEASE_ID ) 
                            VALUES ( %s, %s ) 
                        """

                        database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID))

                    else:                    
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease ( GENE_SYMBOL, DISEASE_ID, GENE_ID ) 
                            VALUES ( %s, %s, %s )
                        """

                        database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID, geneID))
                except Exception as e:
                    self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Error", str(e))
                    continue
                
                # Update a new website source each gene
                try:
                    for source in sources:                
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease_source ( GENE_SYMBOL, SOURCE_WEBSITE ) 
                            VALUES ( %s, %s ) 
                        """
                        
                        database.CreateTask(conn, sqlCommand, (geneSymbol, source))
                except Exception as e:
                    self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Error", str(e))
                    continue

                ( (diseaseInfo['technical']['diseases'] )[diseaseID - 1] )['createMeta']['amountOfFinished'] = ( (diseaseInfo['technical']['diseases'] )[diseaseID - 1] )['createMeta']['amountOfFinished'] + 1
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Successful", "Already updated new a related gene")
            
            database.CloseDatabase(conn) 

        self.SetZeroOnMetadata('updateMeta')

        return

    def UpdateDiseaseDataset(self):
        objectDisease = MetaData()
        objectMapDisease = MetaData()

        listDisease = objectMapDisease.ReadMetadata('Disease')
        
        for eachInfo in listDisease['technical']['diseases']:
            listGene = []

            # Kegg variable
            linkKegg = eachInfo['kege']

            # Huge variable
            linkHuge = eachInfo['huge']['link']
            searchHuge = eachInfo['huge']['nameTextBox']
            IDHuge = eachInfo['huge']['idCheckBox']
            StepHuge = eachInfo['huge']['step']

            try: diseaseID = self.CheckDiseaseID(eachInfo['abbreviation'])
            except: continue

            if (diseaseID != 1):
                continue

            diseaseInfo = objectDisease.ReadMetadata('Disease')

            nameLogFile = 'DISEASE_UPDATE_DISEASE_ID_' + str(diseaseID) + ".txt"

            # If the status is 0, the process has stopped
            if ( diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] == 0):
                continue

            # If the status is 1, the process has just started
            elif ( diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] == 1):
                self.CreateLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile) # Create Log File

            # If the status is 2, the process has paused
            elif ( diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] == 2):
                return

            # Fetch data from kegg website
            try:
                keggInfo = KeggInfo(linkKegg)
                listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Successful", "Already been fetched a kegg information")
            except Exception as e:
                keggInfo = []
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", str(e))

            # Fetch data from huge website
            try:
                hugeInfo = HugeInfo(searchHuge, linkHuge, IDHuge, StepHuge)
                listGeneFromHuge, listTestGeneFromHuge = hugeInfo.SeleniumProcess(diseaseID)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "successful", "Already been fetched a huge information")
            except Exception as e:
                hugeInfo = []
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", str(e))

            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge

            listGene = self.CheckGeneWithMap(self.GetPathToDiseaseLogs() + "/" + nameLogFile, listGeneEachDisease, listGeneFromKegg)
            ( (diseaseInfo['technical']['diseases'] )[int(diseaseID) - 1] )['updateMeta']['amountDisease'] = len(listGene)
            objectDisease.SaveManualUpdateMetadata(diseaseInfo)

            # Connect database
            try:
                database = Database()
                conn = database.ConnectDatabase()
            except:
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", "Database lost connected")
                continue

            # Delete all Gene not related with disease
            try:
                listGeneSymbolOnDisease = [eachGene['GENE_SYMBOL'] for eachGene in listGene]
                FormatStrings = ', '.join(['%s'] * len(listGeneSymbolOnDisease))
                sqlCommand = '''
                    DELETE FROM gene_disease
                    WHERE gene_disease.DISEASE_ID = %%s
                    AND gene_disease.GENE_SYMBOL NOT IN (%s)
                ''' % FormatStrings   
                Records = [diseaseID] + listGeneSymbolOnDisease            
                database.CreateTask(conn, sqlCommand, Records)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Successful", "Delete all Gene not related with disease ID : " + str(diseaseID))
            except:
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, None, "Error", "Something is wrong with the database")
                continue

            for row in listGene:
                diseaseInfo = objectDisease.ReadMetadata('Disease')

                geneID = str(row['GENE_ID'])
                geneSymbol = str(row['GENE_SYMBOL']) 
                sources = row['SOURCE_WEBSITE'].split('; ')

                # Update new a related gene
                try:
                    if ( str(row['GENE_ID']) == 'Not found' ):
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease ( GENE_SYMBOL, DISEASE_ID ) 
                            VALUES ( %s, %s ) 
                        """

                        database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID))
                    else:          
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease ( GENE_SYMBOL, DISEASE_ID, GENE_ID ) 
                            VALUES ( %s, %s, %s )
                        """

                        database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID, geneID))
                except Exception as e:
                    self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Error", str(e))
                    continue

                # Update a new website source each gene
                try:
                    for source in sources:                
                        sqlCommand = """
                            INSERT IGNORE INTO gene_disease_source ( GENE_SYMBOL, SOURCE_WEBSITE ) 
                            VALUES ( %s, %s ) 
                        """
                        
                        database.CreateTask(conn, sqlCommand, (geneSymbol, source))
                except Exception as e:
                    self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Error", str(e))
                    continue
                
                ( (diseaseInfo['technical']['diseases'] )[diseaseID - 1] )['updateMeta']['amountOfFinished'] = ( (diseaseInfo['technical']['diseases'] )[diseaseID - 1] )['updateMeta']['amountOfFinished'] + 1
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.WriteToLogFile(self.GetPathToDiseaseLogs() + "/" + nameLogFile, geneSymbol, "Successful", "Already updated new a related gene")

            database.CloseDatabase(conn)
        
        self.SetZeroOnMetadata('updateMeta')

        return

if __name__ == "__main__":
    disease = Disease()
    # disease.CreateDiseaseDataset()
    # disease.UpdateDiseaseDataset()