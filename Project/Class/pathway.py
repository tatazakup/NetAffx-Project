import pandas as pd
from Initialization import Database
import requests
from bs4 import BeautifulSoup


class GenePathway:
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
        self.ListDisease =  ['Bipolar Disorder', 
                            'Coronary Artery Disease', 
                            "Crohn Disease", 
                            'Hypertension', 
                            'Rheumatoid Arthritis', 
                            'Type 1 Diabetes Mellitus', 
                            'Type 2 Diabetes Mellitus']
        self.ListUrlDisease =   ['https://www.kegg.jp/entry/H01653', 
                                'https://www.kegg.jp/entry/H01742', 
                                'https://www.kegg.jp/entry/H00286', 
                                'https://www.kegg.jp/entry/H01633', 
                                'https://www.kegg.jp/entry/H00630', 
                                'https://www.kegg.jp/entry/H00408', 
                                'https://www.kegg.jp/entry/H00409']
        self.ListGenePathwayOfDisease = []
    
    def GetGeneInPathwayOfDisease(self, ListPathway):
        pathway = pd.DataFrame(ListPathway,columns = ['pathway', 'GeneID'])
        index = 0
        for URL in self.ListUrlDisease[1:]:
            index += 1
            print(self.ListDisease[index])
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            finda = soup.find_all('a')
            for i in finda:
                if i.text[:3] == "hsa":
                    findpath = pathway.loc[pathway['pathway'] == i.text]['GeneID']
                    listgene_pathway = findpath.values.tolist()
                    for gene in listgene_pathway:
                        col = []
                        col.extend([self.ListDisease[index], i.text, gene])
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

            sql = "INSERT INTO pathway (DISEASE_ID, PATHWAY_ID, GENE_ID) VALUES (%s, %s, %s)"
            val = (DISEASE_ID, GenePathwayDis[1], GenePathwayDis[2])
            database.CreateTask(conn, sql, val)
            print("save success")
        database.CloseDatabase(conn)


if __name__ == "__main__":
    List_Pathway = GenePathway()
    List_Pathway.GetGenePathway()
    Pathway_Dis = PathwayOfDis()
    Pathway_Dis.GetGeneInPathwayOfDisease(List_Pathway.listpathway)
    Pathway_Dis.SaveGenePathway2db()
    print("---run success---")