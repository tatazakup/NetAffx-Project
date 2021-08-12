from os import name
import pandas as pd
from Class_Initialization import GetDataFromFile, MetaData

class SNPobject(GetDataFromFile):
    def __init__(self, Chromosome, GeneSymbol, ProbeID, RSID, relationship, distance):
        GetDataFromFile.__init__(self)

        self.Chromosome =  Chromosome
        self.GeneSymbol = GeneSymbol
        self.ProbeSetID = ProbeID
        self.dbSNPRSID = RSID
        self.relationship = relationship
        self.distance = distance

class mapDisease(GetDataFromFile):
    def __init__(self):
        GetDataFromFile.__init__(self)
    
    def match_disease(self, df_disease, df_maindata, index):
        data = df_maindata.loc[df_maindata['NCBIGeneID'] == df_disease['ganeID'][index]]
        return data

    def convert_listofObject_ToCsv(self, list, path):
        df2csv = pd.DataFrame([t.__dict__ for t in list])
        df2csv.to_csv(path,index=False)

    def run(self):
        dataType2 = self.ReadDiseaseType2()
        dataNsp = self.ReadMain_Nsp()
        dataSty = self.ReadMain_Sty()
        ListMainData = [dataNsp, dataSty]
        indexname = 0
        for df in ListMainData:
            DataForExport = []
            for i in range(dataType2.shape[0]): # df.shape[0]
                if pd.isna(dataType2['ganeID'][i]):
                    pass
                else:
                    data = self.match_disease(dataType2, df, i)
                    for j in range(data.shape[0]):
                        row = SNPobject(
                            data.iloc[j]['Chromosome'],
                            data.iloc[j]['GeneSymbol'],
                            data.iloc[j]['ProbeSetID'],
                            data.iloc[j]['dbSNPRSID'],
                            data.iloc[j]['relationship'],
                            data.iloc[j]['distance']
                            )
                        DataForExport.append(row)

            namefile = ['Type 2 diabetes mellitus_Nsp.csv', 'Type 2 diabetes mellitus_Sty.csv']
            path = self.GetPathToListDisease() + '/' + namefile[indexname]
            self.convert_listofObject_ToCsv(DataForExport, path)
            indexname += 1

if __name__ == "__main__":
    mapdata = mapDisease()
    mapdata.run()
    print('run main')
