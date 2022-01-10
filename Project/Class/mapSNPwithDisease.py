import pandas as pd
from Initialization import Database

class mapSNPwithDis:
    def __init__(self) -> None:
        self.ListGeneSNP = []
        self.ListGenePathway = []
        self.ListGeneDisease = []
        self.ListGeneFromSource = []
        self.ListGeneMatchDisease = []

    def query(self):
        database = Database()
        conn = database.ConnectDatabase()

        sqlGeneSNP = "SELECT GENE_ID, RS_ID, GENE_SYMBOL FROM gene_snp;"
        resultGeneSNP = database.CreateTask(conn, sqlGeneSNP, ())
        for i in resultGeneSNP:
            self.ListGeneSNP.append(i)

        sqlGenePathway = "SELECT DISEASE_ID, GENE_ID FROM pathway;"
        resultGenePathway = database.CreateTask(conn, sqlGenePathway, ())
        for i in resultGenePathway:
            self.ListGenePathway.append(i)

        sqlGeneDisease = "SELECT DISEASE_ID, GENE_ID FROM gene_disease;"
        resultGeneDisease = database.CreateTask(conn, sqlGeneDisease, ())
        for i in resultGeneDisease:
            self.ListGeneDisease.append(i)

        sqlGeneSource = "SELECT * FROM gene_disease_source;"
        resultGeneSource = database.CreateTask(conn, sqlGeneSource, ())
        for i in resultGeneSource:
            self.ListGeneFromSource.append(i)

        database.CloseDatabase(conn)
    
    def Map(self):
        df_ListGeneDisease = pd.DataFrame(self.ListGeneDisease, columns= ['DISEASE_ID', 'GENE_ID'])
        df_ListGenePathway = pd.DataFrame(self.ListGenePathway, columns= ['DISEASE_ID', 'GENE_ID'])
        df_ListGeneSource = pd.DataFrame(self.ListGeneFromSource, columns= ['GENE_SYMBOL', 'SOURCE_WEBSITE'])
        for i in self.ListGeneSNP:
            print("geneid :", i[0])
            print("----check in disease-----")
            matchGeneDis = df_ListGeneDisease.loc[df_ListGeneDisease['GENE_ID'] == i[0]]
            if matchGeneDis.empty:
                print("not match")
            else:
                listDis = matchGeneDis["DISEASE_ID"].values.tolist()

                print('GSYMBOL :', i[2])
                checksource = df_ListGeneSource.loc[df_ListGeneSource['GENE_SYMBOL'] == i[2]]
                listSource = checksource['SOURCE_WEBSITE'].values.tolist()
                for DisID in listDis:
                    for Sourceweb in listSource:
                        matchby = 'Gene In Disease From Web ' + Sourceweb
                        value = [i[1], DisID, matchby]
                        self.ListGeneMatchDisease.append(value)
            print("----check in pathway-----")        
            matchGenePathway =df_ListGenePathway.loc[df_ListGenePathway['GENE_ID'] == i[0]]
            if matchGenePathway.empty:
               print("not match")
            else:
                listDisPathway = matchGenePathway["DISEASE_ID"].values.tolist()
                for DisID in listDisPathway:
                    valuepathway = [i[1], DisID,  'Gene in Pathway']
                    self.ListGeneMatchDisease.append(valuepathway)
            print(" ")
                

    def SaveMatch2DB(self):
        database = Database()
        conn = database.ConnectDatabase()
        for matching in self.ListGeneMatchDisease:
            sql = "REPLACE INTO matching_snp_disease(RS_ID, DISEASE_ID, MatchBy) VALUES(%s, %s, %s)"
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