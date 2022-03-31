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

        # 0 equal
        # 1 less than
        # 2 more than
        # 3 between
        self.Distance = []
        # Example Distance = [ [ [2, 36000, 'upstream'], [3, 300000, 400000, 'downstream'] ], [ [2, 140000, 'upstream'], [3, 170000, 171000, 'downstream'] ] ]

        # All
        # upstream
        # downstream
        # intron
        self.Relationship = []
        # Example Relationship = [ ['upstream', 'downstream'], ['upstream', 'intron'] ]

        # 0 stand alone
        # 1 Group
        self.StatusRelationship = 0

        self.Relationship_Distance = []
        # [['upstream', 2500.0], ['downstream', 2500.0], 'intron', 'synon']

        # All
        # T1D
        # T2D
        # \/
        # RA
        self.Disease = ['T1D']
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
        self.source_website = 4

        self.database = Database()
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

    def Add_Relationship_Distance(self, newData):
        self.Relationship_Distance = newData
        return

    def ChangeStatus_Relationship(self, newData):
        self.StatusRelationship = newData
        return

    def Add_Disease(self, newData):
        self.Disease = newData
        return

    def ChangeStatus_Disease(self, newData):
        self.StatusDisease = newData
        return

    def Add_source_website(self, newData):
        self.source_website = newData
        return


    def CreateFormatStrings_RSID_ProbeSetID(self, status, InputRSID=[], InputProbeSetID=[]):
        FormatStrings_RSID_ProbeSetID = ''
        listRSID = []
        listProbeSetID = []

        if (status == 0): 
            listRSID = self.RS_ID
            listProbeSetID = self.ProbeSet_ID
        else: 
            listRSID = InputRSID
            listProbeSetID = InputProbeSetID


        if ( len(listRSID) == 0 ) and ( len(listProbeSetID) == 0 ):
            FormatStrings_RSID_ProbeSetID = ''

        elif ( len(listRSID) == 1 ) and ( len(listProbeSetID) == 0 ):
            FormatStrings_RSID_ProbeSetID = "snp.RS_ID = '" + str(listRSID[0]) + "'"
        
        elif ( len(listRSID) == 0 ) and ( len(listProbeSetID) == 1 ):
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(listProbeSetID[0]) + "'"
        
        elif ( len(listRSID) == 1 ) and ( len(listProbeSetID) == 1 ):
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(listProbeSetID[0]) + "' OR snp.RS_ID = '" + str(self.RS_ID[0]) + "'"

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

        if ( len(self.Chromosome) == 0 ) or (0 in self.Chromosome):
           return FormatStrings_Chromosome

        else:
            if len(self.Chromosome) > 1:
                listChromosome = ", ".join([ ( "'" + str(Each_Chromosome) + "'" ) for Each_Chromosome in self.Chromosome])
                FormatStrings_Chromosome = 'and snp.CHROMOSOME IN (' + listChromosome + ')'

            elif len(self.Chromosome) == 1:
                FormatStrings_Chromosome = "and snp.CHROMOSOME = '" + str(self.Chromosome[0]) + "'"

        return FormatStrings_Chromosome

    def CreateFormatStrings_GeneShip(self):
        if self.Geneship == 0:
            return ''
        elif self.Geneship == 1:
            return 'and snp.SOURCE_GENECHIP = "Nsp"'
        elif self.Geneship == 2:
            return 'and snp.SOURCE_GENECHIP = "Sty"'

    def CreateFormatStrings_Position(self):
        FormatStrings_Position = ''

        list_FormatStrings_Position = ['', '', '', '']
        listPosition_0 = []
        listPosition_1 = []
        listPosition_2 = []
        listPosition_3 = []

        if ( len(self.Position) > 0):
            for condition in self.Position:
                if (condition[0] == 0): listPosition_0.append(str(condition[1]))
                elif (condition[0] == 1): listPosition_1.append(str(condition[1]))
                elif (condition[0] == 2): listPosition_2.append(str(condition[1]))
                elif (condition[0] == 3): listPosition_3.append([str(condition[1]), str(condition[2])])

        if (len(listPosition_0) > 0):
            if len(listPosition_0) == 1:
                list_FormatStrings_Position[0] = 'snp.POSITION = ' + str(listPosition_0[0]) + ' '
            else:
                listPosition_0 = ", ".join( [(str(Each_Position)) for Each_Position in listPosition_0])
                list_FormatStrings_Position[0] = 'snp.POSITION IN (' + listPosition_0 + ' ) '

        if (len(listPosition_1) > 0):
            list_FormatStrings_Position[1] = " or ".join( ['snp.POSITION < ' + (str(Each_Range) ) for Each_Range in listPosition_1])
            print(list_FormatStrings_Position[1])

        if (len(listPosition_2) > 0):
            list_FormatStrings_Position[2] = " or ".join( ['snp.POSITION > ' + (str(Each_Range) ) for Each_Range in listPosition_2])
            print(list_FormatStrings_Position[2])

        if (len(listPosition_3) > 0):
            list_FormatStrings_Position[3] = " or ".join( ['( snp.POSITION between ' + (str(Each_Range[0])) + ' AND ' + (str(Each_Range[1])) + ' )' for Each_Range in listPosition_3])
            print(list_FormatStrings_Position[3])

        FormatStrings_Position = " or ".join( [ (str(Each_FormatStrings_Position) ) for Each_FormatStrings_Position in list_FormatStrings_Position if Each_FormatStrings_Position != '' ])

        if (len(FormatStrings_Position) != 0):
            FormatStrings_Position = " and ( " + FormatStrings_Position + " ) "

        return FormatStrings_Position

    def CreateFormatStrings_Distance(self):
        FormatStrings_Distance = ''

        if ( len(self.Distance) == 0):
            return FormatStrings_Distance
        
        else:
            listFormatString = []
            FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(0)

            print('FormatStrings_RSID_ProbeSetID :', FormatStrings_RSID_ProbeSetID)

            for Each_Group in self.Distance:

                listDistance = []
                listRelationship = ", ".join( [ ( "'" + str(Each_Relationship[2]) + "'" ) for Each_Relationship in Each_Group if Each_Relationship[0] != 3])
                if (len(Each_Group) > 1):
                    listRelationship = listRelationship + ", ".join( [ ( "'" + str(Each_Relationship[3]) + "'" ) for Each_Relationship in Each_Group if Each_Relationship[0] == 3])

                for condition in Each_Group:
                    if (condition[0] == 0): listDistance.append( str(" ( " + "( gene_detail.DISTANCE = " + str(condition[1]) + " ) AND ( " + "RELATIONSHIP = '" + str(condition[2]) + "' ) " + " ) ") )
                    elif (condition[0] == 1): listDistance.append( str(" ( " + "( gene_detail.DISTANCE < " + str(condition[1]) + " ) AND ( " + "RELATIONSHIP = '" + str(condition[2]) + "' ) " + " ) ") )
                    elif (condition[0] == 2): listDistance.append( str(" ( " + "( gene_detail.DISTANCE > " + str(condition[1]) + " ) AND ( " + "RELATIONSHIP = '" + str(condition[2]) + "' ) " + " ) ") )
                    elif (condition[0] == 3): listDistance.append( str(" ( " + "( gene_detail.DISTANCE BETWEEN " + str(condition[1]) + " AND " + str(condition[2]) + " ) AND ( " + "RELATIONSHIP = '" + str(condition[3]) + "' ) " + " ) ") )

                FormatStrings_GroupDistance = " or ".join( [ (str(Each_listDistance) ) for Each_listDistance in listDistance if Each_listDistance != '' ])

                FormatiString = 'gene_detail.RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE RS_ID IN ( SELECT gene_detail.RS_ID FROM ( ( snp INNER JOIN gene_snp ON gene_snp.RS_ID = snp.RS_ID ) INNER JOIN gene_detail ON gene_detail.RS_ID = gene_snp.RS_ID AND gene_detail.GENE_ID = gene_snp.GENE_ID) WHERE ' + FormatStrings_RSID_ProbeSetID + ' GROUP BY gene_detail.RS_ID HAVING COUNT(*) > ' + str(len(Each_Group) - 1) + ' ) AND RELATIONSHIP IN (' + str(listRelationship) + ') AND (' + FormatStrings_GroupDistance + ') GROUP BY RS_ID HAVING COUNT(distinct RELATIONSHIP) = ' + str(len(Each_Group)) + ')'

                listFormatString.append( FormatiString )

            FormatStrings_Distance = " and ( " + " or ".join( [ (str(Each_FormatString) ) for Each_FormatString in listFormatString if Each_FormatString != '' ]) + " ) "

        return FormatStrings_Distance

    def CreateFormatStrings_Relationship(self):
        FormatStrings_Relationship = ''
        
        if len(self.Relationship) == 0:
           return FormatStrings_Relationship

        else:
            if (self.StatusRelationship == 0):            

                if len(self.Relationship) > 1:
                    listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in self.Relationship])
                    FormatStrings_Relationship = 'and gene_detail.RELATIONSHIP IN (' + listRelationship + ')'

                elif len(self.Relationship) == 1:
                    FormatStrings_Relationship = "and gene_detail.RELATIONSHIP = '" + str(self.Relationship[0]) + "'"

            elif (self.StatusRelationship == 1):
                listFormatString = []
                FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(0)

                for Each_Group in self.Relationship:
                    listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in Each_Group])
                    listFormatString.append( 'gene_detail.RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE ' + FormatStrings_RSID_ProbeSetID + ' GROUP BY RS_ID HAVING COUNT(*) > ' + str(len(Each_Group) - 1) + ' ) AND RELATIONSHIP IN (' + str(listRelationship) + ') GROUP BY RS_ID HAVING COUNT(distinct RELATIONSHIP) = ' + str(len(Each_Group)) + ')' )

                FormatStrings_Relationship = " and ( " + ( " OR ".join( [ ( str(Each_String) ) for Each_String in listFormatString]) ) + " ) "

        return FormatStrings_Relationship

    def CreateFormatStrings_Relationship_Distance(self):
        FormatStrings_Relationship_Distance = ''

        if len(self.Relationship_Distance) == 0:
           return FormatStrings_Relationship_Distance
        else:
            FormatStrings_GroupDistance = ''
            listRelationship = []
            listDistance = []
            for Each_Group in self.Relationship_Distance:
                if type(Each_Group) == str:
                    listRelationship.append(str(Each_Group))
                elif type(Each_Group) == list:  
                    listRelationship.append(Each_Group[0])
                    listDistance.append( str(" ( " + "( gene_detail.DISTANCE = " + str(Each_Group[1]) + " ) AND ( " + "RELATIONSHIP = '" + str(Each_Group[0]) + "' ) " + " ) ") )

            if listDistance != []: FormatStrings_GroupDistance = " and ( " + " or ".join( [ (str(Each_listDistance) ) for Each_listDistance in listDistance if Each_listDistance != '' ]) + " ) "

            if len(listRelationship) == 1:
                FormatStrings_Relationship = "and gene_detail.RELATIONSHIP = '" + str(listRelationship[0]) + "'"
            else:
                listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in listRelationship])
                FormatStrings_Relationship = 'and gene_detail.RELATIONSHIP IN (' + listRelationship + ')'

            FormatStrings_Relationship_Distance = FormatStrings_GroupDistance + FormatStrings_Relationship


        return FormatStrings_Relationship_Distance

    def CreateFormatStrings_Disease(self):
        FormatStrings_Disease = ''

        if len(self.Disease) == 0:
            return FormatStrings_Disease
        else:
            if (self.StatusDisease == 0):

                if len(self.Disease) == 1:
                    FormatStrings_Disease = "and disease.DISEASE_ABBREVIATION = '" + str(self.Disease[0]) + "'"

                elif len(self.Disease) > 1:
                    listDisease = ", ".join( [("'" + str(Each_Disease) + "'") for Each_Disease in self.Disease])
                    FormatStrings_Disease = 'and disease.DISEASE_ABBREVIATION IN (' + listDisease + ')'

            # elif (self.StatusDisease == 1):
            #     listFormatString = []

            #     for Each_Group in self.Disease:
            #         listDisease = ", ".join( [ ( str( DiseaseEnum[str(Each_Disease)].value ) ) for Each_Disease in Each_Group] )
            #         listFormatString.append( 'matching_snp_disease.RS_ID IN ( SELECT RS_ID FROM matching_snp_disease WHERE RS_ID IN ( SELECT RS_ID FROM matching_snp_disease GROUP BY RS_ID HAVING COUNT(*) = ' + str(len(Each_Group)) + ' ) AND DISEASE_ID IN (' + str(listDisease) + ') GROUP BY RS_ID HAVING COUNT(distinct DISEASE_ID) = ' + str(len(Each_Group)) + ')' )

            #     FormatStrings_Disease = " and ( " + ( " OR ".join( [ ( str(Each_String) ) for Each_String in listFormatString]) ) + " ) "
            
            elif (self.StatusDisease == 99):
                return FormatStrings_Disease
                

        return FormatStrings_Disease

    def CreateFormatStrings_Source_Website(self):
        listSqlCommandDisease = []
        FormatStrings_Source_Website = ''
        searchWhere = ''
        countMatch = ''

        if self.source_website == 0:
            return FormatStrings_Source_Website
        elif self.source_website == 1:
            searchWhere = " MatchBy = 'huge' "
            countMatch = '1'
        elif self.source_website == 2:
            searchWhere = " MatchBy = 'kegg' "
            countMatch = '1'
        elif self.source_website == 3:
            searchWhere = " MatchBy LIKE '%Pathway%' "
            countMatch = '1'
        elif self.source_website == 4:
            searchWhere = " MatchBy in ('kegg', 'huge') "
            countMatch = '2'
        elif self.source_website == 5:
            searchWhere = " ( MatchBy LIKE '%Pathway%' or MatchBy = 'huge' ) "
            countMatch = '2'
        elif self.source_website == 6:
            searchWhere = " ( MatchBy LIKE '%Pathway%' or MatchBy = 'kegg' ) "
            countMatch = '2'
        elif self.source_website == 7:
            searchWhere = " ( MatchBy LIKE '%Pathway%' or MatchBy in ('kegg', 'huge') ) "
            countMatch = '3'

        for eachDisease in self.Disease:
            diseaseID = DiseaseEnum[str(eachDisease)].value
            listSqlCommandDisease.append(" ( matching_snp_disease.RS_ID in ( select RS_ID FROM matching_snp_disease WHERE ( " + str(searchWhere) + " and DISEASE_ID = " + str(diseaseID) + " ) GROUP BY RS_ID HAVING COUNT(MatchBy) = " + countMatch + " ) AND matching_snp_disease.RS_ID in ( select RS_ID FROM matching_snp_disease WHERE ( DISEASE_ID = " + str(diseaseID) + " ) GROUP BY RS_ID HAVING COUNT(MatchBy) = " + str(countMatch) + " ) AND matching_snp_disease.DISEASE_ID = " + str(diseaseID) + " ) ")

        FormatStrings_Source_Website = " and ( " + (" or ".join( [ eachCommand for eachCommand in listSqlCommandDisease] )) + " ) "
        return FormatStrings_Source_Website

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


    def ExtractRelatedGeneID(self, RSID, ProbeSetID, listUniqueRelateRSID, listUniqueRelateProbeSetID):
        if RSID not in listUniqueRelateRSID:
            listUniqueRelateRSID.append(RSID)

        if ProbeSetID not in listUniqueRelateProbeSetID:
            listUniqueRelateProbeSetID.append(ProbeSetID)

        return listUniqueRelateRSID, listUniqueRelateProbeSetID

    def ExtractUnrelatedGeneID(self, listUniqueRSID, listUniqueProbeSetID):
        listOfUniqueUnrelated_RSID = []
        listOfUniqueUnrelated_ProbeSetID = []

        for eachOriginalFoundRSID in self.RS_ID:
            if eachOriginalFoundRSID not in listUniqueRSID:
                listOfUniqueUnrelated_RSID.append(eachOriginalFoundRSID)
            
        for eachOriginalFoundProbeSetID in self.ProbeSet_ID:
            if eachOriginalFoundProbeSetID not in listUniqueProbeSetID:
                listOfUniqueUnrelated_ProbeSetID.append(eachOriginalFoundProbeSetID)

        return listOfUniqueUnrelated_RSID, listOfUniqueUnrelated_ProbeSetID


    def SearchData(self):
        database = Database()
        conn = database.ConnectDatabase()

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
        # FormatStrings_Distance = self.CreateFormatStrings_Distance()
        # FormatStrings_Relationship = self.CreateFormatStrings_Relationship()
        FormatStrings_Relationship_Distance = self.CreateFormatStrings_Relationship_Distance()
        FormatStrings_Disease = self.CreateFormatStrings_Disease()
        FormatStrings_GeneShip = self.CreateFormatStrings_GeneShip()
        FormatStrings_Source_Website = self.CreateFormatStrings_Source_Website()

        # ------------------------------ Step 1 ------------------------------

        SQLCommand_Relate_InDisease = self.SQLCommand_Relate_InDisease(FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_Disease, FormatStrings_GeneShip, FormatStrings_Source_Website)
        # print('SQLCommand_Relate_InDisease :', SQLCommand_Relate_InDisease)

        results_Relate_InDisease = set( database.CreateTask(conn, SQLCommand_Relate_InDisease, ()) )
        
        if ( results_Relate_InDisease != [] ):
            # print('\n List gene has found on disease \n')

            Index = 0
            for result in results_Relate_InDisease:
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

                listUniqueRelated_RSID, listUniqueRelated_ProbeSetID = self.ExtractRelatedGeneID(result[0], result[1], listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)

                each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]

                Index = Index + 1
                Result_Relate_InDisease.append(each_result)

        # ------------------------------ Step 1 ------------------------------



        # ------------------------------ Step 2 ------------------------------

        SQLCommand_Relate_NotInDisease = self.SQLCommand_Relate_NotInDisease(FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Relationship_Distance, FormatStrings_GeneShip)
        # print('SQLCommand_Relate_NotInDisease :', SQLCommand_Relate_NotInDisease)

        results_Relate_NotInDisease = set( database.CreateTask(conn, SQLCommand_Relate_NotInDisease, ()) )

        if ( results_Relate_NotInDisease != [] and FormatStrings_Disease == '' ):
            # print('\n List gene has not found on disease \n')

            Index = 0
            for result in results_Relate_NotInDisease:
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

                listUniqueRelated_RSID, listUniqueRelated_ProbeSetID = self.ExtractRelatedGeneID(result[0], result[1], listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)

                each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
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

            if ( results_Unrelate_InDisease != [] ):
                # print('\n List gene has not found on disease \n')

                Index = 0
                for result in results_Unrelate_InDisease:
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

                    each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]
                    Index = Index + 1
                    Result_Unrelate_InDisease.append(each_result)

        # ------------------------------ Step 3 ------------------------------


        # ------------------------------ Step 4 ------------------------------

        if (FormatStrings_RSID_ProbeSetID != ''):
            SQLCommand_Unrelate_NotInDisease = self.SQLCommand_Unrelate_NotInDisease(FormatStrings_RSID_ProbeSetID)
            # print('SQLCommand_Unrelate_NotInDisease :', SQLCommand_Unrelate_NotInDisease)

            results_Unrelate_NotInDisease = set( database.CreateTask(conn, SQLCommand_Unrelate_NotInDisease, ()) )

            if ( results_Unrelate_NotInDisease != [] ):
                # print('\n List gene has not found on disease \n')

                Index = 0
                for result in results_Unrelate_NotInDisease:
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

                    each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
                    Index = Index + 1
                    Result_Unrelate_NotInDisease.append(each_result)

        # ------------------------------ Step 4 ------------------------------

        database.CloseDatabase(conn)

        return Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease

if __name__ == "__main__":
    searchFunction = Search()
    searchFunction.SearchData()



