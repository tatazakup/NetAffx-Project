from bs4 import BeautifulSoup as soup
import urllib.request
from Class_Initialization import GetDataFromFile
import pandas as pd

class HugeInfo(GetDataFromFile):
    
    def __init__(self):
        GetDataFromFile.__init__(self)
        return
    
    def HugeDataset(self):
        
        pathDisease = self.sourceWebsite['huge']['first'] + r'C0011854' + self.sourceWebsite['huge']['second']
        
        res = soup(urllib.request.urlopen( pathDisease ), 'html.parser')
        
        findinres = res.find_all('table', {'style':'table_inside'})
        a = findinres[0].find_all('td', {'align':'left'})
        listGene = []
        for i in a:
            geneSymbol = ( i.get_text()[4:].split('\r\n   \t\t\t\t\t\t\n') )[0]
            
            listGene.append(geneSymbol)

        return listGene

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
        
        pathDisease = self.sourceWebsite['kegg'] + '/ds:H00408'
        
        res = soup(urllib.request.urlopen(pathDisease), 'html.parser')
        
        diseaseName = self.GetName(res)
        
        allGene = self.GetAllGene(res)
        
        listGene = []
        for eachGene in allGene:
            separateWord = eachGene.split('[')
            ganeSymbol = ( separateWord[0].split() )[0]
            # ganeID = ( ( separateWord[1].split(':')[1] ).split() )[0].replace(']', '')
            
            listGene.append( ganeSymbol )
        
        return diseaseName, listGene
    
class Disease(GetDataFromFile):
    listNcbiData = []
    pathDisease = ''
    
    def __init__(self):
        GetDataFromFile.__init__(self)
        self.listNcbiData = self.ReadNcbiData()
        return
    
    def CreateDiseaseFile(self, fileName):
        self.pathDisease = self.GetPathToListDisease() + "/" + fileName + ".csv"
        self.diseaseHeader.to_csv( self.pathDisease, index = False)
        return
    
    def ImportDataToFile(self, data):
        importData = pd.DataFrame(data)
        importData.to_csv( self.pathDisease, mode='a', index = False, header=False)
        return
    
    def CheckGeneWithMap(self, listGene):
        unique_list = []
        unique_list_done = []
        for geneSymbol in listGene:
            if geneSymbol not in unique_list_done:
                
                geneDetail = {
                    'geneSymbol' : geneSymbol,
                    'ganeID' : ''
                }
                
                listGene =  self.listNcbiData[self.listNcbiData['geneSymbol'] == str(geneSymbol)]
                
                if ( listGene.size == 0 ):
                    print('Gene Symbol not matching with', geneSymbol)
                    
                    geneObject =  self.listNcbiData[self.listNcbiData['alsoKnowAs'].str.contains(geneSymbol)]
                    
                    index = 0
                    for index, row in geneObject.iterrows():
                        
                        result = [v for v in row['alsoKnowAs'][2:-2].split('; ') if geneSymbol == v]
                        if ( result != [] ):
                            geneDetail['ganeID'] = row['geneID']
                            break
                        else:
                            index += 1
                else:
                    geneDetail['ganeID'] = (listGene['geneID'].values)[0]
                
                print( geneDetail )
                unique_list_done.append(geneSymbol)
                unique_list.append(geneDetail)
                
            else:
                continue
            
        return unique_list
    
    def CreateDiseaseDataset(self):
        
        keggInfo = KeggInfo()
        diseaseName, listGeneKegg = keggInfo.KeggDataset()
        
        hugeDataset = HugeInfo()
        listGeneHuge = hugeDataset.HugeDataset()
        
        listGene = listGeneHuge + listGeneKegg
        
        listGene = self.CheckGeneWithMap(listGene)
        
        self.CreateDiseaseFile(diseaseName)
        self.ImportDataToFile(listGene)
        
        return
    
if __name__ == "__main__":
    disease = Disease()
    disease.CreateDiseaseDataset()
    
    print('run main')