from bs4 import BeautifulSoup as soup
import urllib.request
from Class_Initialization import GetDataFromFile, Database, MetaData, Initialize
import pandas as pd
import time

"""
Class detail
"""
class HugeInfo(GetDataFromFile, Initialize):
    LinkData = None
    
    def __init__(self, linkData):
        GetDataFromFile.__init__(self)
        self.LinkData = linkData
        return
    
    def FetchGeneID(self, GeneSymbol):
        conn = self.ConnectDatabase()
        sqlCommand = """
            SELECT 
                NCBI.GENE_ID
            FROM ( ( SNP_AN_AS 
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            WHERE OTHER_SYMBOL.OTHER_SYMBOL = %s OR SNP_AN_AS.GENE_SYMBOL = %s
        """
        
        result = self.CreateTask(conn, sqlCommand, (GeneSymbol, GeneSymbol))
        self.CloseDatabase(conn)
        try:
            return result[0][0]
        except:
            return 'Not found'
    
    def HugeDataset(self, diseaseID):
        listGene = []
        
        pathDisease = self.LinkData
        
        res = soup(urllib.request.urlopen( pathDisease ), 'html.parser')
        
        findinres = res.find_all('table', {'style':'table_inside'})
        a = findinres[0].find_all('td', {'align':'left'})
        
        for i in a[:]:
            geneSymbol = ( i.get_text()[4:].split('\r\n   \t\t\t\t\t\t\n') )[0]
            
            # GeneID = self.FetchGeneID(geneSymbol)

            listGene.append({
                'DISEASE_ID': diseaseID,
                'GENE_ID' : "Not found",
                'GENE_SYMBOL' : geneSymbol,
                'SOURCE_WEBSITE' : 'huge'
            })

        return listGene

"""
Class detail
"""
class KeggInfo(GetDataFromFile):
    LinkData = None
    
    def __init__(self, linkData):
        GetDataFromFile.__init__(self)
        self.LinkData = linkData
        return
    
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
        
        pathDisease = self.LinkData
        
        res = soup(urllib.request.urlopen( pathDisease ), 'html.parser')
        
        # diseaseName = self.GetName(res)
        
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

"""
Class detail
"""
class Disease(GetDataFromFile, MetaData, Initialize):
    listNcbiData = []
    pathDisease = ''
    
    def __init__(self):
        GetDataFromFile.__init__(self)
        self.listNcbiData = self.ReadNcbiData()
        return
    
    def ImportDataToFile(self, fileName, data):
        self.pathDisease = self.GetPathToListDisease() + "/" + fileName + ".csv"
        importData = pd.DataFrame([t.__dict__ for t in data])
        importData.to_csv( self.pathDisease, mode='a', index = False)
        return
    
    def FetchGeneID(self, GeneSymbol):
        conn = self.ConnectDatabase()
        sqlCommand = """
            SELECT 
                NCBI.GENE_ID
            FROM ( ( SNP_AN_AS 
            INNER JOIN NCBI ON NCBI.GENE_ID = SNP_AN_AS.GENE_ID )
            INNER JOIN OTHER_SYMBOL ON OTHER_SYMBOL.GENE_ID = NCBI.GENE_ID)
            WHERE OTHER_SYMBOL.OTHER_SYMBOL = %s OR SNP_AN_AS.GENE_SYMBOL = %s
        """
        
        result = self.CreateTask(conn, sqlCommand, (GeneSymbol, GeneSymbol))
        self.CloseDatabase(conn)
        try:
            return result[0][0]
        except:
            return 'Not found'
      
    def CheckGeneWithMap(self, diseaseList, excludeList ):
        
        listGeneDisease = []
        UniqueList = [] # uses for check unique geneID
        ExcludeList = [eachGene['GENE_SYMBOL'] for eachGene in excludeList]
        # print('ExcludeList :', ExcludeList)
        
        for diseaseGene in diseaseList[:10]:
            
            Sources = ""
            GeneSymbol = diseaseGene['GENE_SYMBOL']
            SourceWebsite = diseaseGene['SOURCE_WEBSITE']
            diseaseID = diseaseGene['DISEASE_ID']
            
            if GeneSymbol not in UniqueList and GeneSymbol not in ExcludeList:
                # print( 'condition 1 |', GeneSymbol, SourceWebsite)
                
                GeneID = self.FetchGeneID(GeneSymbol)
                
                Matches = (detailDisease for detailDisease in (diseaseList) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                for Match in Matches: Sources = Sources + Match['SOURCE_WEBSITE'] + "; "
                Sources = Sources[:-2]
                
                listGeneDisease.append({
                    'GENE_ID' : GeneID,
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : Sources
                })
                
                UniqueList.append(GeneSymbol)
            elif GeneSymbol not in UniqueList and GeneSymbol in ExcludeList:
                # print( 'condition 2 |', GeneSymbol, SourceWebsite)
                
                Matches = (detailDisease for detailDisease in (diseaseList) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                for Match in Matches: Sources = Sources + Match['SOURCE_WEBSITE'] + "; "
                Sources = Sources[:-2]
                
                listGeneDisease.append({
                    'GENE_ID' : diseaseGene['GENE_ID'],
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : Sources
                })
                
                UniqueList.append(GeneSymbol)
            else:
                continue
            
        return listGeneDisease
    
    def CheckDuplicateDisease(self, diseaseID, listGeneAllDisease, listGeneOfDiseaseID):
        listGeneDisease = []
        UniqueListGeneSymbol = [] # uses for check unique genesID
        if ( len(listGeneAllDisease) > 0 ): ExcludeListGeneSymbol = [eachGene['GENE_SYMBOL'] for eachGene in listGeneAllDisease]
        else: ExcludeListGeneSymbol = []
        
        if ( len(listGeneAllDisease) > 0 ): ExcludeList = [eachGene['GENE_SYMBOL'] for eachGene in listGeneAllDisease]
        else: ExcludeList = []
        
        for diseaseGene in listGeneOfDiseaseID[:]:
            
            Sources = ""
            geneDisease = {}
            GeneSymbol = diseaseGene['GENE_SYMBOL']
            GeneID = diseaseGene['GENE_ID']
            
            if GeneSymbol not in UniqueListGeneSymbol and GeneSymbol not in ExcludeListGeneSymbol:
                # print( 'condition 1 |', diseaseGene)
                
                geneDisease = {
                    'GENE_ID' : GeneID,
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : diseaseGene['SOURCE_WEBSITE']
                }
                
                UniqueListGeneSymbol.append(GeneSymbol)
                listGeneDisease.append(geneDisease)
                
            elif GeneSymbol in UniqueListGeneSymbol and GeneSymbol not in ExcludeListGeneSymbol:
                # print( 'condition 2 |', diseaseGene)
                
                Matches = (detailDisease for detailDisease in (listGeneAllDisease + listGeneOfDiseaseID) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                for Match in Matches: 
                    Sources = Sources + Match['SOURCE_WEBSITE'] + "; "
                    if ( GeneID == 'Not found'):
                        if ( Match['SOURCE_WEBSITE'] == 'Not found'): continue
                        else: GeneID = Match['GENE_ID']
                        
                Sources = Sources[:-2]
                
                geneDisease = {
                    'GENE_ID' : GeneID,
                    'GENE_SYMBOL' : GeneSymbol,
                    'SOURCE_WEBSITE' : Sources
                }
                
                UniqueListGeneSymbol.append(GeneSymbol)
                Matches = (detailDisease for detailDisease in (listGeneDisease + listGeneAllDisease) if detailDisease['GENE_SYMBOL'] == GeneSymbol)
                print('index :', Matches)
            
            print( 'result :', geneDisease )
            
        print( 'UniqueListGeneSymbol :', UniqueListGeneSymbol )

        
        return
    
    def CheckDiseaseID(self, abbreviation):
        conn = self.ConnectDatabase()
        
        sqlCommand = '''
            SELECT DISEASE_ID FROM DISEASE WHERE DISEASE_ABBREVIATION = %s
        '''
        
        result = self.CreateTask(conn, sqlCommand, (str(abbreviation), ))
        
        self.CloseDatabase(conn)
        
        try:
            return result[0][0]
        except:
            return 'Not found'
    
    def CreateDiseaseDataset(self):
        metaData = MetaData()
        diseaseInfo = metaData.ReadMetadata('Disease')
        listGene = []
        allListGeneKegg = []
        allListGeneHuge = []
        
        for eachDisease in diseaseInfo['technical']['diseases']:
            
            print('Disease Name :', eachDisease['Name'])
            
            diseaseID = self.CheckDiseaseID(eachDisease['Abbreviation'])
            
            print('diseaseID :', diseaseID)
            
            keggInfo = KeggInfo(eachDisease['kege'])
            hugeDataset = HugeInfo(eachDisease['huge'])
            
            listGeneKegg = keggInfo.KeggDataset(diseaseID)
            listGeneHuge = hugeDataset.HugeDataset(diseaseID)
            
            listGeneEachDisease = listGeneKegg + listGeneHuge
            
            listGene = listGene + self.CheckGeneWithMap(listGeneEachDisease, listGeneKegg)
            
            # if ( diseaseID <= 4 ):
            
            #     keggInfo = KeggInfo(eachDisease['kege'])
            #     hugeDataset = HugeInfo(eachDisease['huge'])
                
            #     listGeneKegg = keggInfo.KeggDataset(diseaseID)
            #     listGeneHuge = hugeDataset.HugeDataset(diseaseID)
                
            #     listGeneEachDisease = listGeneKegg + listGeneHuge
                
            #     # listGene = self.CheckDuplicateDisease(diseaseID, listGene, listGeneEachDisease)
            #     listGene = listGene + self.CheckGeneWithMap(listGeneEachDisease, listGeneKegg)
                
            #     # print( listGene )
                
            #     # self.ImportDataToFile(diseaseName, listGene)
            # else:
            #     continue
        
        finalListGene = []
        
        for eachGene in listGene:
            print( eachGene )
            
        return
    
    def UpdateDiseaseDataset(self):
        metaData = MetaData()
        diseaseInfo = metaData.ReadMetadata('Disease')
        
        for eachDisease in diseaseInfo['technical']['diseases']:
            print( 'Abbreviation :', eachDisease['Abbreviation'] )
            DiseaseId = self.CheckDiseaseID(eachDisease['Abbreviation'])
            
            keggInfo = KeggInfo(eachDisease['kege'])
            hugeDataset = HugeInfo(eachDisease['huge'])
            
            # Get data on website
            listGeneKegg = keggInfo.KeggDataset(DiseaseId)
            listGeneHuge = hugeDataset.HugeDataset(DiseaseId)
            listGene = listGeneKegg + listGeneHuge
            
            # Update metadata
            eachDisease['lastMedoficationTime'] = time.time()
            
            listGene = self.CheckGeneWithMap(listGene, listGeneKegg)
            listGeneSymbolOnDisease = [eachGene['GENE_SYMBOL'] for eachGene in listGene]
            
            conn = self.ConnectDatabase()
            
            FormatStrings = ', '.join(['%s'] * len(listGeneSymbolOnDisease))
            Records = [DiseaseId] + listGeneSymbolOnDisease
            
            # Select Child from Parent
            # sqlCommand = '''
            #     SELECT GENE_SYMBOL, SOURCE_WEBSITE
            # ''' % FormatStrings
            
            # Parent
            # sqlCommand = '''
            #     SELECT GENE_SYMBOL FROM DISEASE_AS
            #     WHERE DISEASE_AS.DISEASE_ID = %%s
            #     AND DISEASE_AS.GENE_SYMBOL NOT IN (%s)
            # ''' % FormatStrings
            
            # result = self.CreateTask(conn, sqlCommand, Records)
            
            # print( result )
            
            for eachGene in listGene:
                
                FormatStrings = ', '.join(['%s'] * len(str(eachGene['SOURCE_WEBSITE']).split('; ')))
                
                sqlCommand = '''
                    SELECT * FROM AS_SOURCE
                    WHERE AS_SOURCE.GENE_SYMBOL = %%s
                    AND AS_SOURCE.SOURCE_WEBSITE IN (%s)
                ''' % FormatStrings
                
                Records = [eachGene['GENE_SYMBOL']] + ( list(map(str, (eachGene['SOURCE_WEBSITE']).split('; '))) )
                
                # print( 'Disease :', eachDisease['Abbreviation'], ' || GeneID :', eachGene['GENE_ID'], 'Records :', Records )
                
                result = self.CreateTask(conn, sqlCommand, Records)
                
                print( result )
                
                continue
            
            self.CloseDatabase(conn)
            
            # return
            
            # print( eachDisease['Abbreviation'] )
            # print( listGene )
            
            # # Select Disease id 
            # sqlCommand = ''' 
            #     SELECT DISEASE_ID FROM DISEASE
            #     WHERE DISEASE_ABBREVIATION = %s
            # '''
            # DiseaseID = (self.CreateTask(conn, sqlCommand, (eachDisease['Abbreviation'], )))[0][0]
            
            # # 
            # sqlCommand = ''' 
            #     SELECT GENE_SYMBOL, GENE_ID FROM DISEASE_AS
            #     WHERE DISEASE_ID = %s
            # '''
            # DiseaseID = (self.CreateTask(conn, sqlCommand, (eachDisease['Abbreviation'], )))
            
            # print( 'DiseaseID :', DiseaseID)
            
        # metaData.SaveManualUpdateMetadata(diseaseInfo)
        
        return
    
if __name__ == "__main__":
    # Test full process
    disease = Disease()
    
    # disease.CreateDiseaseDataset()
    
    # Test Input fetch data form website
    # hugeDataset = HugeInfo()
    # listGeneHuge = hugeDataset.HugeDataset()
    
    # print('listGeneHuge :', listGeneHuge)
    
    disease.UpdateDiseaseDataset()
    
    print('run main')