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

    def FetchGeneID(self, GeneSymbol):
        database = Database()
        conn = database.ConnectDatabase()
        sqlCommand = """
            SELECT snp_an_as.GENE_ID
            FROM snp_an_as
            WHERE snp_an_as.GENE_SYMBOL = %s LIMIT 1;
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

    def CheckGeneWithMap(self, diseaseList, keggList ):
        
        listGeneDisease = []
        UniqueList = [] # uses for check unique geneID
        ExcludeList = [eachGene['GENE_SYMBOL'] for eachGene in keggList] # List of gene, Don't have to find gene id
        
        for diseaseGene in diseaseList[:]:
            Sources = ""
            GeneSymbol = diseaseGene['GENE_SYMBOL'].strip()
            SourceWebsite = diseaseGene['SOURCE_WEBSITE']
            diseaseID = diseaseGene['DISEASE_ID']

            IsFoundUniqueList = GeneSymbol in UniqueList
            IsFoundExcludeList = GeneSymbol in ExcludeList
            if IsFoundUniqueList:                
                print( 'condition 1 |', GeneSymbol, SourceWebsite)
                continue

            # Condition for What Gene not have gene id on website and must have to find gene id on database ( Huge )
            elif not(IsFoundUniqueList) and not(IsFoundExcludeList):
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
        metaData = MetaData()
        diseaseInfo = metaData.ReadMetadata('Disease')

        for eachDisease in diseaseInfo['technical']['diseases']:                       
            diseaseID = self.CheckDiseaseID(eachDisease['Abbreviation'])
            
            print('Disease ID :', diseaseID)
            
            keggInfo = KeggInfo(eachDisease['kege'])
            hugeDataset = HugeInfo(eachDisease['huge'])

            listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
            listGeneFromHuge = hugeDataset.HugeDataset(diseaseID)

            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge
            listGene = self.CheckGeneWithMap(listGeneEachDisease, listGeneFromKegg)

            database = Database()
            conn = database.ConnectDatabase()

            for row in listGene:
                geneID = str(row['GENE_ID'])
                geneSymbol = str(row['GENE_SYMBOL']) 
                sources = row['SOURCE_WEBSITE'].split('; ')

                if ( str(row['GENE_ID']) == 'Not found' ):
                    sqlCommand = """
                        INSERT IGNORE INTO disease_as ( GENE_SYMBOL, DISEASE_ID ) 
                        VALUES ( %s, %s ) 
                    """

                    database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID))

                else:                    
                    sqlCommand = """
                        INSERT IGNORE INTO disease_as ( GENE_SYMBOL, DISEASE_ID, GENE_ID ) 
                        VALUES ( %s, %s, %s )
                    """

                    database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID, geneID))
                
                for source in sources:                
                    sqlCommand = """
                        INSERT IGNORE INTO as_source ( GENE_SYMBOL, SOURCE_WEBSITE ) 
                        VALUES ( %s, %s ) 
                    """
                    
                    database.CreateTask(conn, sqlCommand, (geneSymbol, source))
            
            database.CloseDatabase(conn)

            if ( str(diseaseID) == "2" ):
                return
        return

    def UpdateDiseaseDataset(self):
        metaData = MetaData()
        diseaseInfo = metaData.ReadMetadata('Disease')
        
        for eachDisease in diseaseInfo['technical']['diseases']:
            diseaseID = self.CheckDiseaseID(eachDisease['Abbreviation'])

            keggInfo = KeggInfo(eachDisease['kege'])
            hugeDataset = HugeInfo(eachDisease['huge'])

            listGeneFromKegg = keggInfo.KeggDataset(diseaseID)
            listGeneFromHuge = hugeDataset.HugeDataset(diseaseID)

            listGeneEachDisease = listGeneFromKegg + listGeneFromHuge

            listGene = self.CheckGeneWithMap(listGeneEachDisease, listGeneFromKegg)
            listGeneSymbolOnDisease = [eachGene['GENE_SYMBOL'] for eachGene in listGene]

            database = Database()
            conn = database.ConnectDatabase()

            FormatStrings = ', '.join(['%s'] * len(listGeneSymbolOnDisease))

            sqlCommand = '''
                DELETE FROM disease_as
                WHERE disease_as.DISEASE_ID = %%s
                AND disease_as.GENE_SYMBOL NOT IN (%s)
            ''' % FormatStrings   

            Records = [diseaseID] + listGeneSymbolOnDisease            

            database.CreateTask(conn, sqlCommand, Records)

            for row in listGene:
                geneID = str(row['GENE_ID'])
                geneSymbol = str(row['GENE_SYMBOL']) 
                sources = row['SOURCE_WEBSITE'].split('; ')

                if ( str(row['GENE_ID']) == 'Not found' ):
                    sqlCommand = """
                        INSERT IGNORE INTO disease_as ( GENE_SYMBOL, DISEASE_ID ) 
                        VALUES ( %s, %s ) 
                    """

                    database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID))

                else:                    
                    sqlCommand = """
                        INSERT IGNORE INTO disease_as ( GENE_SYMBOL, DISEASE_ID, GENE_ID ) 
                        VALUES ( %s, %s, %s )
                    """

                    database.CreateTask(conn, sqlCommand, (geneSymbol, diseaseID, geneID))

                for source in sources:                
                    sqlCommand = """
                        INSERT IGNORE INTO as_source ( GENE_SYMBOL, SOURCE_WEBSITE ) 
                        VALUES ( %s, %s ) 
                    """
                    
                    database.CreateTask(conn, sqlCommand, (geneSymbol, source))

            database.CloseDatabase(conn)

            if ( str(diseaseID) == "1" ):
                return
        return

if __name__ == "__main__":
    disease = Disease()
    disease.UpdateDiseaseDataset()

    # testList = ['HLA-DRB1', 'HLA-DQB1', 'HLA-DQA1', 'INS', 'CTLA-4', 'PTPN22', 'IL-2RA', 'PTPN2', 'ERBB3', 'IL2', 'IFIH1', 'CLEC16A', 'BACH2', 'PRKCQ', 'CTSH', 'C1QTNF6', 'SH2B3', 'C12orf30', 'CD226', 'ITPR3', 'CYP27B1', 'ACE']
    # testString = 'HLA-DQB1'
    # print( testString in testList )