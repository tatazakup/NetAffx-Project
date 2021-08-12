from os import name
import pandas as pd
from Class_Initialization import GetDataFromFile, MetaData
from datetime import datetime

class SNPobject(GetDataFromFile):
    def __init__(self, ProbeID, RSID, Chromosome, relationship, distance, GeneSymbol, NCBIGeneID):
        GetDataFromFile.__init__(self)

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

class mapAlsoKnowAs(GetDataFromFile):
    def __init__(self):
        GetDataFromFile.__init__(self)
    
    def GetAlsoKnowAs(self, dataframe, geneid):
        alsoknowas = dataframe.loc[dataframe['GeneID'] == int(geneid)]['AlsoKnowAs'].iloc[0][2:-2]
        return alsoknowas

    def GetTimeStamp(self, dataframe, geneid):
        timestamp = dataframe.loc[dataframe['GeneID'] == int(geneid)]['UpdatedAt'].iloc[0]
        return timestamp

    def convert_listofObject_ToCsv(self, list, path):
        df2csv = pd.DataFrame([t.__dict__ for t in list])
        df2csv.to_csv(path,index=False)

    def run(self):
        dataNCBI = self.ReadNcbiData()
        dataNsp = self.ReadMain_Nsp()
        dataSty = self.ReadMain_Sty()
        ListMainData = [dataNsp, dataSty]
        indexname = 0
        for df in ListMainData:
            DataForExport = []
            for i in range(5):
                row = SNPobject(
                    df['ProbeSetID'][i], 
                    df['dbSNPRSID'][i],
                    df['Chromosome'][i],
                    df['relationship'][i],
                    df['distance'][i],
                    df['GeneSymbol'][i],
                    df['NCBIGeneID'][i],
                    )
                alsoknowas = self.GetAlsoKnowAs(dataNCBI, df['NCBIGeneID'][i])
                timestamp = self.GetTimeStamp(dataNCBI, df['NCBIGeneID'][i])
                row.updateAlsoKnowAs(alsoknowas, timestamp)
                DataForExport.append(row)
            
            namefile = ['demo_MainData_Nsp_mapped.csv', 'demo_MainData_Sty_maped.csv'] # 'MainData_Nsp.csv', 'MainData_Sty.csv'
            path = self.GetPathToMainCSV() + '/' + namefile[indexname]
            self.convert_listofObject_ToCsv(DataForExport, path)
            indexname += 1

if __name__ == "__main__":
    mapdata = mapAlsoKnowAs()
    mapdata.run()
    print('run main')
