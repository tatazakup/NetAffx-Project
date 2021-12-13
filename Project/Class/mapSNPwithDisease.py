import pandas as pd
from Initialization import Database

class mapSNPwithDis:
    def __init__(self) -> None:
        self.ListGeneSNP = []
        self.ListGenePathway = []
        self.ListGeneDisease = []
        self.ListGeneMatchDisease = []

    def query(self):
        database = Database()
        conn = database.ConnectDatabase()

        sqlGeneSNP = "SELECT GENE_ID, RS_ID FROM snp_an_as;"
        resultGeneSNP = database.CreateTask(conn, sqlGeneSNP, ())
        for i in resultGeneSNP:
            self.ListGeneSNP.append(i)

        sqlGenePathway = "SELECT DISEASE_ID, GENE_ID FROM Pathway;"
        resultGenePathway = database.CreateTask(conn, sqlGenePathway, ())
        for i in resultGenePathway:
            self.ListGenePathway.append(i)

        sqlGeneDisease = "SELECT DISEASE_ID, GENE_ID FROM disease_as;"
        resultGeneDisease = database.CreateTask(conn, sqlGeneDisease, ())
        for i in resultGeneDisease:
            self.ListGeneDisease.append(i)

        database.CloseDatabase(conn)
    
    def Map(self):
        col = []
        df_ListGeneDisease = pd.DataFrame(self.ListGeneDisease, columns= ['DISEASE_ID', 'GENE_ID'])
        df_ListGenePathway = pd.DataFrame(self.ListGenePathway, columns= ['DISEASE_ID', 'GENE_ID'])
        for i in self.ListGeneSNP:
            matchGeneDis =df_ListGeneDisease.loc[df_ListGeneDisease['GENE_ID'] == i[0]]
            if matchGeneDis.empty:
                pass
            else:
                listDis = matchGeneDis["DISEASE_ID"].values.tolist()
                for DisID in listDis:
                    value = [i[1], DisID]
                    self.ListGeneMatchDisease.append(value)
            matchGenePathway =df_ListGenePathway.loc[df_ListGenePathway['GENE_ID'] == i[0]]
            if matchGenePathway.empty:
               pass
            else:
                listDisPathway = matchGenePathway["DISEASE_ID"].values.tolist()
                for DisID in listDisPathway:
                    valuepathway = [i[1], DisID]
                    self.ListGeneMatchDisease.append(valuepathway)

    def SaveMatch2DB(self):
        database = Database()
        conn = database.ConnectDatabase()
        for matching in self.ListGeneMatchDisease:
            sql = "REPLACE INTO snp_an_disease(RS_ID, DISEASE_ID) VALUES(%s, %s)"
            val = (matching)
            resultGeneDisease = database.CreateTask(conn, sql, val)
            print("save success")
        database.CloseDatabase(conn)

if __name__ == "__main__":
    map = mapSNPwithDis()
    map.query()
    map.Map()
    print(map.ListGeneMatchDisease)
    map.SaveMatch2DB()
    print("---run success---")