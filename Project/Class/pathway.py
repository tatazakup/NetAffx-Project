from tkinter import E
from matplotlib.font_manager import json_load
import pandas as pd
from Initialization import Database, MetaData, FilePath
import requests
from bs4 import BeautifulSoup
import json


class PathwayDataFromKEGG:
    def __init__(self):
        self.URL = 'http://rest.kegg.jp/link/hsa/pathway'
        self.listpathway = []

    def GetGenePathway(self):
        reqpage = requests.get(self.URL)
        soup = BeautifulSoup(reqpage.content, "html.parser")
        text = soup.text
        list_text = text.split('\n')
        for i in list_text[:-1]:
            col = []
            sep_pg = i.split('\t')
            pathway = sep_pg[0][5:]
            gene = sep_pg[1][4:]
            print(pathway, gene)
            col.extend([pathway, gene])
            self.listpathway.append(col)
    
class PathwayOfDis:
    def __init__(self):
        self.ListDisease =  ['Coronary Artery Disease', 
                            "Crohn Disease", 
                            'Hypertension', 
                            'Rheumatoid Arthritis', 
                            'Type 1 Diabetes Mellitus', 
                            'Type 2 Diabetes Mellitus',             	
                            'Bipolar disorder']
        self.ListUrlDisease =   ['https://www.kegg.jp/entry/H01742', 
                                'https://www.kegg.jp/entry/H00286', 
                                'https://www.kegg.jp/entry/H01633', 
                                'https://www.kegg.jp/entry/H00630', 
                                'https://www.kegg.jp/entry/H00408', 
                                'https://www.kegg.jp/entry/H00409',
                                'https://www.kegg.jp/entry/H01653']

        self.ListGenePathwayOfDisease = []
    
    def FetchPathwayEachDisease(self):
        index = 0
        
        # Call metadata
        objectPathway = MetaData()
        objectPathway.ReadMetadata('pathway')

        for URL in self.ListUrlDisease:
            print(self.ListDisease[index])
            reqpage_kegg = requests.get(URL)
            gethtml_kegg = BeautifulSoup(reqpage_kegg.content, "html.parser")
            finda = gethtml_kegg.find_all('a')
            for i in finda:
                if i.text[:3] == "hsa":
                    print('  ', i.text, end = '' )
                    if i.text not in objectPathway.dataOnMetadata[self.ListDisease[index]] :
                        objectPathway.dataOnMetadata[self.ListDisease[index]].append(i.text)
                        print(' New Pathway')
                    else:
                        print(' exist Pathway')

            index += 1
        
        # Update Metadata
        objectPathway.SaveUpdateMetadata()
    
    def Find_GeneInPathwayOfDisease(self, DataPathway):
        df_pathway = pd.DataFrame(DataPathway,columns = ['pathway', 'GeneID'])
        
        # Read Pathway From metadata
        objectPathway = MetaData()
        Dict_pathway = objectPathway.ReadMetadata('pathway')
        for DisName in Dict_pathway:
            if DisName != "Status":
                for pathwayid in Dict_pathway[DisName]:
                    FindGeneEachPathway = df_pathway.loc[df_pathway['pathway'] == pathwayid]['GeneID']
                    ListResult_FindGene = FindGeneEachPathway.values.tolist()
                    for gene in ListResult_FindGene:
                        col = []
                        col.extend([DisName, pathwayid, gene])
                        print(col)
                        self.ListGenePathwayOfDisease.append(col)
    
    def SaveGenePathway2db(self):
        database = Database()
        conn = database.ConnectDatabase()
        for GenePathwayDis in self.ListGenePathwayOfDisease:
            if GenePathwayDis[0] == "Type 1 Diabetes Mellitus":
                DISEASE_ID = 1
            elif GenePathwayDis[0] == "Type 2 Diabetes Mellitus":
                DISEASE_ID = 2
            elif GenePathwayDis[0] == "Bipolar disorder":
                DISEASE_ID = 3
            elif GenePathwayDis[0] == 'Coronary Artery Disease':
                DISEASE_ID = 4
            elif GenePathwayDis[0] == "Crohn Disease":
                DISEASE_ID = 5
            elif GenePathwayDis[0] == "Hypertension":
                DISEASE_ID = 6
            elif GenePathwayDis[0] == "Rheumatoid Arthritis":
                DISEASE_ID = 7

            sql = "REPLACE INTO pathway (DISEASE_ID, PATHWAY_ID, GENE_ID) VALUES (%s, %s, %s)"
            val = (DISEASE_ID, GenePathwayDis[1], GenePathwayDis[2])
            database.CreateTask(conn, sql, val)
            # print(val, end='')
        print("save success")
        database.CloseDatabase(conn)


if __name__ == "__main__":
    Data_Pathway = PathwayDataFromKEGG()
    Data_Pathway.GetGenePathway()
    Pathway_Dis = PathwayOfDis()
    Pathway_Dis.FetchPathwayEachDisease()
    Pathway_Dis.Find_GeneInPathwayOfDisease(Data_Pathway.listpathway)
    Pathway_Dis.SaveGenePathway2db()

    print("---run success---")