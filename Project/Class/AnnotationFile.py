from numpy import add
import pandas as pd
import os
from Initialization import Database, FilePath, MetaData
import time

class SNP:
    def __init__(self, RS_ID, ProbeSet_ID, Chromosome, Position, Source_Geneship):
        self.RS_ID = RS_ID
        self.ProbeSet_ID = ProbeSet_ID
        self.Chromosome = Chromosome
        self.Position = Position
        self.Soure_Geneship = Source_Geneship
        self.Associated_Gene = []

    def Add_AssociatedGene(self, Asso_Gene):
        self.Associated_Gene.append(Asso_Gene)

    def show(self):
        print('RS_ID :', self.RS_ID)
        print('RrobeSet_ID :', self.ProbeSet_ID)
        print('Chromosome :', self.Chromosome)
        print('Position :', self.Soure_Geneship)
        print('AssociatedGene :', self.Associated_Gene)

class AssociatedGene:
    def __init__(self, Gene_ID, GeneSymbol, Distance, Relationship):
        self.Gene_ID = Gene_ID
        self.GeneSymbol = GeneSymbol
        self.Distance = Distance
        self.Relationship = Relationship
    
    def value(self):
        list_value = [self.Gene_ID, self.GeneSymbol, self.Distance, self.Relationship]
        return list_value
    
    def show(self):
        print('   Gene_ID :', self.Gene_ID)
        print('   GeneSymbol :', self.GeneSymbol)
        print('   Distance :', self.Distance)
        print('   Relationship :', self.Relationship)

class Manage_AnnotationFile(FilePath):
    def __init__(self):
        FilePath.__init__(self)
        path_dir = self.GetPathToAnnotationFile()
        self.list_DataSet = []
        objectMeta = MetaData()
        SepGeneInfo = self.TryFetchDataOnMetaData(objectMeta, 'SeparateGene')
        SepGeneInfo['Status']['textStatus'] = 'Reading Annotation File'
        objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
        for (root, dirs, file) in os.walk(path_dir):
            for fileName in file:
                csvFile = pd.read_csv(path_dir + "/" + fileName)
                print(csvFile)
                self.list_DataSet.append(csvFile)
        self.list_Geneship = ["Nsp", "Sty"]
        SepGeneInfo['Status']['amountState'] = (self.list_DataSet[0].shape[0] + self.list_DataSet[1].shape[0] )*2
        SepGeneInfo['Status']['amountOfFinished'] = 1
        objectMeta.SaveManualUpdateMetadata(SepGeneInfo)


    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def Manage_SNP(self, dataset, index, Geneship):
        RS_ID = dataset["dbSNP RS ID"][index]
        ProbeSet_ID = dataset["Probe Set ID"][index]
        Chromosome = dataset["Chromosome"][index]
        Position = dataset["Physical Position"][index]
        return SNP(RS_ID, ProbeSet_ID, Chromosome, Position, Geneship)
    
    def Split_AssociatedGene(self, dataset, index):
        AssoGene_Data = dataset["Associated Gene"][index]
        List_Gene = AssoGene_Data.split('///')
        return List_Gene
    
    def Manage_AssociatedGene(self, Gene_detail):
        Relationship = Gene_detail[1]
        Distance = Gene_detail[2]
        GeneSymbol = Gene_detail[4]
        Gene_ID = Gene_detail[5]
        return AssociatedGene(Gene_ID, GeneSymbol, Distance, Relationship)

    def SeparateGene(self):
        objectMeta = MetaData()
        SepGeneInfo = self.TryFetchDataOnMetaData(objectMeta, 'SeparateGene')
        List_SNP = []
        number = 0
        for dataset in self.list_DataSet:
            for row_index in range(dataset.shape[0]): #dataset.shape[0] #range(50)
                Geneship = self.list_Geneship[number]
                SNP = self.Manage_SNP(dataset, row_index, Geneship)
                # write state metadata
                SepGeneInfo['Status']['textStatus'] = 'Separating Associated Gene Of SNP: ' + SNP.RS_ID + ' Genechip: ' + Geneship
                objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
                List_AssoGene = self.Split_AssociatedGene(dataset, row_index)
                memory_Gene = []
                if SNP.RS_ID and SNP.ProbeSet_ID and dataset["Associated Gene"][row_index] != '---':
                    for Gene in List_AssoGene:
                        Gene_detail = Gene.split(' // ')
                        Relationship = Gene_detail[1]
                        Distance = Gene_detail[2]
                        GeneSymbol = Gene_detail[4]
                        Gene_ID = Gene_detail[5]
                        if Gene_ID != '---':
                            Asso_Gene = self.Manage_AssociatedGene(Gene_detail)
                            if GeneSymbol in memory_Gene:
                                for mem_gene in SNP.Associated_Gene:
                                    if mem_gene.GeneSymbol == GeneSymbol:
                                        if mem_gene.Relationship == Relationship and int(mem_gene.Distance) > int(Distance):
                                            mem_gene.Distance = Distance
                                        elif mem_gene.Relationship != Relationship:
                                            SNP.Add_AssociatedGene(Asso_Gene)
                                            # Asso_Gene.show()
                            else:
                                memory_Gene.append(GeneSymbol)
                                SNP.Add_AssociatedGene(Asso_Gene)
                                # Asso_Gene.show()
                SNP.show()
                if SNP.RS_ID == "---" or SNP.ProbeSet_ID == "---":
                    pass
                    print("pass SNP", SNP.RS_ID, SNP.ProbeSet_ID)
                else:
                    List_SNP.append(SNP)
                SepGeneInfo['Status']['amountOfFinished'] = SepGeneInfo['Status']['amountOfFinished'] + 1
                objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
            number += 1
        return List_SNP
    
    def TestSeparateGene(self, RSID, Genechip):
        if Genechip.lower() == "nsp":
            dataset = self.list_DataSet[0]
            Geneship = self.list_Geneship[0]
        else:
            dataset = self.list_DataSet[1]
            Geneship = self.list_Geneship[1]
        
        # find index of rsid parameter
        row_index = dataset[dataset["dbSNP RS ID"] == RSID].index.values.astype(int)[0]

        # Print that associated gene of snp
        print("   Associated Gene From CSV" )
        AssGene_Value = dataset["Associated Gene"][row_index]
        listAssGene = AssGene_Value.split(' /// ')
        for G in listAssGene:
            print(G)
        print("")

        SNP = self.Manage_SNP(dataset, row_index, Geneship)
        List_AssoGene = self.Split_AssociatedGene(dataset, row_index)
        memory_Gene = []
        if SNP.RS_ID and SNP.ProbeSet_ID and dataset["Associated Gene"][row_index] != '---':
            for Gene in List_AssoGene:
                Gene_detail = Gene.split(' // ')
                Relationship = Gene_detail[1]
                Distance = Gene_detail[2]
                GeneSymbol = Gene_detail[4]
                Gene_ID = Gene_detail[5]
                if Gene_ID != '---':
                    Asso_Gene = self.Manage_AssociatedGene(Gene_detail)
                    if GeneSymbol in memory_Gene:
                        for mem_gene in SNP.Associated_Gene:
                            if mem_gene.GeneSymbol == GeneSymbol:
                                if mem_gene.Relationship and int(mem_gene.Distance) > int(Distance):
                                    mem_gene.Distance = Distance
                                elif mem_gene.Relationship != Relationship:
                                    SNP.Add_AssociatedGene(Asso_Gene)
                                    # Asso_Gene.show()
                    else:
                        memory_Gene.append(GeneSymbol)
                        SNP.Add_AssociatedGene(Asso_Gene)
                        # Asso_Gene.show()
        SNP.show()
        if SNP.RS_ID == "---" or SNP.ProbeSet_ID == "---":
            pass
            print("pass SNP", SNP.RS_ID, SNP.ProbeSet_ID)
        else:
            return SNP

    def SaveSNP(self, list):
        objectMeta = MetaData()
        SepGeneInfo = self.TryFetchDataOnMetaData(objectMeta, 'SeparateGene')
        database = Database()
        conn = database.ConnectDatabase()
        for SNP in list:
            SepGeneInfo['Status']['textStatus'] = 'Saving SNP ' + SNP.RS_ID  + ' to Database'
            objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
            sql = """
            INSERT INTO snp VALUES (%s, %s, %s, %s, %s)
            """
            val = (SNP.RS_ID, SNP.ProbeSet_ID, SNP.Chromosome, SNP.Position, SNP.Soure_Geneship)
            print("sql1 insert to snp table:", val)
            database.CreateTask(conn, sql, val)

            for gene in SNP.Associated_Gene:
                sqlcheck =  """
                SELECT * FROM gene_snp WHERE GENE_ID = %s AND RS_ID = %s
                """
                valcheck = (gene.Gene_ID, SNP.RS_ID)
                resultcheck = database.CreateTask(conn, sqlcheck, valcheck)
                if len(resultcheck) == 0:
                    sql2 = """
                            INSERT INTO gene_snp VALUES (%s, %s, %s)
                            """
                    val2 = (gene.Gene_ID, SNP.RS_ID, gene.GeneSymbol)
                    print("sql2 insert to gene_snp table:", val2)
                    database.CreateTask(conn, sql2, val2)
                else:
                    print("gene was in db :", valcheck)
                sql3 = """
                INSERT INTO gene_detail (GENE_ID, RS_ID, DISTANCE, RELATIONSHIP) VALUES (%s, %s, %s, %s)
                """
                val3 = (gene.Gene_ID, SNP.RS_ID, gene.Distance, gene.Relationship)
                print("sql3 insert to gene_detail table:", val3)
                database.CreateTask(conn, sql3, val3)
            SepGeneInfo['Status']['amountOfFinished'] = SepGeneInfo['Status']['amountOfFinished'] + 1
            objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
        SepGeneInfo['Status']['amountOfFinished'] = SepGeneInfo['Status']['amountState']
        objectMeta.SaveManualUpdateMetadata(SepGeneInfo)
        database.CloseDatabase(conn)
    
    def DropSNP(self):
        database = Database()
        conn = database.ConnectDatabase()
        sql3 =   """
                DELETE FROM gene_detail
                """
        database.CreateTask(conn, sql3, ())
        sql2 =   """
                DELETE FROM gene_snp
                """
        database.CreateTask(conn, sql2, ())
        sql =   """
                DELETE FROM snp
                """
        database.CreateTask(conn, sql, ())
        database.CloseDatabase(conn)
        
if __name__ == "__main__":
    AF = Manage_AnnotationFile()
    ListS = AF.SeparateGene()
    print(ListS)
    AF.SaveSNP(ListS)
    # # AF.DropSNP()
    # print("---run success---")




    
        
    


