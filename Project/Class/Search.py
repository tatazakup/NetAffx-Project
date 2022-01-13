from Initialization import Database

class Search(Database):
    def __init__(self):
        self.RS_ID = ['rs9380593']
        self.ProbeSet_ID = []
        self.GeneID = []
        self.GeneSymbol = []

        # 0 All
        # 1 Chomosome#1
        # 3 Chomosome#2
        # \/
        # 23 Chomosome#23
        self.Chromosome = [0]

        # 0 equal
        # 1 less than
        # 2 more than
        # 3 between
        self.Position = [ [3, 1000, 100000000] ]

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

        # 0 All
        # 1 T1D
        # 2 T2D
        # \/
        # 7 RA
        self.Disease = []

        # 0 All 
        # 1 Huge
        # 2 Kegg
        # 3 Pathway
        self.source_website = 3

        return

    def ImportData(self, newData):
        
        return

    def CreateFormatStrings_RSID_ProbeSetID(self):
        FormatStrings_RSID_ProbeSetID = ''

        if ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) == 0 ):
            FormatStrings_RSID_ProbeSetID = ''

        elif ( len(self.RS_ID) == 1 ) and ( len(self.ProbeSet_ID) == 0 ):
            FormatStrings_RSID_ProbeSetID = "snp.RS_ID = '" + str(self.RS_ID[0]) + "'"
        
        elif ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) == 1 ):
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(self.ProbeSet_ID[0]) + "'"

        elif ( len(self.RS_ID) != 0 ) and ( len(self.ProbeSet_ID) == 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in self.RS_ID])
            FormatStrings_RSID_ProbeSetID = '( snp.RS_ID IN (' + listRS_ID + ') )'

        elif ( len(self.RS_ID) == 0 ) and ( len(self.ProbeSet_ID) != 0 ):
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in self.ProbeSet_ID])
            FormatStrings_RSID_ProbeSetID = '( snp.PROBESET_ID IN (' + listProbeSet_ID + ') )'

        elif ( len(self.RS_ID) != 0 ) and ( len(self.ProbeSet_ID) != 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in self.RS_ID])
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in self.ProbeSet_ID])

            FormatStrings_RSID_ProbeSetID = '( snp.RS_ID IN (' + listRS_ID + ') OR snp.PROBESET_ID IN (' + listProbeSet_ID + ') )'
        return FormatStrings_RSID_ProbeSetID

    def CreateFormatStrings_GeneID(self):
        FormatStrings_GeneID = ''
        if len(self.GeneID) > 1:
            listGeneID = ", ".join([str(Each_GeneID) for Each_GeneID in self.GeneID])
            FormatStrings_GeneID = 'and gene_snp.GENE_ID IN (' + listGeneID + ')'
        elif len(self.GeneID) == 1:
            FormatStrings_GeneID = 'and gene_snp.GENE_ID = ' + str(self.GeneID[0])
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

        for condition in self.Position:
            if (condition[0] == 0):
                FormatStrings_Position = FormatStrings_Position + 'and snp.POSITION = ' + str(condition[1]) + ' '
            elif (condition[0] == 1):
                FormatStrings_Position = FormatStrings_Position + 'and snp.POSITION > ' + str(condition[1]) + ' '
            elif (condition[0] == 2):
                FormatStrings_Position = FormatStrings_Position + 'and snp.POSITION < ' + str(condition[1]) + ' '
            elif (condition[0] == 3):
                FormatStrings_Position = FormatStrings_Position + 'and snp.POSITION between ' + str(condition[1]) + ' and ' + str(condition[2]) + ' '

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
                listRelationship = ", ".join("'" + [str(Each_Relationship) + "'" for Each_Relationship in self.Relationship])
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
                listDisease = ", ".join([str(Each_Disease) for Each_Disease in self.Disease])
                FormatStrings_Disease = 'and matching_snp_disease.Disease_ID IN (' + listDisease + ')'

            elif len(self.Disease) == 1:
                FormatStrings_Disease = 'and matching_snp_disease.Disease_ID = ' + str(self.Disease[0])

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

        mysqlCommand = """
            SELECT
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
            INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID)
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

        if ( FormatStrings_RSID_ProbeSetID == ''):
            mysqlCommand = mysqlCommand.replace('and', '', 1)

        print('mysqlCommand :', mysqlCommand)

        results = set( database.CreateTask(conn, mysqlCommand, ()) )

        if ( results != [] ):
            Index = 0
            for result in results:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                print(
                    '               Index :', Index, '\n'
                    '                RSID :', result[0], '\n'
                    '         PROBESET_ID :', result[1], '\n'
                    '          CHROMOSOME :', result[2], '\n'
                    '            POSITION :', result[3], '\n'
                    '     SOURCE_GENESHIP :', result[4], '\n'
                    '        RELATIONSHIP :', result[5], '\n'
                    '            DISTANCE :', result[6], '\n'
                    '         GENE_SYMBOL :', result[7], '\n'
                    '             GENE_ID :', result[8], '\n'
                    '        OTHER_SYMBOL :', ', '.join([str(elem)[2:-3] for elem in other_symbol]), '\n'
                    '        Disease_NAME :', result[9], '\n'
                    'DISEASE_ABBREVIATION :', result[10], '\n'
                    '             MatchBy :', result[11], '\n'
                )

                Index = Index + 1

        database.CloseDatabase(conn)

        return

if __name__ == "__main__":
    searchFunction = Search()
    searchFunction.SearchData()