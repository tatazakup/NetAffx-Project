from numpy import add
import pandas as pd
import os
from Initialization import Database

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
        print('Gene_ID :', self.Gene_ID)
        print('GeneSymbol :', self.GeneSymbol)
        print('Distance :', self.Distance)
        print('Relationship :', self.Relationship)

class Manage_AnnotationFile:
    def __init__(self):
        self.Data_Nsp = pd.read_csv("D:\\SNP_Project\\NetAffx-Project\\Project\\AnnotationFile\\Mapping250K_Nsp.na32.annot.csv")
        self.Data_Sty = pd.read_csv("D:\\SNP_Project\\NetAffx-Project\\Project\\AnnotationFile\\Mapping250K_Sty.na32.annot.csv")
        self.list_DataSet = [self.Data_Nsp, self.Data_Sty]
        self.list_Geneship = ["Nsp", "Sty"]

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
        List_SNP = []
        number = 0
        for dataset in self.list_DataSet:
            for row_index in range(2): #dataset.shape[0]
                Geneship = self.list_Geneship[number]
                SNP = self.Manage_SNP(dataset, row_index, Geneship)
                List_AssoGene = self.Split_AssociatedGene(dataset, row_index)
                memory_Gene = []
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
                                        mem_gene.Relationship = Distance
                                    elif mem_gene.Relationship != Relationship:
                                        SNP.Add_AssociatedGene(Asso_Gene)
                                        # Asso_Gene.show()
                        else:
                            memory_Gene.append(GeneSymbol)
                            SNP.Add_AssociatedGene(Asso_Gene)
                            # Asso_Gene.show()
                SNP.show()
                List_SNP.append(SNP)
            number += 1
        return List_SNP
    
    def SaveSNP(self, list):
        database = Database()
        conn = database.ConnectDatabase()
        for SNP in list:
            sql = """
            INSERT INTO snp_an VALUES (%s, %s, %s, %s, %s)
            """
            val = (SNP.RS_ID, SNP.ProbeSet_ID, SNP.Chromosome, SNP.Position, SNP.Soure_Geneship)
            database.CreateTask(conn, sql, val)

            for gene in SNP.Associated_Gene:
                sql2 = """
                INSERT INTO snp_an_as VALUES (%s, %s, %s)
                """
                val2 = (gene.Gene_ID, SNP.RS_ID, gene.GeneSymbol)
                database.CreateTask(conn, sql2, val2)
                print("sql2success")

                sql3 = """
                INSERT INTO snp_an_as_detail (GENE_ID, RS_ID, DISTANCE, RELATIONSHIP) VALUES (%s, %s, %s, %s)
                """
                val3 = (gene.Gene_ID, SNP.RS_ID, gene.Distance, gene.Relationship)
                database.CreateTask(conn, sql3, val3)
                print("sql3success")

        database.CloseDatabase(conn)
    
    def DropSNP(self):
        database = Database()
        conn = database.ConnectDatabase()
        sql3 =   """
                DELETE FROM snp_an_as_detail
                """
        database.CreateTask(conn, sql3, ())
        sql2 =   """
                DELETE FROM snp_an_as
                """
        database.CreateTask(conn, sql2, ())
        sql =   """
                DELETE FROM snp_an
                """
        database.CreateTask(conn, sql, ())
        database.CloseDatabase(conn)
        
if __name__ == "__main__":
    AF = Manage_AnnotationFile()
    ListS = AF.SeparateGene()
    AF.SaveSNP(ListS)
    # AF.DropSNP()
    print("---run success---")
    


    
        
    




    
        
    


