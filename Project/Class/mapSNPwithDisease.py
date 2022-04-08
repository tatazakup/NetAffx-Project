import pandas as pd
from Initialization import Database

class mapSNP_Disease:
    def __init__(self):
        self.ListGeneSNP = []
        self.ListGenePathway = []
        self.ListGeneDisease = []
        self.ListGeneFromSource = []
        self.sqlsave = "REPLACE INTO matching_snp_disease(RS_ID, DISEASE_ID, MatchBy, GENE_ID) VALUES(%s, %s, %s, %s)"

    def QueryGeneSNP(self, database, conn):
        sqlGeneSNP = "SELECT GENE_ID, RS_ID, GENE_SYMBOL FROM gene_snp;"
        resultGeneSNP = database.CreateTask(conn, sqlGeneSNP, ())
        for i in resultGeneSNP:
            self.ListGeneSNP.append(i)
        print('List Gene SNP Already use')

    def QueryGenePathway(self, database, conn):
        sqlGenePathway = "SELECT DISEASE_ID, GENE_ID, PATHWAY_ID FROM pathway;"
        resultGenePathway = database.CreateTask(conn, sqlGenePathway, ())
        for i in resultGenePathway:
            self.ListGenePathway.append(i)

    def QueryGeneDisease(self, database, conn):
        sqlGeneDisease = "SELECT DISEASE_ID, GENE_ID FROM gene_disease;"
        resultGeneDisease = database.CreateTask(conn, sqlGeneDisease, ())
        for i in resultGeneDisease:
            self.ListGeneDisease.append(i)

    def QueryGeneSource(self, database, conn):
        sqlGeneSource = "SELECT * FROM gene_disease_source;"
        resultGeneSource = database.CreateTask(conn, sqlGeneSource, ())
        for i in resultGeneSource:
            self.ListGeneFromSource.append(i)

    def MapDisease(self):
        database = Database()
        conn = database.ConnectDatabase()
        self.QueryGeneSNP(database, conn)
        self.QueryGeneDisease(database, conn)
        self.QueryGeneSource(database, conn)
        df_ListGeneDisease = pd.DataFrame(self.ListGeneDisease, columns= ['DISEASE_ID', 'GENE_ID'])
        df_ListGeneSource = pd.DataFrame(self.ListGeneFromSource, columns= ['GENE_SYMBOL', 'SOURCE_WEBSITE'])

        print("----check in disease-----")
        for i in self.ListGeneSNP:
            print("geneid :", i[0])
            matchGeneDis = df_ListGeneDisease.loc[df_ListGeneDisease['GENE_ID'] == i[0]]
            if matchGeneDis.empty:
                print("not match")
            else:
                listDis = matchGeneDis["DISEASE_ID"].values.tolist()
                for DisID in listDis:
                    checksource = df_ListGeneSource.loc[(df_ListGeneSource['GENE_SYMBOL'] == i[2]) & (df_ListGeneSource['DISEASE_ID'] == DisID)]
                    listSource = checksource['SOURCE_WEBSITE'].values.tolist()
                    for Sourceweb in listSource:
                        matchby =  Sourceweb
                        value = [i[1], DisID, matchby]
                        print('  ', value)
                        database.CreateTask(conn, self.sqlsave, (value))
                        print("   save success")
        database.CloseDatabase(conn)
        
    def MapPathway(self):
        database = Database()
        conn = database.ConnectDatabase()
        self.QueryGeneSNP(database, conn)
        self.QueryGenePathway(database, conn)
        df_ListGenePathway = pd.DataFrame(self.ListGenePathway, columns= ['DISEASE_ID', 'GENE_ID', 'PATHWAY_ID'])
        
        print("----check in pathway-----")   
        for i in self.ListGeneSNP:
            print("geneid :", i[0])
            matchGenePathway = df_ListGenePathway.loc[df_ListGenePathway['GENE_ID'] == i[0]]
            if matchGenePathway.empty:
               print("not match")
            else:
                listDisPathway = list(set( matchGenePathway['DISEASE_ID'].values.tolist() ))
                for DisID in listDisPathway:
                    dis_df = matchGenePathway.loc[matchGenePathway['DISEASE_ID'] == DisID]
                    list_pathway_disid = dis_df['PATHWAY_ID'].values.tolist()
                    matchby = 'Pathway ' + str(list_pathway_disid)
                    value = [i[1], DisID, matchby]
                    print('  ', value)
                    database.CreateTask(conn, self.sqlsave, (value))
                    print("   save success")
        database.CloseDatabase(conn)
    
    def MapBoth(self):
        # Connect database
        database = Database()
        conn = database.ConnectDatabase()

        # Query data for find match
        self.QueryGeneSNP(database, conn)
        self.QueryGeneDisease(database, conn)
        self.QueryGeneSource(database, conn)
        self.QueryGenePathway(database, conn)

        # Convert List to dataframe Pandas (easy for find specific value)
        df_ListGeneDisease = pd.DataFrame(self.ListGeneDisease, columns= ['DISEASE_ID', 'GENE_ID'])
        df_ListGeneSource = pd.DataFrame(self.ListGeneFromSource, columns= ['GENE_SYMBOL', 'SOURCE_WEBSITE', 'DISEASE_ID'])
        df_ListGenePathway = pd.DataFrame(self.ListGenePathway, columns= ['DISEASE_ID', 'GENE_ID', 'PATHWAY_ID'])

        for i in self.ListGeneSNP:
            print("geneid :", i[0])

            # Check By Gene in Disease
            print("  Check By Gene in Disease")
            matchGeneDis = df_ListGeneDisease.loc[df_ListGeneDisease['GENE_ID'] == i[0]]
            if matchGeneDis.empty:
                print("    not match")
            else:
                listDis = matchGeneDis["DISEASE_ID"].values.tolist()
                for DisID in listDis:
                    checksource = df_ListGeneSource.loc[(df_ListGeneSource['GENE_SYMBOL'] == i[2]) & (df_ListGeneSource['DISEASE_ID'] == DisID)]
                    listSource = checksource['SOURCE_WEBSITE'].values.tolist()
                    for Sourceweb in listSource:
                        matchby =  Sourceweb
                        value = [i[1], DisID, matchby, i[0]]
                        print('    ', value, end=' ')
                        database.CreateTask(conn, self.sqlsave, (value))
                        print("save success")
            
            # Check By Gene in Pathway
            print('  Check By Gene in Pathway')
            matchGenePathway = df_ListGenePathway.loc[df_ListGenePathway['GENE_ID'] == i[0]]
            if matchGenePathway.empty:
               print("    not match")
            else:
                listDisPathway = list(set( matchGenePathway['DISEASE_ID'].values.tolist() ))
                for DisID in listDisPathway:
                    dis_df = matchGenePathway.loc[matchGenePathway['DISEASE_ID'] == DisID]
                    list_pathway_disid = dis_df['PATHWAY_ID'].values.tolist()
                    matchby = 'Pathway ' + str(list_pathway_disid)
                    value = [i[1], DisID, matchby, i[0]]
                    print('    ', value,end=' ')
                    database.CreateTask(conn, self.sqlsave, (value))
                    print("save success")
        
        # Disconnect database
        database.CloseDatabase(conn)


if __name__ == "__main__":
    # map = mapSNPwithDis()
    # map.query()
    # map.Map()
    # map.SaveMatch2DB()

    testmap = mapSNP_Disease()
    testmap.MapBoth()
    print("---run success---")