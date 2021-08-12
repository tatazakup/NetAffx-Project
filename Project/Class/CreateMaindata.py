from os import name
import pandas as pd
from Class_Initialization import GetDataFromFile, MetaData
from datetime import datetime

class SNP:
    def __init__(self, ProbeID, RSID, Chromosome, relationship, distance, GeneSymbol, NCBIGeneID):
        self.ProbeSetID = ProbeID
        self.dbSNPRSID = RSID
        self.Chromosome =  Chromosome
        self.relationship = relationship
        self.distance = distance
        self.GeneSymbol = GeneSymbol
        self.NCBIGeneID = NCBIGeneID
        self.AlsoKnowAs = []
        self.UpdatedAt = None
    
    def updateAlsoKnowAs(self, list, timestamp):
        self.AlsoKnowAs = list
        self.UpdatedAt = timestamp

class Maindata(GetDataFromFile):
    def __init__(self):
        GetDataFromFile.__init__(self)

    def ConvertTimeStampToDatetime(self, timeInput):
        timeOutput = datetime.fromtimestamp(timeInput)
        return timeOutput

    def separateGeneOfSNP(self,listgene):
        split_Gene = listgene.split('///')
        return split_Gene

    def ConvertListToCsv(self, list, listcolumns, path_output):
        df = pd.DataFrame(list,columns = listcolumns)
        df.to_csv(path_output,index=False)

    def CreateMainData(self):
        dataNsp = self.ReadListSNP_Nsp()
        dataSty = self.ReadListSNP_Sty()
        ListMainData = [dataNsp, dataSty]
        indexname = 0
        for i in ListMainData:
            All_ProbeID = i['Probe Set ID']
            All_SnpID = i['dbSNP RS ID']
            All_Gene = i['Associated Gene']
            All_Chromosome = i['Chromosome']
            DataForExport = []
            for row in range(5): # i.shape[0]
                eachrow_ProbeID = All_ProbeID[row]
                eachrow_SnpID = All_SnpID[row]
                eachrow_Chromosome = All_Chromosome[row]
                eachrow_Gene = All_Gene[row]
                split_Gene = self.separateGeneOfSNP(eachrow_Gene)
                memory = []
                listGeneInSNP = []
                if eachrow_ProbeID and eachrow_SnpID and eachrow_Gene != '---':
                     for Gene in split_Gene:
                        GeneDetail = Gene.split(' // ') # -- Gene[1] = relationship // Gene[2] = distance // Gene[4] = GeneSymbol // Gene[5] = GeneID
                        if GeneDetail[5] != '---': #Check GeneID != '---'
                            GeneSymbol = GeneDetail[4] 
                            GeneID = GeneDetail[5]
                            SnpRelationship = GeneDetail[1] 
                            GeneDistance = GeneDetail[2]
                            col = []
                            if GeneSymbol in memory :
                                for i in listGeneInSNP:
                                    if i[5] == GeneSymbol:
                                        if i[3] == SnpRelationship and int(i[4]) > int(GeneDetail[2]):
                                            i[4] = GeneDistance
                                        elif i[3] != SnpRelationship:
                                            col = []
                                            col.append(eachrow_ProbeID)
                                            col.append(eachrow_SnpID)
                                            col.append(eachrow_Chromosome)
                                            col.append(SnpRelationship)
                                            col.append(GeneDistance)
                                            col.append(GeneSymbol)
                                            col.append(GeneID)
                                            if col not in listGeneInSNP:
                                                listGeneInSNP.append(col)
                            else :
                                memory.append(GeneDetail[4])
                                col.append(eachrow_ProbeID)
                                col.append(eachrow_SnpID)
                                col.append(eachrow_Chromosome)
                                col.append(SnpRelationship)
                                col.append(GeneDistance)
                                col.append(GeneSymbol)
                                col.append(GeneID)
                                listGeneInSNP.append(col)

                for eachGene in listGeneInSNP:
                    DataForExport.append(eachGene)

            listcolumns = ['ProbeSetID', 'dbSNPRSID', 'Chromosome', 'relationship', 'distance', 'GeneSymbol', 'NCBIGeneID']
            namefile = ['demo_MainData_Nsp.csv', 'demo_MainData_Sty.csv'] # 'MainData_Nsp.csv', 'MainData_Sty.csv'
            path_output = self.GetPathToMainCSV() + '/' + namefile[indexname]
            self.ConvertListToCsv(DataForExport, listcolumns, path_output)
            indexname += 1
        
if __name__ == "__main__":
    listSNPdata = Maindata()
    listSNPdata.CreateMainData()
    print('run main')
