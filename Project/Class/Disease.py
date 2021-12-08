from bs4 import BeautifulSoup as soup
import urllib.request
from Initialization import Database, MetaData
import pandas as pd
import time

class HugeInfo():
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
    
    def HugeDataset(self, diseaseID):
        listGene = []
        res = self.SendRequestToWebsite()
        
        if ( res == False ):
            return []
        else:
            findinres = res.find_all('table', {'style':'table_inside'})
            a = findinres[0].find_all('td', {'align':'left'})
            
            for i in a[:]:
                geneSymbol = ( i.get_text()[4:].split('\r\n   \t\t\t\t\t\t\n') )[0]

                listGene.append({
                    'DISEASE_ID': diseaseID,
                    'GENE_ID' : "Not found",
                    'GENE_SYMBOL' : geneSymbol,
                    'SOURCE_WEBSITE' : 'huge'
                })

            return listGene

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
            SELECT DISTINCT GENE_ID FROM snp_an_as;
        """
        self.listNcbiData = database.CreateTask(conn, mysqlCommand, ())
        database.CloseDatabase(conn)
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

    def CreateDiseaseDataset(self):
        metaData = MetaData()
        diseaseInfo = metaData.ReadMetadata('Disease')

        for eachDisease in diseaseInfo['technical']['diseases']:
            diseaseID = self.CheckDiseaseID(eachDisease['Abbreviation'])
            
            keggInfo = KeggInfo(eachDisease['kege'])
            hugeDataset = HugeInfo(eachDisease['huge'])

            listGeneKegg = keggInfo.KeggDataset(diseaseID)
            listGeneHuge = hugeDataset.HugeDataset(diseaseID)

            listGeneEachDisease = listGeneKegg + listGeneHuge
            
        return

if __name__ == "__main__":
    disease = Disease()
    disease.CreateDiseaseDataset()