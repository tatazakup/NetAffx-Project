from Initialization import Database, FilePath
import pandas as pd

class Search(Database):
    def __init__(self):
        self.RS_ID = []
        self.ProbeSet_ID = []
        self.GeneID = []
        self.GeneSymbol = []

        # 0 All
        # 1 Chomosome#1
        # 3 Chomosome#2
        # \/
        # 23 Chomosome#23
        self.Chromosome = []

        # 0 equal
        # 1 less than
        # 2 more than
        # 3 between
        self.Position = []

        # 0 All 
        # 1 Nsp
        # 2 Sty
        self.Geneship = 0

        # 0 equal
        # 1 less than
        # 2 more than
        # 3 between
        self.Distance = []

        # All
        # upstream
        # downstream
        # intron
        self.Relationship = []

        # All
        # T1D
        # T2D
        # \/
        # RA
        self.Disease = []

        # 0 All 
        # 1 Huge
        # 2 Kegg
        # 3 Pathway
        self.source_website = 0

        return

    def ImportData(self, newData):
        for Each_data in newData:
            self.Add_RSID_PROBE_SET(Each_data)
        return

    def Add_RSID_PROBE_SET(self, newData):
        if 'rs' in str(newData): (self.RS_ID).append(str(newData))
        elif 'SNP' in str(newData): (self.ProbeSet_ID).append(str(newData))
        return

    def Add_GeneID(self, newData):
        self.GeneID = newData
        return
    
    def Add_GeneSymbol(self, newData):
        print('Add_GeneSymbol :', newData)
        if ( len(newData) == 1 ):
            if newData[0] == '':
                return
        self.GeneSymbol = newData
        return

    def Add_Chromosome(self, newData):
        self.Chromosome = newData
        return

    def Add_Position(self, newData):
        self.Position = newData
        return

    def Add_Geneship(self, newData):
        self.Geneship = newData
        return

    def Add_Distance(self, newData):
        self.Distance = newData
        return

    def Add_Relationship(self, newData):
        self.Relationship = newData
        return

    def Add_Disease(self, newData):
        self.Disease = newData
        return

    def Add_source_website(self, newData):
        self.source_website = newData
        return



    def CreateFormatStrings_RSID_ProbeSetID(self):
        FormatStrings_RSID_ProbeSetID = ''

        if ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) == 0 ):
            FormatStrings_RSID_ProbeSetID = ''

        elif ( len(self.RS_ID) == 1 ) and ( len(self.ProbeSet_ID) == 0 ):
            FormatStrings_RSID_ProbeSetID = "snp.RS_ID = '" + str(self.RS_ID[0]) + "'"
        
        elif ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) == 1 ):
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(self.ProbeSet_ID[0]) + "'"
        
        elif ( len(self.RS_ID) == 1 ) and ( len(self.ProbeSet_ID) == 1 ):
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(self.ProbeSet_ID[0]) + "' OR " + "snp.RS_ID = '" + str(self.RS_ID[0]) + "'"

        elif ( len(self.RS_ID) != 0 ) and ( len(self.ProbeSet_ID) == 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in self.RS_ID])
            FormatStrings_RSID_ProbeSetID = 'snp.RS_ID IN (' + listRS_ID + ')'

        elif ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) != 0 ):
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in self.ProbeSet_ID])
            FormatStrings_RSID_ProbeSetID = 'snp.PROBESET_ID IN (' + listProbeSet_ID + ')'

        elif ( len(self.RS_ID) != 0 ) and ( len(self.ProbeSet_ID) != 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in self.RS_ID])
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in self.ProbeSet_ID])

            FormatStrings_RSID_ProbeSetID = '( snp.RS_ID IN (' + listRS_ID + ') OR snp.PROBESET_ID IN (' + listProbeSet_ID + ') )'

        return FormatStrings_RSID_ProbeSetID

    def CreateFormatStrings_GeneID(self):
        FormatStrings_GeneID = ''
        if len(self.GeneID) > 1:
            listGeneID = ", ".join([str(Each_GeneID) for Each_GeneID in self.GeneID])
            FormatStrings_GeneID = 'and gene_detail.GENE_ID IN (' + listGeneID + ')'
        elif len(self.GeneID) == 1:
            FormatStrings_GeneID = 'and gene_detail.GENE_ID = ' + str(self.GeneID[0])
        return FormatStrings_GeneID

    def CreateFormatStrings_GeneSymbol(self):
        FormatStrings_GeneSymbol = ''
        if len(self.GeneSymbol) > 1:
            listGeneSymbol = ", ".join([("'" + str(Each_GeneSymbol) + "'") for Each_GeneSymbol in self.GeneSymbol])
            FormatStrings_GeneSymbol = 'and ( other_symbol.OTHER_SYMBOL IN (' + listGeneSymbol + ') OR gene_snp.GENE_SYMBOL IN (' + listGeneSymbol + ')' + ')'
        elif len(self.GeneSymbol) == 1:
            FormatStrings_GeneSymbol = "and ( other_symbol.OTHER_SYMBOL = '" + str(self.GeneSymbol[0]) + "' OR gene_snp.GENE_SYMBOL = '" + str(self.GeneSymbol[0]) + "')"
        return FormatStrings_GeneSymbol

    def CreateFormatStrings_Chromosome(self):
        FormatStrings_Chromosome = ''

        if len(self.Chromosome) == 0:
           return FormatStrings_Chromosome

        else:
            if 0 in self.Chromosome:
                return FormatStrings_Chromosome

            elif len(self.Chromosome) > 1:
                listChromosome = ", ".join([str(Each_Chromosome) for Each_Chromosome in self.Chromosome])
                FormatStrings_Chromosome = 'and snp.CHROMOSOME IN (' + listChromosome + ')'

            elif len(self.Chromosome) == 1:
                FormatStrings_Chromosome = 'and snp.CHROMOSOME = ' + str(self.Chromosome[0])

        return FormatStrings_Chromosome

    def CreateFormatStrings_GeneShip(self):
        if self.Geneship == 0:
            return ''
        elif self.Geneship == 1:
            return 'and snp.SOURCE_GENESHIP = "Nsp"'
        elif self.Geneship == 2:
            return 'and snp.SOURCE_GENESHIP = "Sty"'

    def CreateFormatStrings_Position(self):
        FormatStrings_Position = ''

        if ( len(self.Position) > 0):
            index = 0
            FormatStrings_Position = 'and '

            for condition in self.Position:
                if (condition[0] == 0):
                    FormatStrings_Position = FormatStrings_Position + 'snp.POSITION = ' + str(condition[1]) + ' '
                elif (condition[0] == 1):
                    FormatStrings_Position = FormatStrings_Position + 'snp.POSITION > ' + str(condition[1]) + ' '
                elif (condition[0] == 2):
                    FormatStrings_Position = FormatStrings_Position + 'snp.POSITION < ' + str(condition[1]) + ' '
                elif (condition[0] == 3):
                    FormatStrings_Position = FormatStrings_Position + 'snp.POSITION between ' + str(condition[1]) + ' and ' + str(condition[2]) + ' '

                if index != (len(self.Position) - 1 ):
                   FormatStrings_Position = FormatStrings_Position + " OR " 
                index = index + 1

        return FormatStrings_Position

    def CreateFormatStrings_Distance(self):
        FormatStrings_Distance = ''

        for condition in self.Distance:
            if (condition[0] == 0):
                FormatStrings_Distance = FormatStrings_Distance + 'and gene_detail.DISTANCE = ' + str(condition[1]) + ' '
            elif (condition[0] == 1):
                FormatStrings_Distance = FormatStrings_Distance + 'and gene_detail.DISTANCE > ' + str(condition[1]) + ' '
            elif (condition[0] == 2):
                FormatStrings_Distance = FormatStrings_Distance + 'and gene_detail.DISTANCE < ' + str(condition[1]) + ' '
            elif (condition[0] == 3):
                FormatStrings_Distance = FormatStrings_Distance + 'and gene_detail.DISTANCE between ' + str(condition[1]) + ' and ' + str(condition[2]) + ' '

        return FormatStrings_Distance    

    def CreateFormatStrings_Relationship(self):
        FormatStrings_Relationship = ''
        
        if len(self.Relationship) == 0:
           return FormatStrings_Relationship

        else:
            if 0 in self.Relationship:
                return FormatStrings_Relationship

            elif len(self.Relationship) > 1:
                listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in self.Relationship])
                FormatStrings_Relationship = 'and gene_detail.RELATIONSHIP IN (' + listRelationship + ')'

            elif len(self.Relationship) == 1:
                FormatStrings_Relationship = "and gene_detail.RELATIONSHIP = '" + str(self.Relationship[0]) + "'"

        return FormatStrings_Relationship

    def CreateFormatStrings_Disease(self):
        FormatStrings_Disease = ''

        if len(self.Disease) == 0:
           return FormatStrings_Disease

        else:
            if 0 in self.Disease:
                return FormatStrings_Disease

            elif len(self.Disease) > 1:
                listDisease = ", ".join( [("'" + str(Each_Disease) + "'") for Each_Disease in self.Disease])
                FormatStrings_Disease = 'and disease.DISEASE_ABBREVIATION IN (' + listDisease + ')'

            elif len(self.Disease) == 1:
                FormatStrings_Disease = "and disease.DISEASE_ABBREVIATION = '" + str(self.Disease[0]) + "'"

        return FormatStrings_Disease

    def CreateFormatStrings_Source_Website(self):
        if self.source_website == 0:
            return ''
        elif self.source_website == 1:
            return 'and matching_snp_disease.MatchBy = "huge"'
        elif self.source_website == 2:
            return 'and matching_snp_disease.MatchBy = "kegg"'
        elif self.source_website == 3:
            return 'and matching_snp_disease.MatchBy = "pathway"'

    def SearchData(self):
        database = Database()
        conn = database.ConnectDatabase()

        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID()
        FormatStrings_GeneID = self.CreateFormatStrings_GeneID()
        FormatStrings_GeneSymbol = self.CreateFormatStrings_GeneSymbol()
        FormatStrings_Chromosome = self.CreateFormatStrings_Chromosome()
        FormatStrings_Position = self.CreateFormatStrings_Position()
        FormatStrings_Distance = self.CreateFormatStrings_Distance()
        FormatStrings_Relationship = self.CreateFormatStrings_Relationship()
        FormatStrings_Disease = self.CreateFormatStrings_Disease()
        FormatStrings_GeneShip = self.CreateFormatStrings_GeneShip()
        FormatStrings_Source_Website = self.CreateFormatStrings_Source_Website()

        if ( FormatStrings_RSID_ProbeSetID == '' and FormatStrings_GeneID == '' and FormatStrings_GeneSymbol == '' 
            and FormatStrings_Chromosome == '' and FormatStrings_Position == '' and FormatStrings_Distance == '' 
            and FormatStrings_Relationship == '' and FormatStrings_Disease == '' and FormatStrings_GeneShip == '' 
            and FormatStrings_Source_Website == '' ): 
            IsUseWhere = ''
        else:
            IsUseWhere = 'WHERE'

        print( 'FormatStrings_RSID_ProbeSetID :', len(FormatStrings_RSID_ProbeSetID))

        mysqlCommand_FoundDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENESHIP,

                gene_detail.RELATIONSHIP, 
                gene_detail.DISTANCE,

                gene_snp.GENE_SYMBOL,
                gene_snp.GENE_ID,

                disease.DISEASE_NAME,
                disease.DISEASE_ABBREVIATION,

                matching_snp_disease.MatchBy
            FROM ( ( ( ( ( ( snp
            INNER JOIN gene_snp ON gene_snp.RS_ID = snp.RS_ID )
            INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID AND gene_detail.GENE_ID = gene_snp.GENE_ID)
            INNER JOIN ncbi ON ncbi.GENE_ID = gene_snp.GENE_ID )
            INNER JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            INNER JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID )
            INNER JOIN disease ON disease.DISEASE_ID = matching_snp_disease.DISEASE_ID )
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            ORDER BY snp.CHROMOSOME ASC, snp.POSITION ASC;
        """ % (
            IsUseWhere,
            FormatStrings_RSID_ProbeSetID,
            FormatStrings_GeneID,
            FormatStrings_GeneSymbol,
            FormatStrings_Chromosome,
            FormatStrings_Position,
            FormatStrings_Distance,
            FormatStrings_Relationship,
            FormatStrings_Disease,
            FormatStrings_GeneShip,
            FormatStrings_Source_Website
        )

        mysqlCommand_NotFoundDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENESHIP,

                gene_detail.RELATIONSHIP, 
                gene_detail.DISTANCE,

                gene_snp.GENE_SYMBOL,
                gene_snp.GENE_ID
            FROM ( ( ( ( ( snp
            INNER JOIN gene_snp ON gene_snp.RS_ID = snp.RS_ID )
            INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID AND gene_detail.GENE_ID = gene_snp.GENE_ID)
            INNER JOIN ncbi ON ncbi.GENE_ID = gene_snp.GENE_ID )
            INNER JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            LEFT JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID )
            WHERE demo_automap3.matching_snp_disease.RS_ID IS NULL
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            %s
            ORDER BY snp.CHROMOSOME ASC, snp.POSITION ASC;
        """ % (
            'and ' + FormatStrings_RSID_ProbeSetID,
            FormatStrings_GeneID,
            FormatStrings_GeneSymbol,
            FormatStrings_Chromosome,
            FormatStrings_Position,
            FormatStrings_Distance,
            FormatStrings_Relationship,
            FormatStrings_GeneShip
        )

        if ( len(FormatStrings_RSID_ProbeSetID) == 0):
            mysqlCommand_FoundDisease = mysqlCommand_FoundDisease.replace('and', '', 1)
            mysqlCommand_NotFoundDisease = mysqlCommand_NotFoundDisease.replace('and', '', 1)

        # print('mysqlCommand_FD :', mysqlCommand_FoundDisease)
        # print('mysqlCommand_NFD :', mysqlCommand_NotFoundDisease)

        results_FD = set( database.CreateTask(conn, mysqlCommand_FoundDisease, ()) )
        results_NFD = set( database.CreateTask(conn, mysqlCommand_NotFoundDisease, ()) )
        listResult_FD = []
        listResult_NFD = []
        if ( results_FD != [] ):
            # print('\n List gene has found on disease \n')

            Index = 0
            for result in results_FD:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                # print(
                #     '               INDEX :', Index, '\n'
                #     '                RSID :', result[0], '\n'
                #     '         PROBESET_ID :', result[1], '\n'
                #     '          CHROMOSOME :', result[2], '\n'
                #     '            POSITION :', result[3], '\n'
                #     '     SOURCE_GENESHIP :', result[4], '\n'
                #     '        RELATIONSHIP :', result[5], '\n'
                #     '            DISTANCE :', result[6], '\n'
                #     '         GENE_SYMBOL :', result[7], '\n'
                #     '             GENE_ID :', result[8], '\n'
                #     '        OTHER_SYMBOL :', ', '.join([str(elem)[2:-3] for elem in other_symbol]), '\n'
                #     '        DISEASE_NAME :', result[9], '\n'
                #     'DISEASE_ABBREVIATION :', result[10], '\n'
                #     '            MATCH_BY :', result[11], '\n'
                # )

                each_result = [result[0],result[1],int(result[2]),result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]
                Index = Index + 1
                listResult_FD.append(each_result)

        if ( results_NFD != [] ):
            # print('\n List gene has not found on disease \n')

            Index = 0
            for result in results_NFD:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                # print(
                #     '               INDEX :', Index, '\n'
                #     '                RSID :', result[0], '\n'
                #     '         PROBESET_ID :', result[1], '\n'
                #     '          CHROMOSOME :', result[2], '\n'
                #     '            POSITION :', result[3], '\n'
                #     '     SOURCE_GENESHIP :', result[4], '\n'
                #     '        RELATIONSHIP :', result[5], '\n'
                #     '            DISTANCE :', result[6], '\n'
                #     '         GENE_SYMBOL :', result[7], '\n'
                #     '             GENE_ID :', result[8], '\n'
                #     '        OTHER_SYMBOL :', ', '.join([str(elem)[2:-3] for elem in other_symbol]), '\n'
                # )
                
                each_result = [result[0],result[1],int(result[2]),result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
                Index = Index + 1
                listResult_NFD.append(each_result)

        database.CloseDatabase(conn)

        return listResult_FD, listResult_NFD

if __name__ == "__main__":
    searchFunction = Search()
    searchFunction.SearchData()