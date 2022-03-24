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
    searchName = ""
    urlLink = ""
    hugeID = 0
    step = 0

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

        driver = Chrome(ChromeDriverPath + '/chromedriver.exe', options=chrome_options)

        return driver
    
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
    urlLink = None
    
    def __init__(self, linkData):
        self.urlLink = linkData
        return

    def SendRequestToWebsite(self):
        isCompleted = False
        count = 0
        while ( isCompleted == False):
            if ( count == 5 ):
                return False
            try:
                urlNcbi = self.urlLink
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
    
    def __init__(self):
        return

    def CreateLogFile(self, filename):
        textFile = open(filename,"w+")
        textFile.close()
        return

    def WriteToLogFile(self, filename, geneSymbol, status, description):
        textFile = open(filename,"a")
        if (geneSymbol == None):
            textFile.write("%s \n%s \n\r" % ("Status : " + str(status), "Description : " + str(description)) )
        else:    
            textFile.write("%s \n%s \n\r" % ("Status Gene " + str(geneSymbol) + " : " + str(status), "Description : " + str(description)) )
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

    def FetchGeneID(self, geneSymbol):
        database = Database()
        conn = database.ConnectDatabase()
        sqlCommand = """
            SELECT gene_snp.GENE_ID
            FROM gene_snp
            WHERE gene_snp.GENE_SYMBOL = %s LIMIT 1;
        """
        
        result = database.CreateTask(conn, sqlCommand, (geneSymbol, ))
        if ( result == [] ):
            sqlCommand = """
                SELECT other_symbol.GENE_ID
                FROM other_symbol
                WHERE other_symbol.OTHER_SYMBOL = %s LIMIT 1;
            """
            result = database.CreateTask(conn, sqlCommand, (geneSymbol, ))

        database.CloseDatabase(conn)
        try:
            return result[0][0]
        except:
            return 'Not found'

    def SetZeroOnMetadata(self, typeMetadata):
        objectDisease = MetaData()
        diseaseInfo = objectDisease.ReadMetadata('Disease')

        if ( diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] != 2  ):
            index = 0

            for eachInfo in diseaseInfo['technical']['diseases']:
                ( (diseaseInfo['technical']['diseases'] )[index] )[typeMetadata]['amountDisease'] = 0
                ( (diseaseInfo['technical']['diseases'] )[index] )[typeMetadata]['amountOfFinished'] = 0
                index = index + 1

            if ( diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] == 1 or diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] == 3 ):
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] = 0
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseID'] = 0
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = ""

            objectDisease.SaveManualUpdateMetadata(diseaseInfo)

    def CheckGeneWithMap(self, typeMetadata, indexDisease, nameLogFile, diseaseList, keggList ):
        objectDisease = MetaData()
        listGeneDisease = []
        UniqueList = [] # uses for check unique geneID
        ExcludeList = [eachGene['GENE_SYMBOL'] for eachGene in keggList] # List of gene, Don't have to find gene id

        diseaseInfo = objectDisease.ReadMetadata('Disease')
        diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

        if ( diseaseStatus == 0 or diseaseStatus == 2):
            return
        else:
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] = 0
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountDisease'] = len(diseaseList)
            diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = "Checking " + diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName']
            objectDisease.SaveManualUpdateMetadata(diseaseInfo)
        
        for diseaseGene in diseaseList[:]:
            Sources = ""
            GeneSymbol = diseaseGene['GENE_SYMBOL'].strip()
            SourceWebsite = diseaseGene['SOURCE_WEBSITE']
            diseaseID = diseaseGene['DISEASE_ID']

            IsFoundUniqueList = GeneSymbol in UniqueList
            IsFoundExcludeList = GeneSymbol in ExcludeList

            if IsFoundUniqueList:                
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 1", "")

            # Condition for What Gene not have gene id on website and must have to find gene id on database ( Huge )
            elif not(IsFoundUniqueList) and not(IsFoundExcludeList):
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 2", "Condition for What Gene not have gene id on website and must have to find gene id on database ( Huge )")
                
                GeneID = self.FetchGeneID(GeneSymbol)
                
                listGeneDisease.append({
                    'GENE_ID' : GeneID,
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : SourceWebsite
                })
                
                UniqueList.append(GeneSymbol)

            # Condition for what gene have gene id on website and don't have to find gene id on database ( Kegg )
            elif not(IsFoundUniqueList) and IsFoundExcludeList:
                self.WriteToLogFile(nameLogFile, GeneSymbol, "condition 3", "Condition for what gene have gene id on website and don't have to find gene id on database ( Kegg )")
                
                Matches = (detailDisease for detailDisease in (diseaseList) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                for Match in Matches: Sources = Sources + Match['SOURCE_WEBSITE'] + "; "
                Sources = Sources[:-2]
                
                listGeneDisease.append({
                    'GENE_ID' : diseaseGene['GENE_ID'],
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : Sources
                })
                
                UniqueList.append(GeneSymbol)

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            # If the status is 0, the process has stopped and If the status is 2, the process has paused
            if ( diseaseStatus == 0 or diseaseStatus == 2): return
            else:
                ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] = ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] + 1
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
        
        return listGeneDisease

    def CreateDiseaseDataset(self):
        objectDisease = MetaData()
        objectMapDisease = MetaData()

        typeMetadata = "createMeta"

        listDisease = objectMapDisease.ReadMetadata('Disease')

        for eachInfo in listDisease['technical']['diseases']:

            try: diseaseID = self.CheckDiseaseID(eachInfo['abbreviation'])
            except: continue

            listGene = []
            isKeggCompleted = False
            isHugeCompleted = False

            indexDisease = int(diseaseID) - 1
            nameLogFile = 'DISEASE_CREATE_DISEASE_ID_' + str(diseaseID) + ".txt"
            pathToLogFile = self.GetPathToDiseaseLogs() + "/" + nameLogFile

            # Kegg variable
            linkKegg = eachInfo['kege']

            # Huge variable
            linkHuge = eachInfo['huge']['link']
            searchHuge = eachInfo['huge']['nameTextBox']
            IDHuge = eachInfo['huge']['idCheckBox']
            StepHuge = eachInfo['huge']['step']            

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            if ( diseaseStatus == 0):
                self.SetZeroOnMetadata(typeMetadata)
                return
            elif ( diseaseStatus == 1):
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseID'] = diseaseID
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = "Searching " + eachInfo['name']
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.CreateLogFile(pathToLogFile)
            elif ( diseaseStatus == 2): return

            # Fetch data from kegg website
            try:
                keggInfo = KeggInfo(linkKegg)
                listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
                self.WriteToLogFile(pathToLogFile, None, "Successful", "Already been fetched a kegg information")
                isKeggCompleted = True
            except Exception as e:
                keggInfo = []
                listGeneFromKegg = []
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))

            # Fetch data from huge website
            try:
                hugeInfo = HugeInfo(searchHuge, linkHuge, IDHuge, StepHuge)
                listGeneFromHuge, listTestGeneFromHuge = hugeInfo.SeleniumProcess(diseaseID)
                self.WriteToLogFile(pathToLogFile, None, "successful", "Already been fetched a huge information")
                isHugeCompleted = True
            except Exception as e:
                hugeInfo = []
                listGeneFromHuge = []
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            if (diseaseStatus == 0):
                self.SetZeroOnMetadata(typeMetadata)
                return
            elif (diseaseStatus == 2): return

            # If both kegg and huge are not response
            if ( ( isKeggCompleted == False) and (isHugeCompleted == False) ):
                self.WriteToLogFile(pathToLogFile, None, "Error", "Both kegg and huge navigator website are not response")
                continue
            
            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge

            listGene = self.CheckGeneWithMap(typeMetadata, indexDisease, pathToLogFile, listGeneEachDisease, listGeneFromKegg)

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            if ( diseaseStatus == 0):
                self.SetZeroOnMetadata(typeMetadata)
                return
            elif ( diseaseStatus == 2): return
            elif ( diseaseStatus == 3): diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] = 1

            diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = "Storing " + eachInfo['name']
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountDisease'] = len(listGene)
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] = 0
            objectDisease.SaveManualUpdateMetadata(diseaseInfo)

            # Connect database
            try:
                database = Database()
                conn = database.ConnectDatabase()
            except Exception as e:
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))
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
                    self.WriteToLogFile(pathToLogFile, geneSymbol, "Error", str(e))
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
                    self.WriteToLogFile(pathToLogFile, geneSymbol, "Error", str(e))
                    continue

                ( (diseaseInfo['technical']['diseases'] )[indexDisease] )['createMeta']['amountOfFinished'] = ( (diseaseInfo['technical']['diseases'] )[indexDisease] )['createMeta']['amountOfFinished'] + 1
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.WriteToLogFile(pathToLogFile, geneSymbol, "Successful", "Already updated new a related gene")
            
            database.CloseDatabase(conn) 

        self.SetZeroOnMetadata('createMeta')

        return

    def UpdateDiseaseDataset(self):
        objectDisease = MetaData()
        objectMapDisease = MetaData()

        typeMetadata = "updateMeta"

        listDisease = objectMapDisease.ReadMetadata('Disease')
        
        for eachInfo in listDisease['technical']['diseases']:
            
            try: diseaseID = self.CheckDiseaseID(eachInfo['abbreviation'])
            except: continue

            listGene = []
            isKeggCompleted = False
            isHugeCompleted = False

            indexDisease = int(diseaseID) - 1
            nameLogFile = 'DISEASE_UPDATE_DISEASE_ID_' + str(diseaseID) + ".txt"
            pathToLogFile = self.GetPathToDiseaseLogs() + "/" + nameLogFile

            # Kegg variable
            linkKegg = eachInfo['kege']

            # Huge variable
            linkHuge = eachInfo['huge']['link']
            searchHuge = eachInfo['huge']['nameTextBox']
            IDHuge = eachInfo['huge']['idCheckBox']
            StepHuge = eachInfo['huge']['step']

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            if (diseaseStatus == 0): 
                self.SetZeroOnMetadata(typeMetadata)
                continue
            elif ( diseaseStatus == 1):
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseID'] = diseaseID
                diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = "Searching " + eachInfo['name']
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.CreateLogFile(pathToLogFile)
            elif ( diseaseStatus == 2): return

            # Fetch data from kegg website
            try:
                keggInfo = KeggInfo(linkKegg)
                listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
                self.WriteToLogFile(pathToLogFile, None, "Successful", "Already been fetched a kegg information")
                isKeggCompleted = True
            except Exception as e:
                keggInfo = []
                listGeneFromKegg = []
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))

            # Fetch data from huge website
            try:
                hugeInfo = HugeInfo(searchHuge, linkHuge, IDHuge, StepHuge)
                listGeneFromHuge, listTestGeneFromHuge = hugeInfo.SeleniumProcess(diseaseID)
                self.WriteToLogFile(pathToLogFile, None, "successful", "Already been fetched a huge information")
                isHugeCompleted = True
            except Exception as e:
                hugeInfo = []
                listGeneFromHuge = []
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])

            if ( diseaseStatus == 0): continue
            elif ( diseaseStatus == 2): return

            # If both kegg and huge are not response
            if ( ( isKeggCompleted == False) and (isHugeCompleted == False) ):
                self.WriteToLogFile(pathToLogFile, None, "Error", "Both kegg and huge navigator website are not response")
                continue

            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge

            listGene = self.CheckGeneWithMap(typeMetadata, indexDisease, pathToLogFile, listGeneEachDisease, listGeneFromKegg)

            diseaseInfo = objectDisease.ReadMetadata('Disease')
            diseaseStatus = int(diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'])
            
            if ( diseaseStatus == 0): continue
            elif ( diseaseStatus == 2): return
            elif ( diseaseStatus == 3): diseaseInfo['technical']['diseaseStatus'][typeMetadata]['status'] = 1

            diseaseInfo['technical']['diseaseStatus'][typeMetadata]['diseaseName'] = "Storing " + eachInfo['name']
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountDisease'] = len(listGene)
            ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] = 0
            objectDisease.SaveManualUpdateMetadata(diseaseInfo)

            # Connect database
            try:
                database = Database()
                conn = database.ConnectDatabase()
            except Exception as e:
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))
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
                self.WriteToLogFile(pathToLogFile, None, "Successful", "Delete all Gene not related with disease ID : " + str(diseaseID))
            except Exception as e:
                self.WriteToLogFile(pathToLogFile, None, "Error", str(e))
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
                    self.WriteToLogFile(pathToLogFile, geneSymbol, "Error", str(e))
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
                    self.WriteToLogFile(pathToLogFile, geneSymbol, "Error", str(e))
                    continue
                
                ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] = ( (diseaseInfo['technical']['diseases'] )[indexDisease] )[typeMetadata]['amountOfFinished'] + 1
                objectDisease.SaveManualUpdateMetadata(diseaseInfo)
                self.WriteToLogFile(pathToLogFile, geneSymbol, "Successful", "Already updated new a related gene")

            database.CloseDatabase(conn)
        
        self.SetZeroOnMetadata(typeMetadata)

        return

if __name__ == "__main__":
    disease = Disease()
    # disease.CreateDiseaseDataset()
    # disease.UpdateDiseaseDataset()