from bs4 import BeautifulSoup as soup
import urllib.request
from Class_Initialization import GetDataFromFile
import pandas as pd

class ModelDisease():
    def __init__(self, _GeneID, _GeneSymbol, _Source):
        self.GeneID = _GeneID
        self.GeneSymbol = _GeneSymbol
        self.Source = _Source

"""
Class detail
"""
class HugeInfo(GetDataFromFile):
    
    def __init__(self):
        GetDataFromFile.__init__(self)
        return
    
    def HugeDataset(self):
        
        pathDisease = self.sourceWebsite['huge']['first'] + r'C0011860' + self.sourceWebsite['huge']['second'] # Set default path for get data from website
        
        res = soup(urllib.request.urlopen( pathDisease ), 'html.parser')
        
        findinres = res.find_all('table', {'style':'table_inside'})
        a = findinres[0].find_all('td', {'align':'left'})
        listGene = []
        for i in a:
            geneSymbol = ( i.get_text()[4:].split('\r\n   \t\t\t\t\t\t\n') )[0]
            
            listGene.append({
                'geneSymbol' : geneSymbol,
                'source' : 'huge'
            })

        return listGene

"""
Class detail
"""
class KeggInfo(GetDataFromFile):
    
    def __init__(self):
        GetDataFromFile.__init__(self)
        return
    
    def GetName(self, inputDOM):
        positionDiseaseNameHTML = inputDOM.find("th", string="Name")
        diseaseName = ( (positionDiseaseNameHTML.previous_element).find("td") ).next_element.next_element
        return diseaseName
    
    def GetAllGene(self, inputDOM):
        positionGeneHTML = inputDOM.find("th", string="Gene")
        allGeneNotSeparate = ( (positionGeneHTML.previous_element).find("td") ).next_element
        allGene = allGeneNotSeparate.get_text().split('\n')
        allGene.pop()
        return allGene
    
    def KeggDataset(self):
        
        pathDisease = self.sourceWebsite['kegg'] + '/H00409' # Set default path for get data from website

        res = soup(urllib.request.urlopen(pathDisease), 'html.parser')
        
        diseaseName = self.GetName(res)
        
        allGene = self.GetAllGene(res)
        
        listGene = []
        for eachGene in allGene:
            separateWord = eachGene.split('[')
            geneSymbol = ( separateWord[0].split() )[0]
            # ganeID = ( ( separateWord[1].split(':')[1] ).split() )[0].replace(']', '')
            
            listGene.append({
                'geneSymbol' : geneSymbol,
                'source' : 'kegg'
            })
        
        return diseaseName, listGene

"""
Class detail
"""
class Disease(GetDataFromFile):
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
    
    def FetchGeneID(self, geneSymbol):
        geneObject =  self.listNcbiData[self.listNcbiData['geneSymbol'] == str(geneSymbol)] # try map geneSymbol with geneSymbol on file GeneWithMap
        
        if ( geneObject.size == 0 ): # if not found geneSymbol
            geneObject =  self.listNcbiData[self.listNcbiData['alsoKnowAs'].str.contains(str(geneSymbol), na=False)] # try map geneAlsoKnowAs with geneSymbol on file GeneWithMap
                
            for index, row in geneObject.iterrows():
                
                result = [v for v in row['alsoKnowAs'].split('; ') if str(geneSymbol) == str(v)]
                if ( result != [] ):
                    return row['geneID']
        else: # if found geneSymbol
            return (geneObject['geneID'].values)[0]
        
        return ''
    
    def CheckGeneWithMap(self, listDiseaseGene):
        listGeneDisease = []
        unique_list = [] # uses for check unique geneID
        for diseaseGene in listDiseaseGene:
            
            geneSymbol = diseaseGene['geneSymbol']
            
            if geneSymbol not in unique_list:
                geneID = self.FetchGeneID(geneSymbol)
                
                matches = (x for x in (listDiseaseGene) if x['geneSymbol'] == geneSymbol)
                
                sources = ''
                
                for match in matches: sources = sources + match['source'] + "; "
                
                sources = sources[:-2]
                
                print(geneSymbol, geneID, sources)
                
                geneDisease = ModelDisease(
                    _GeneID = geneID,
                    _GeneSymbol = geneSymbol,
                    _Source = sources
                )
                listGeneDisease.append(geneDisease)
                unique_list.append(geneSymbol)
            
            else:
                continue
            
        return listGeneDisease
    
    def CreateDiseaseDataset(self):
        
        keggInfo = KeggInfo()
        diseaseName, listGeneKegg = keggInfo.KeggDataset()

        hugeDataset = HugeInfo()
        listGeneHuge = hugeDataset.HugeDataset()
        
        listGene = listGeneHuge + listGeneKegg
        
        listGene = self.CheckGeneWithMap(listGene)
        
        self.ImportDataToFile(diseaseName, listGene)
        
        return
    
if __name__ == "__main__":
    disease = Disease()
    disease.CreateDiseaseDataset()
    
    print('run main')