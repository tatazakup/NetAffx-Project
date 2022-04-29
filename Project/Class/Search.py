from ctypes.wintypes import INT
from Initialization import Database, FilePath
import pandas as pd
import enum

class DiseaseEnum(enum.Enum):
    T1D = 1
    T2D = 2
    BD = 3
    CAD = 4
    CD = 5
    HT = 6
    RA = 7

class Search(Database):
    def __init__(self):
        self.RS_ID = []
        self.ProbeSet_ID = []
        self.GeneID = []
        self.GeneSymbol = []

        # 0 All
        # 1 Chomosome# 1
        # 3 Chomosome# 2
        # \/
        # 23 Chomosome# 23
        self.Chromosome = []
        # Example Chromosome = [1, 3, 5]

        # 0 equal
        # 1 less than
        # 2 more than
        # 3 between
        self.Position = []
        # Example Position = [ [0, 3000], [1, 200], [3, 100, 300] ]

        # 0 All
        # 1 Nsp
        # 2 Sty
        self.Geneship = 0
        # Example Geneship = [1]

        self.Relationship_Distance = []
        # [['upstream', 2500.0], ['downstream', 2500.0], 'intron', 'synon']

        # All
        # T1D
        # T2D
        # \/
        # RA
        self.Disease = []
        # Example Disease = [ ['T1D], 'T2D'], ['T1D', 'RA'] ]

        # 0 stand alone
        # 1 Group
        # 99 None
        self.StatusDisease = 0

        # 0 Union 
        # 1 Huge
        # 2 Kegg
        # 3 Pathway
        # 4 Huge and kegg
        # 5 Huge and pathway
        # 6 kegg and pathway
        # 7 kegg and kegg and pathway
        self.source_website = 0

        self.database = Database()
        self.test = False
        self.advanceSearch = ''
        return

    # Initialization
    def ImportData(self, newData):
        for Each_data in newData: self.Add_RSID_PROBE_SET(Each_data)

    def Add_RSID_PROBE_SET(self, newData):
        if 'rs' in str(newData): (self.RS_ID).append(str(newData))
        elif 'SNP' in str(newData): (self.ProbeSet_ID).append(str(newData))

    def Add_GeneID(self, newData): self.GeneID = newData
    def Add_GeneSymbol(self, newData):
        if ( len(newData) == 1 ):
            if newData[0] == '': return

        self.GeneSymbol = newData

    def Add_Chromosome(self, newData): self.Chromosome = newData
    def Add_Position(self, newData): self.Position = newData
    def Add_Geneship(self, newData): self.Geneship = newData
    def Add_Relationship_Distance(self, newData): self.Relationship_Distance = newData
    def Add_Disease(self, newData): self.Disease = newData
    def Add_source_website(self, newData): self.source_website = newData
    def Add_advanceSearch(self, newData): self.advanceSearch = newData

    def ChangeStatus_Disease(self, newData): self.StatusDisease = newData
    def ChangeStatusTest(self, newStatus): self.StatusTest = newStatus

    # Create Format String Function
    def CreateFormatStrings_RSID_ProbeSetID(self, status, InputRSID=[], InputProbeSetID=[]):
        FormatStrings_RSID_ProbeSetID = ''
        listRSID = []
        listProbeSetID = []

        if (status == 0): listRSID = self.RS_ID; listProbeSetID = self.ProbeSet_ID
        else: listRSID = InputRSID; listProbeSetID = InputProbeSetID

        if ( len(listRSID) == 0 ) and ( len(listProbeSetID) == 0 ): FormatStrings_RSID_ProbeSetID = ''
        elif ( len(listRSID) == 1 ) and ( len(listProbeSetID) == 0 ): FormatStrings_RSID_ProbeSetID = "snp.RS_ID = '" + str(listRSID[0]) + "'"
        elif ( len(listRSID) == 0 ) and ( len(listProbeSetID) == 1 ): FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(listProbeSetID[0]) + "'"
        elif ( len(listRSID) == 1 ) and ( len(listProbeSetID) == 1 ): FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(listProbeSetID[0]) + "' OR snp.RS_ID = '" + str(self.RS_ID[0]) + "'"
        elif ( len(listRSID) != 0 ) and ( len(listProbeSetID) == 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in listRSID])
            FormatStrings_RSID_ProbeSetID = 'snp.RS_ID IN (' + listRS_ID + ')'
        elif ( len(listRSID) == 0 ) and ( len(listProbeSetID) != 0 ):
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in listProbeSetID])
            FormatStrings_RSID_ProbeSetID = 'snp.PROBESET_ID IN (' + listProbeSet_ID + ')'
        elif ( len(listRSID) != 0 ) and ( len(listProbeSetID) != 0 ):
            listRS_ID = ", ".join([("'" + str(Each_RS_ID) + "'") for Each_RS_ID in listRSID])
            listProbeSet_ID = ", ".join([("'" + str(Each_ProbeSet_ID) + "'") for Each_ProbeSet_ID in listProbeSetID])

            FormatStrings_RSID_ProbeSetID = '( snp.RS_ID IN (' + listRS_ID + ') OR snp.PROBESET_ID IN (' + listProbeSet_ID + ') )'

        return FormatStrings_RSID_ProbeSetID

    def CreateFormatStrings_GeneID(self):
        FormatStrings_GeneID = ''

        if len(self.GeneID) > 1:
            listGeneID = ", ".join([str(Each_GeneID) for Each_GeneID in self.GeneID])
            FormatStrings_GeneID = 'and gene_detail.GENE_ID IN (' + listGeneID + ')'
        elif len(self.GeneID) == 1: FormatStrings_GeneID = 'and gene_detail.GENE_ID = ' + str(self.GeneID[0])

        return FormatStrings_GeneID

    def CreateFormatStrings_GeneSymbol(self):
        FormatStrings_GeneSymbol = ''

        if len(self.GeneSymbol) > 1:
            listGeneSymbol = ", ".join([("'" + str(Each_GeneSymbol) + "'") for Each_GeneSymbol in self.GeneSymbol])
            FormatStrings_GeneSymbol = 'and ( other_symbol.OTHER_SYMBOL IN (' + listGeneSymbol + ') OR gene_snp.GENE_SYMBOL IN (' + listGeneSymbol + ')' + ')'
        elif len(self.GeneSymbol) == 1: FormatStrings_GeneSymbol = "and ( other_symbol.OTHER_SYMBOL = '" + str(self.GeneSymbol[0]) + "' OR gene_snp.GENE_SYMBOL = '" + str(self.GeneSymbol[0]) + "')"

        return FormatStrings_GeneSymbol

    def CreateFormatStrings_Chromosome(self):
        FormatStrings_Chromosome = ''

        print('asd')
        if ( len(self.Chromosome) == 0 ) or (0 in self.Chromosome): 
            return FormatStrings_Chromosome
        else:
            if len(self.Chromosome) > 1:
                listChromosome = ", ".join([ ( "'" + str(Each_Chromosome) + "'" ) for Each_Chromosome in self.Chromosome])
                FormatStrings_Chromosome = 'and snp.CHROMOSOME IN (' + listChromosome + ')'
            elif len(self.Chromosome) == 1: FormatStrings_Chromosome = "and snp.CHROMOSOME = '" + str(self.Chromosome[0]) + "'"

        return FormatStrings_Chromosome

    def CreateFormatStrings_GeneShip(self):
        match self.Geneship:
            case 0: return ''
            case 1: return 'and snp.SOURCE_GENECHIP = "Nsp"'
            case 2: return 'and snp.SOURCE_GENECHIP = "Sty"'

    def CreateFormatStrings_Position(self):
        FormatStrings_Position = ''

        list_FormatStrings_Position = ['', '', '', '']
        listPosition_0 = []
        listPosition_1 = []
        listPosition_2 = []
        listPosition_3 = []

        if ( len(self.Position) > 0):
            for condition in self.Position:
                match condition[0]:
                    case 0: listPosition_0.append(str(condition[1]))
                    case 1: listPosition_1.append(str(condition[1]))
                    case 2: listPosition_2.append(str(condition[1]))
                    case 3: listPosition_3.append([str(condition[1]), str(condition[2])])

        if (len(listPosition_0) > 0):
            if len(listPosition_0) == 1: list_FormatStrings_Position[0] = 'snp.POSITION = ' + str(listPosition_0[0]) + ' '
            else:
                listPosition_0 = ", ".join( [(str(Each_Position)) for Each_Position in listPosition_0])
                list_FormatStrings_Position[0] = 'snp.POSITION IN (' + listPosition_0 + ' ) '

        if (len(listPosition_1) > 0): list_FormatStrings_Position[1] = " or ".join( ['snp.POSITION < ' + (str(Each_Range) ) for Each_Range in listPosition_1])
        if (len(listPosition_2) > 0): list_FormatStrings_Position[2] = " or ".join( ['snp.POSITION > ' + (str(Each_Range) ) for Each_Range in listPosition_2])
        if (len(listPosition_3) > 0): list_FormatStrings_Position[3] = " or ".join( ['( snp.POSITION between ' + (str(Each_Range[0])) + ' AND ' + (str(Each_Range[1])) + ' )' for Each_Range in listPosition_3])

        FormatStrings_Position = " or ".join( [ (str(Each_FormatStrings_Position) ) for Each_FormatStrings_Position in list_FormatStrings_Position if Each_FormatStrings_Position != '' ])

        if (len(FormatStrings_Position) != 0): FormatStrings_Position = " and ( " + FormatStrings_Position + " ) "

        return FormatStrings_Position

    def CreateFormatStrings_Relationship_Distance(self):
        FormatStrings_Relationship_Distance = ''

        if len(self.Relationship_Distance) == 0: return FormatStrings_Relationship_Distance

        else:
            FormatStrings_GroupDistance = ''
            listRelationship = []
            listDistance = []
            for Each_Group in self.Relationship_Distance:

                if type(Each_Group) == str: listRelationship.append(str(Each_Group))
                elif type(Each_Group) == list:  
                    listRelationship.append(Each_Group[0])
                    listDistance.append( str(" ( " + "( gene_detail.DISTANCE <= " + str(Each_Group[1]) + " ) AND ( " + "RELATIONSHIP = '" + str(Each_Group[0]) + "' ) " + " ) ") )

            if listDistance != []: FormatStrings_GroupDistance = " and ( " + " or ".join( [ (str(Each_listDistance) ) for Each_listDistance in listDistance if Each_listDistance != '' ]) + " ) "

            if len(listRelationship) == 1: FormatStrings_Relationship = "and gene_detail.RELATIONSHIP = '" + str(listRelationship[0]) + "'"
            else:
                listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in listRelationship])
                FormatStrings_Relationship = 'and gene_detail.RELATIONSHIP IN (' + listRelationship + ')'

            FormatStrings_Relationship_Distance = FormatStrings_GroupDistance + FormatStrings_Relationship


        return FormatStrings_Relationship_Distance

    def CreateFormatStrings_Disease(self):
        FormatStrings_Disease = ''

        if len(self.Disease) == 0: return FormatStrings_Disease
        else:
            if (self.StatusDisease == 0):

                if len(self.Disease) == 1: FormatStrings_Disease = "and disease.DISEASE_ABBREVIATION = '" + str(self.Disease[0]) + "'"
                elif len(self.Disease) > 1:
                    listDisease = ", ".join( [("'" + str(Each_Disease) + "'") for Each_Disease in self.Disease])
                    FormatStrings_Disease = 'and disease.DISEASE_ABBREVIATION IN (' + listDisease + ')'
            
            elif (self.StatusDisease == 99): return FormatStrings_Disease
                
        return FormatStrings_Disease

    def CreateFormatStrings_Source_Website(self):
        listSqlCommandDisease = []
        FormatStrings_Source_Website = ''
        searchWhere = ''
        countMatch = ''

        match self.source_website:
            case 0: return FormatStrings_Source_Website
            case 1: countMatch = '1'; searchWhere = " matching_snp_disease.MatchBy = 'huge' "
            case 2: countMatch = '1'; searchWhere = " matching_snp_disease.MatchBy = 'kegg' "
            case 3: countMatch = '1'; searchWhere = " matching_snp_disease.MatchBy LIKE '%Pathway%' "
            case 4: countMatch = '2'; searchWhere = " matching_snp_disease.MatchBy in ('kegg', 'huge') "
            case 5: countMatch = '2'; searchWhere = " ( matching_snp_disease.MatchBy LIKE '%Pathway%' or matching_snp_disease.MatchBy = 'huge' ) "
            case 6: countMatch = '2'; searchWhere = " ( matching_snp_disease.MatchBy LIKE '%Pathway%' or matching_snp_disease.MatchBy = 'kegg' ) "
            case 7: countMatch = '3'; searchWhere = " ( matching_snp_disease.MatchBy LIKE '%Pathway%' or matching_snp_disease.MatchBy in ('kegg', 'huge') ) "

        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(0)

        for eachDisease in self.Disease:
            diseaseID = DiseaseEnum[str(eachDisease)].value
            listSqlCommandDisease.append(" ( matching_snp_disease.RS_ID in ( select RS_ID FROM matching_snp_disease WHERE ( " + str(searchWhere) + " and DISEASE_ID = " + str(diseaseID) + " ) GROUP BY RS_ID HAVING COUNT(MatchBy) >= " + countMatch + " ) AND matching_snp_disease.GENE_ID in ( select GENE_ID FROM matching_snp_disease INNER JOIN snp ON snp.RS_ID = matching_snp_disease.RS_ID WHERE ( " + FormatStrings_RSID_ProbeSetID + "  and DISEASE_ID = " + str(diseaseID) + " ) GROUP BY GENE_ID HAVING COUNT(MatchBy) = " + str(countMatch) + " ) AND matching_snp_disease.DISEASE_ID = " + str(diseaseID) + " AND " + str(searchWhere) + " ) ")

        FormatStrings_Source_Website = " and ( " + (" or ".join( [ eachCommand for eachCommand in listSqlCommandDisease] )) + " ) "
        return FormatStrings_Source_Website


    # SQL Function
    def SQLCommand_Relate_InDisease(self, FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_Disease, FormatStrings_GeneShip, FormatStrings_Source_Website):
        mysqlCommand_FoundInDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENECHIP,

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
            LEFT JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            INNER JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID AND matching_snp_disease.GENE_ID = gene_snp.GENE_ID )
            INNER JOIN disease ON disease.DISEASE_ID = matching_snp_disease.DISEASE_ID  )
            WHERE %s
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
            FormatStrings_RSID_ProbeSetID,
            FormatStrings_GeneID,
            FormatStrings_GeneSymbol,
            FormatStrings_Chromosome,
            FormatStrings_Position,
            FormatStrings_Relationship_Distance,
            FormatStrings_Disease,
            FormatStrings_GeneShip,
            FormatStrings_Source_Website
        )

        return mysqlCommand_FoundInDisease
    
    def SQLCommand_Relate_NotInDisease(self, FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_GeneShip):
        mysqlCommand_NotFoundInDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENECHIP,

                gene_detail.RELATIONSHIP, 
                gene_detail.DISTANCE,

                gene_snp.GENE_SYMBOL,
                gene_snp.GENE_ID
            FROM ( ( ( ( ( snp
            INNER JOIN gene_snp ON gene_snp.RS_ID = snp.RS_ID )
            INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID AND gene_detail.GENE_ID = gene_snp.GENE_ID)
            INNER JOIN ncbi ON ncbi.GENE_ID = gene_snp.GENE_ID )
            LEFT JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            LEFT JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID AND matching_snp_disease.GENE_ID = gene_snp.GENE_ID )
            WHERE matching_snp_disease.RS_ID IS NULL
            and %s
            %s
            %s
            %s
            %s
            %s
            %s
            ORDER BY snp.CHROMOSOME ASC, snp.POSITION ASC;
        """ % (
            FormatStrings_RSID_ProbeSetID,
            FormatStrings_GeneID,
            FormatStrings_GeneSymbol,
            FormatStrings_Chromosome,
            FormatStrings_Position,
            FormatStrings_Relationship_Distance,
            FormatStrings_GeneShip
        )

        return mysqlCommand_NotFoundInDisease

    def SQLCommand_Unrelate_InDisease(self, FormatStrings_RSID_ProbeSetID):
        mysqlCommand_FoundInDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENECHIP,

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
            LEFT JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            INNER JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID )
            INNER JOIN disease ON disease.DISEASE_ID = matching_snp_disease.DISEASE_ID )
            WHERE %s
            ORDER BY snp.CHROMOSOME ASC, snp.POSITION ASC;
        """ % (
            FormatStrings_RSID_ProbeSetID
        )

        return mysqlCommand_FoundInDisease

    def SQLCommand_Unrelate_NotInDisease(self, FormatStrings_RSID_ProbeSetID):
        mysqlCommand_NotFoundInDisease = """
            SELECT DISTINCT
                snp.RS_ID,
                snp.PROBESET_ID,
                snp.CHROMOSOME,
                snp.POSITION,
                snp.SOURCE_GENECHIP,

                gene_detail.RELATIONSHIP, 
                gene_detail.DISTANCE,

                gene_snp.GENE_SYMBOL,
                gene_snp.GENE_ID
            FROM ( ( ( ( ( snp
            INNER JOIN gene_snp ON gene_snp.RS_ID = snp.RS_ID )
            INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID AND gene_detail.GENE_ID = gene_snp.GENE_ID)
            INNER JOIN ncbi ON ncbi.GENE_ID = gene_snp.GENE_ID )
            LEFT JOIN other_symbol ON other_symbol.GENE_ID = ncbi.GENE_ID )
            LEFT JOIN matching_snp_disease ON matching_snp_disease.RS_ID = snp.RS_ID )
            WHERE matching_snp_disease.RS_ID IS NULL
            and %s
            ORDER BY snp.CHROMOSOME ASC, snp.POSITION ASC;
        """ % (
            FormatStrings_RSID_ProbeSetID
        )

        return mysqlCommand_NotFoundInDisease


    # Extract Function
    def ExtractRelatedGeneID(self, RSID, ProbeSetID, listUniqueRelateRSID, listUniqueRelateProbeSetID):
        if RSID not in listUniqueRelateRSID: listUniqueRelateRSID.append(RSID)
        if ProbeSetID not in listUniqueRelateProbeSetID: listUniqueRelateProbeSetID.append(ProbeSetID)

        return listUniqueRelateRSID, listUniqueRelateProbeSetID

    def ExtractUnrelatedGeneID(self, listUniqueRSID, listUniqueProbeSetID):
        listOfUniqueUnrelated_RSID = []
        listOfUniqueUnrelated_ProbeSetID = []

        for eachOriginalFoundRSID in self.RS_ID:
            if eachOriginalFoundRSID not in listUniqueRSID: listOfUniqueUnrelated_RSID.append(eachOriginalFoundRSID)
            
        for eachOriginalFoundProbeSetID in self.ProbeSet_ID:
            if eachOriginalFoundProbeSetID not in listUniqueProbeSetID: listOfUniqueUnrelated_ProbeSetID.append(eachOriginalFoundProbeSetID)

        return listOfUniqueUnrelated_RSID, listOfUniqueUnrelated_ProbeSetID


    # Search Function
    def SearchData(self):
        database = Database()
        conn = database.ConnectDatabase()

        SQLCommand_Relate_InDisease = ''
        SQLCommand_Relate_NotInDisease = ''
        SQLCommand_Unrelate_InDisease = ''
        SQLCommand_Unrelate_NotInDisease = ''

        Result_Relate_InDisease = []
        Result_Relate_NotInDisease = []
        Result_Unrelate_InDisease = []
        Result_Unrelate_NotInDisease = []

        listUniqueRelated_RSID = []
        listUniqueRelated_ProbeSetID = []
        listUniqueUnrelated_RSID = []
        listUniqueUnrelated_ProbeSetID = []

        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(0)
        FormatStrings_GeneID = self.CreateFormatStrings_GeneID()
        FormatStrings_GeneSymbol = self.CreateFormatStrings_GeneSymbol()
        FormatStrings_Chromosome = self.CreateFormatStrings_Chromosome()
        FormatStrings_Position = self.CreateFormatStrings_Position()
        FormatStrings_Relationship_Distance = self.CreateFormatStrings_Relationship_Distance()
        FormatStrings_Disease = self.CreateFormatStrings_Disease()
        FormatStrings_GeneShip = self.CreateFormatStrings_GeneShip()
        FormatStrings_Source_Website = self.CreateFormatStrings_Source_Website()

        # ------------------------------ Step 1 ------------------------------

        SQLCommand_Relate_InDisease = self.SQLCommand_Relate_InDisease(FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_Disease, FormatStrings_GeneShip, FormatStrings_Source_Website)
        print('SQLCommand_Relate_InDisease :', SQLCommand_Relate_InDisease)
        results_Relate_InDisease = set( database.CreateTask(conn, SQLCommand_Relate_InDisease, ()) )
        
        print('\n List gene has found on disease \n')
        if ( results_Relate_InDisease != [] ):
            Index = 0

            for result in results_Relate_InDisease:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                listUniqueRelated_RSID, listUniqueRelated_ProbeSetID = self.ExtractRelatedGeneID(result[0], result[1], listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)
                
                if (self.test == False): each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]
                else: each_result = [result[0],result[1],str(result[2]),result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]

                Index = Index + 1
                Result_Relate_InDisease.append(each_result)

        # ------------------------------ Step 1 ------------------------------



        # ------------------------------ Step 2 ------------------------------

        if ( FormatStrings_Disease == '' ):
            SQLCommand_Relate_NotInDisease = self.SQLCommand_Relate_NotInDisease(FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_GeneShip)
            # print('SQLCommand_Relate_NotInDisease :', SQLCommand_Relate_NotInDisease)
            results_Relate_NotInDisease = set( database.CreateTask(conn, SQLCommand_Relate_NotInDisease, ()) )
            print('\n List gene has not found on disease \n')

            if ( results_Relate_NotInDisease != [] ):
                Index = 0

                for result in results_Relate_NotInDisease:
                    mysqlCommand = """ 
                        SELECT
                            OTHER_SYMBOL
                        FROM other_symbol
                        WHERE GENE_ID = %s
                    """

                    other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))
                    listUniqueRelated_RSID, listUniqueRelated_ProbeSetID = self.ExtractRelatedGeneID(result[0], result[1], listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)

                    if (self.test == False): each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
                    else: each_result = [result[0],result[1],(result[2]),str(result[3]),result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]

                    Index = Index + 1
                    Result_Relate_NotInDisease.append(each_result)

        # ------------------------------ Step 2 ------------------------------



        # ----------------------- Before start Step 3 ------------------------

        listUniqueUnrelated_RSID, listUniqueUnrelated_ProbeSetID = self.ExtractUnrelatedGeneID(listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)
        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(1, listUniqueUnrelated_RSID, listUniqueUnrelated_ProbeSetID)

        # ----------------------- Before start Step 3 ------------------------



        # ------------------------------ Step 3 ------------------------------
        
        if (FormatStrings_RSID_ProbeSetID != ''):
            SQLCommand_Unrelate_InDisease = self.SQLCommand_Unrelate_InDisease(FormatStrings_RSID_ProbeSetID)
            # print('SQLCommand_Unrelate_InDisease :', SQLCommand_Unrelate_InDisease)
            results_Unrelate_InDisease = set( database.CreateTask(conn, SQLCommand_Unrelate_InDisease, ()) )
            print('\n List gene has not found on disease \n')

            if ( results_Unrelate_InDisease != [] ):
                Index = 0

                for result in results_Unrelate_InDisease:
                    mysqlCommand = """ 
                        SELECT
                            OTHER_SYMBOL
                        FROM other_symbol
                        WHERE GENE_ID = %s
                    """

                    other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                    if (self.test == False): each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]
                    else: each_result = [result[0],result[1],str(result[2]),result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]

                    Index = Index + 1
                    Result_Unrelate_InDisease.append(each_result)

        # ------------------------------ Step 3 ------------------------------



        # ------------------------------ Step 4 ------------------------------
        
        if (FormatStrings_RSID_ProbeSetID != ''):
            SQLCommand_Unrelate_NotInDisease = self.SQLCommand_Unrelate_NotInDisease(FormatStrings_RSID_ProbeSetID)
            # print('SQLCommand_Unrelate_NotInDisease :', SQLCommand_Unrelate_NotInDisease)
            results_Unrelate_NotInDisease = set( database.CreateTask(conn, SQLCommand_Unrelate_NotInDisease, ()) )
            print('\n List gene has not found on disease \n')

            if ( results_Unrelate_NotInDisease != [] ):
                Index = 0

                for result in results_Unrelate_NotInDisease:
                    mysqlCommand = """ 
                        SELECT
                            OTHER_SYMBOL
                        FROM other_symbol
                        WHERE GENE_ID = %s
                    """

                    other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                    if (self.test == False): each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
                    else: each_result = [result[0],result[1],str(result[2]),result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]

                    Index = Index + 1
                    Result_Unrelate_NotInDisease.append(each_result)

        # ------------------------------ Step 4 ------------------------------

        database.CloseDatabase(conn)

        return Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease

    def AdvanceSearchData(self):
        database = Database()
        conn = database.ConnectDatabase()

        results = set( database.CreateTask(conn, self.advanceSearch, ()) )

        database.CloseDatabase(conn)
        return results

if __name__ == "__main__":
    searchFunction = Search()
    searchFunction.SearchData()



