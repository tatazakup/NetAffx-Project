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
        # self.RS_ID = [
        #     'rs1748035', 'rs4920334', 'rs4912122', 'rs12117895', 'rs215773', 'rs3103778', 'rs736861', 'rs869988', 'rs207190', 'rs4276942', 'rs10889189', 'rs2989476', 'rs11207909', 'rs6691577', 'rs7546928', 'rs2132999', 'rs1896250', 'rs1782127', 'rs4658112', 'rs396954', 'rs1361461', 'rs11185337', 'rs12759387', 'rs4378202', 'rs12125340', 'rs10793652', 'rs11240054', 'rs4845390', 'rs4845690', 'rs7534239', 'rs12129036', 'rs2840584', 'rs285482', 'rs7519141', 'rs4657694', 'rs2213736', 'rs1385542', 'rs12401659', 'rs6425425', 'rs4113814', 'rs680638', 'rs951366', 'rs926576', 'rs4628571', 'rs6665548', 'rs6604643', 'rs6679942', 'rs6741819', 'rs4027132', 'rs12472797', 'rs737565', 'rs7562696', 'rs10187657', 'rs3755221', 'rs848531', 'rs11676056', 'rs11687654', 'rs6705537', 'rs7571842', 'rs6730095', 
        #     'rs2678381', 'rs7573844', 'rs7570682', 'rs920217', 'rs11123306', 'rs1375144', 'rs2418876', 'rs6750543', 'rs10928826', 'rs787433', 'rs4641882', 'rs17328734', 'rs6755520', 'rs2592941', 'rs10166245', 'rs1840111', 'rs1344706', 'rs4666691', 'rs11686149', 'rs16834896', 'rs11889699', 'rs2697306', 'rs4673905', 'rs17248501', 'rs1836729', 'rs4673821', 'rs284531', 'rs10188509', 'rs10191097', 'rs887829', 'rs4332874', 'rs6739594', 'rs2953146', 'rs2953145', 'rs459980', 'rs2129895', 'rs951557', 'rs9815582', 'rs6795255', 'rs1667739', 'rs4858594', 'rs6549906', 'rs4955204', 'rs4276227', 'rs4627791', 'rs906482', 'rs2251219', 'rs2071508', 'rs9881216', 'rs1390245', 'rs1541855', 'rs934841', 'rs9857344', 'rs9826629', 'rs1918399', 'rs12632233', 'rs9850669', 'rs2713694', 'rs2683780', 'rs11918028', 
        #     'rs6787687', 'rs9870357', 'rs7630226', 'rs4679308', 'rs11923216', 'rs7649424', 'rs6807522', 'rs10512895', 'rs6439517', 'rs4683457', 'rs1511554', 'rs7624830', 'rs206316', 'rs1817116', 'rs7622507', 
        #     'rs7428372', 'rs2900668', 'rs1492022', 'rs9838752', 'rs9877175', 'rs779331', 'rs10937909', 'rs4355331', 'rs1479255', 'rs10025322', 'rs1553460', 'rs6827675', 'rs4525961', 'rs7687409', 'rs965253', 'rs13149206', 'rs2055942', 'rs3934674', 'rs4368579', 'rs1372494', 'rs6819526', 'rs2867289', 'rs1371990', 'rs6827298', 'rs1874237', 'rs7691186', 'rs13131633', 'rs2452601', 'rs6838310', 'rs11099007', 'rs649250', 'rs2055392', 'rs4365738', 'rs4956324', 'rs990619', 'rs355168', 'rs6844851', 'rs13126272', 'rs433477', 'rs4862742', 'rs17246850', 'rs1471620', 'rs1471621', 'rs11134359', 'rs411172', 'rs868927', 'rs797309', 'rs6861906', 'rs2561142', 'rs582489', 'rs154250', 'rs11960484', 'rs17732475', 'rs1490796', 'rs10066702', 'rs3934500', 'rs4361497', 'rs4704591', 'rs6452631', 'rs255375', 'rs27000', 'rs4400148', 'rs2643467', 'rs2657439', 'rs1428006', 'rs1643893', 'rs27456', 'rs10037373', 'rs4705247', 'rs1366584', 'rs999580', 'rs9687904', 'rs4389803', 'rs6596989', 'rs9378836', 'rs1029123', 'rs4145451', 'rs9370893', 'rs9464966', 'rs6912394', 'rs6910353', 'rs572550', 'rs2472764', 'rs10946406', 'rs9465890', 'rs3131043', 'rs241429', 'rs4711475', 'rs13196792', 'rs9462805', 'rs1224715', 'rs9294744', 'rs9346240', 'rs852928', 'rs1373360', 'rs700496', 'rs4706172', 'rs474075', 'rs7775358', 'rs2452941', 'rs10484867', 'rs9320996', 'rs1629273', 'rs7765175', 'rs954753', 'rs6906574', 'rs9403799', 'rs1352976', 'rs2763025', 'rs12194277', 'rs3757291', 'rs4709820', 'rs1923380', 'rs6972063', 'rs10951131', 'rs11976431', 'rs6463213', 'rs308092', 'rs968794', 'rs1076224', 'rs2189352', 'rs2285757', 'rs12537100', 'rs4721562', 'rs2237318', 'rs879591', 'rs10238918', 'rs4483064', 'rs2692541', 'rs2941538', 'rs7783847', 'SNP_A-1990374', 'rs10808072', 'rs17345800', 'rs2041681', 'rs2402752', 'rs12706898', 'rs2774960', 'rs10216140', 'rs11768025', 'rs7787537', 'rs1635079', 'rs17280674', 'rs886674', 'rs10241157', 'rs4875428', 'rs481061', 'rs2461020', 'rs2716955', 'rs1487152', 'rs10111407', 'rs2726561', 'rs7003972', 'rs9643449', 'rs4541875', 'rs12542996', 'rs10097578', 'rs2511733', 'rs4734830', 'rs1993980', 'rs3019878', 'rs1456310', 'rs4288339', 'rs12680149', 'rs731589', 'rs7016497', 'rs4350094', 'rs11790055', 'rs7030123', 'rs901992', 'rs10756425', 'rs263655', 'rs10965219', 'rs13301991', 'rs1888379', 'rs10967973', 'rs4879540', 'rs1857080', 'rs1633490', 'rs307652', 'rs1854574', 'rs1573257', 'rs11138278', 'rs815846', 'rs10993628', 'rs7025938', 'rs10760959', 'rs10120268', 'rs7872727', 'rs1931321', 'rs10982256', 'rs4978621', 'rs7860900', 'rs888230', 'rs10119132', 'rs11103407', 'rs9410019', 'rs7906792', 'rs10905165', 'rs10905715', 'rs7917066', 'rs17537423', 'rs1892302', 'rs1111056', 'rs10906865', 'rs7078573', 'rs10740915', 'rs788261', 'rs10826258', 'rs2138556', 'rs942576', 'rs17600642', 'rs10430532', 'rs7077721', 'rs10881889', 'rs7896131', 'rs2861579', 'rs7083245', 'rs11191818', 'rs10886660', 'rs11248381', 'rs2096285', 'rs897355', 'rs4372426', 'rs10832653', 'rs1392998', 'rs2283238', 'rs10742161', 'rs7948834', 'rs10767929', 'rs7928792', 'rs1791687', 'rs11237796', 'rs12273069', 'rs7937583', 'rs2170719', 'rs4258339', 'rs1509728', 'rs4938280', 'rs7948928', 'rs4938805', 'rs2514890', 'rs10893668', 'rs1431573', 'rs6590695', 'rs10848635', 'rs4765747', 'rs10848977', 'rs2110221', 'rs1991192', 'rs753202', 'rs7959282', 'rs7136898', 'rs7312241', 'rs3741629', 'rs10875861', 'rs11168839', 'rs7296288', 'rs10747679', 'rs276056', 'rs11173188', 'rs1245661', 'rs1245652', 'rs7959346', 'rs7139230', 'rs10862673', 'rs1452234', 'rs7297350', 'rs4897823', 'rs1489347', 'rs11106224', 'rs7311213', 'rs12427050', 'rs7486084', 'rs905611', 'rs11112069', 'rs1882496', 'rs7315146', 'rs7133159', 'rs4767759', 'rs10846903', 'rs11059460', 'rs1616468', 'rs4759490', 'rs9550626', 'rs4550321', 'rs515620', 'rs9539828', 'rs7981254', 'rs7985729', 'rs4942472', 'rs7338889', 'rs184828', 'rs1149839', 'rs495838', 'rs9316676', 'rs9598580', 'rs9528626', 'rs12584910', 'rs7995700', 'rs1475797', 'rs1540460', 'rs1927765', 'rs4405424', 'rs2278673', 'rs7333011', 'rs7159947', 'rs17197037', 'rs2293732', 'rs17243139', 'rs10483341', 'rs1467794', 'rs9322991', 'rs2807800', 'rs12434721', 'rs10431700', 'rs11629054', 'rs8007922', 'rs1568404', 'rs1060570', 'rs10220356', 'rs2074932', 'rs11621118', 'rs4903864', 'rs10484022', 'rs7151817', 'rs12587020', 'rs17731311', 'rs1884679', 'rs4904886', 'rs1242112', 'rs734313', 'rs7141044', 'rs10438244', 'rs11622475', 'rs2353498', 'rs4068854', 'rs4780224', 'rs8031347', 'rs10444865', 'rs2305648', 'rs7166775', 'rs7182141', 'rs8036096', 'rs1381855', 'rs12050604', 'rs4924705', 'rs2571249', 'rs12916429', 'rs10519250', 'rs8036777', 'rs7163502', 'rs901130', 'rs8032618', 'rs427459', 'rs17599989', 'rs4420487', 'rs2447265', 
        #     'rs11074005', 'rs8024991', 'rs7163584', 'rs7163576', 'rs4076907', 'rs2092015', 'rs1946127', 'rs4063481', 'rs7198835', 'rs7187198', 'rs12927595', 'rs3851722', 'rs1840186', 'rs226898', 'rs420259', 'rs8059963', 'rs3935873', 'rs7499584', 'rs1344484', 'rs8056052', 'rs2192859', 'rs8050549', 'rs6498863', 'rs8060756', 'rs35198', 'rs12149894', 'rs7184694', 'rs8054657', 'rs1048194', 'rs4782872', 'rs6540248', 'rs9889625', 'rs1521462', 'rs7210608', 'rs2108978', 'rs4924803', 'rs10048172', 'rs203076', 'rs12602586', 'rs2017854', 'rs9897983', 'rs11657439', 'rs7240747', 'rs522276', 'rs12960691', 'rs4797825', 'rs1622239', 'rs2733128', 'rs7237024', 'rs2848782', 'rs3910788', 'rs8083594', 'rs12958775', 'rs1944328', 'rs9963380', 'rs12610384', 'rs759071', 'rs7260296', 'rs889122', 'rs8113425', 'rs7247513', 'rs12979795', 'rs1048123', 'rs4803595', 'rs6509133', 'rs10221457', 'rs10409187', 'rs653925', 'rs11672395', 'rs7248493', 'rs3761218', 'rs6084817', 'rs8121908', 'rs2224300', 'rs3790285', 'rs4564856', 'rs2424430', 'rs17310782', 'rs220530', 'rs6130168', 'rs6030341', 'rs4810439', 'rs6031991', 'rs11696804', 'rs1885290', 'rs941798', 'rs6025653', 'rs6090229', 'rs2823032', 'rs229040', 'rs2154490', 'rs2832394', 'rs2834252', 'rs760138', 'rs4817721', 'rs2834997', 'rs980184', 'rs8130025', 'rs12482209', 'rs17435801', 'rs12157657', 'rs3747113', 'rs688034', 'rs4822752', 
        #     'rs11089599', 'rs933224', 'rs5766424', 'rs5989843', 'rs5939073', 'rs2694712', 'rs1482813', 'rs5915660', 'rs6641047', 'rs2218062', 'rs5979707', 'rs5979951', 'rs17246840', 'rs5909418', 'rs5944611', 
        #     'rs1842186', 'rs1500728', 'rs5943629', 'rs2710405', 'rs5971556', 'rs5928022', 'rs808540', 'rs808539', 'rs12387514', 'rs5963181', 'rs1026332', 'rs235823', 'rs6614576', 'rs2050979', 'rs6625472', 'rs5922091', 'rs5923792', 'rs768198', 'rs6642610', 'rs2744462', 'rs5956772', 'rs12556842', 'rs1324156', 'rs1174079', 'rs5970014', 'rs5924979'
        # ]
        # self.RS_ID = [
        #     'rs1748035', 'rs4920334', 'rs4912122', 'rs12117895', 'rs215773', 'rs3103778', 'rs736861', 'rs869988', 'rs207190', 'rs4276942', 'rs10889189', 'rs2989476', 'rs11207909', 'rs6691577', 'rs7546928', 'rs2132999', 'rs1896250', 'rs1782127', 'rs4658112', 'rs396954', 'rs1361461', 'rs11185337', 'rs12759387', 'rs4378202', 'rs12125340', 'rs10793652', 'rs11240054', 'rs4845390', 'rs4845690', 'rs7534239', 'rs12129036', 'rs2840584', 'rs285482', 'rs7519141', 'rs4657694', 'rs2213736', 'rs1385542', 'rs12401659', 'rs6425425', 'rs4113814', 'rs680638', 'rs951366', 'rs926576', 'rs4628571', 'rs6665548', 'rs6604643', 'rs6679942', 'rs6741819', 'rs4027132', 'rs12472797', 'rs737565', 'rs7562696', 'rs10187657', 'rs3755221', 'rs848531', 'rs11676056', 'rs11687654', 'rs6705537', 'rs7571842', 'rs6730095', 
        #      'rs2678381', 'rs7573844', 'rs7570682', 'rs920217', 'rs11123306', 'rs1375144', 'rs2418876', 'rs6750543', 'rs10928826', 'rs787433', 'rs4641882', 'rs17328734', 'rs6755520', 'rs2592941', 'rs10166245', 'rs1840111', 'rs1344706', 'rs4666691', 'rs11686149', 'rs16834896', 'rs11889699', 'rs2697306', 'rs4673905', 'rs17248501', 'rs1836729', 'rs4673821', 'rs284531', 'rs10188509', 'rs10191097', 'rs887829', 'rs4332874', 'rs6739594', 'rs2953146', 'rs2953145', 'rs459980', 'rs2129895', 'rs951557', 'rs9815582', 'rs6795255', 'rs1667739', 'rs4858594', 'rs6549906', 'rs4955204', 'rs4276227', 'rs4627791', 'rs906482', 'rs2251219', 'rs2071508', 'rs9881216', 'rs1390245', 'rs1541855', 'rs934841', 'rs9857344', 'rs9826629', 'rs1918399', 'rs12632233', 'rs9850669', 'rs2713694', 'rs2683780', 'rs11918028'
        # ]

        self.ProbeSet_ID = []
        # self.ProbeSet_ID = ['SNP_A-1948953', 'SNP_A-1990374']

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

        # 0 stand alone
        # 1 Group
        self.StatusDistance = 0

        # All
        # upstream
        # downstream
        # intron
        self.Relationship = []
        # Example Relationship = [ ['upstream', 'downstream'], ['upstream', 'intron'] ]

        # 0 stand alone
        # 1 Group
        self.StatusRelationship = 0

        # All
        # T1D
        # T2D
        # \/
        # RA
        self.Disease = []
        # Example Disease = [ ['T1D], 'T2D'], ['T1D', 'RA'] ]

        # 0 stand alone
        # 1 Group
        self.StatusDisease = 0

        # 0 All 
        # 1 Huge
        # 2 Kegg
        # 3 Pathway
        # 4 Huge and kegg
        # 5 Huge and pathway
        # 6 kegg and pathway
        # 7 kegg and kegg and pathway
        self.source_website = 0

        self.database = Database()

        self.FormatStrings_RSID_ProbeSetID = ""
        self.FormatStrings_GeneID = ""
        self.FormatStrings_GeneSymbol = ""
        self.FormatStrings_Chromosome = ""
        self.FormatStrings_Position = ""
        self.FormatStrings_Distance = ""
        self.FormatStrings_Relationship = ""
        self.FormatStrings_Disease = ""
        self.FormatStrings_GeneShip = ""
        self.FormatStrings_Source_Website = ""
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
            FormatStrings_RSID_ProbeSetID = "snp.PROBESET_ID = '" + str(listProbeSetID[0]) + "' OR " + "snp.RS_ID = '" + str(self.RS_ID[0]) + "'"

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
                listChromosome = ", ".join([str(Each_Chromosome) for Each_Chromosome in self.Chromosome])
                FormatStrings_Chromosome = 'and snp.CHROMOSOME IN (' + listChromosome + ')'

            elif len(self.Chromosome) == 1:
                FormatStrings_Chromosome = 'and snp.CHROMOSOME = ' + str(self.Chromosome[0])

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

        list_FormatStrings_Distance = ['', '', '', '']
        listDistance_0 = []
        listDistance_1 = []
        listDistance_2 = []
        listDistance_3 = []

        if ( len(self.Distance) == 0):
            return FormatStrings_Distance
        
        else:
            if (self.StatusDistance == 0):
                if ( len(self.Distance) > 0):
                    for condition in self.Distance:
                        if (condition[0] == 0): listDistance_0.append(str(condition[1]))
                        elif (condition[0] == 1): listDistance_1.append(str(condition[1]))
                        elif (condition[0] == 2): listDistance_2.append(str(condition[1]))
                        elif (condition[0] == 3): listDistance_3.append([condition[1],condition[2]])

                if (len(listDistance_0) > 0):
                    if len(listDistance_0) == 1:
                        list_FormatStrings_Distance[0] = 'gene_detail.DISTANCE = ' + str(listDistance_0[0]) + ' '
                    else:
                        listDistance_0 = ", ".join( [(str(Each_Distance)) for Each_Distance in listDistance_0])
                        list_FormatStrings_Distance[0] = 'gene_detail.DISTANCE IN (' + listDistance_0 + ' ) '

                if (len(listDistance_1) > 0):
                    list_FormatStrings_Distance[1] = " or ".join( ['gene_detail.DISTANCE < ' + (str(Each_Range) ) for Each_Range in listDistance_1])

                if (len(listDistance_2) > 0):
                    list_FormatStrings_Distance[2] = " or ".join( ['gene_detail.DISTANCE > ' + (str(Each_Range) ) for Each_Range in listDistance_2])

                if (len(listDistance_3) > 0):
                    list_FormatStrings_Distance[3] = " OR ".join( ['gene_detail.DISTANCE between ' + (str(Each_Range[0])) + ' AND ' + (str(Each_Range[1])) for Each_Range in listDistance_3])

                FormatStrings_Distance = " or ".join( [ (str(Each_FormatStrings_Distance) ) for Each_FormatStrings_Distance in list_FormatStrings_Distance if Each_FormatStrings_Distance != '' ])

                if (len(FormatStrings_Distance) != 0):
                    FormatStrings_Distance = " and ( " + FormatStrings_Distance + " ) "
            else:
                listFormatString = []
                FormatStrings_RSID_ProbeSetID = "gene_detail." + (self.CreateFormatStrings_RSID_ProbeSetID(0))[4:]

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

                    FormatiString = 'gene_detail.RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE ' + FormatStrings_RSID_ProbeSetID + ' GROUP BY RS_ID HAVING COUNT(*) > ' + str(len(Each_Group) - 1) + ' ) AND RELATIONSHIP IN (' + str(listRelationship) + ') AND (' + FormatStrings_GroupDistance + ') GROUP BY RS_ID HAVING COUNT(distinct RELATIONSHIP) = ' + str(len(Each_Group)) + ')'
                    listFormatString.append( FormatiString )

                FormatStrings_Distance = " or ".join( [ (str(Each_FormatString) ) for Each_FormatString in listFormatString if Each_FormatString != '' ])

            FormatStrings_Distance = " and ( " + FormatStrings_Distance + " ) "

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
                FormatStrings_RSID_ProbeSetID = "gene_detail." + (self.CreateFormatStrings_RSID_ProbeSetID(0))[4:]

                for Each_Group in self.Relationship:
                    listRelationship = ", ".join( [ ( "'" + str(Each_Relationship) + "'" ) for Each_Relationship in Each_Group])
                    listFormatString.append( 'gene_detail.RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE RS_ID IN ( SELECT RS_ID FROM gene_detail WHERE ' + FormatStrings_RSID_ProbeSetID + ' GROUP BY RS_ID HAVING COUNT(*) > ' + str(len(Each_Group) - 1) + ' ) AND RELATIONSHIP IN (' + str(listRelationship) + ') GROUP BY RS_ID HAVING COUNT(distinct RELATIONSHIP) = ' + str(len(Each_Group)) + ')' )

                FormatStrings_Relationship = " and ( " + ( " OR ".join( [ ( str(Each_String) ) for Each_String in listFormatString]) ) + " ) "

        return FormatStrings_Relationship

    def CreateFormatStrings_Disease(self):
        FormatStrings_Disease = ''

        if len(self.Disease) == 0:
           return FormatStrings_Disease

        else:
            if (self.StatusDisease == 0):

                if len(self.Disease) > 1:
                    listDisease = ", ".join( [("'" + str(Each_Disease) + "'") for Each_Disease in self.Disease])
                    FormatStrings_Disease = 'and disease.DISEASE_ABBREVIATION IN (' + listDisease + ')'

                elif len(self.Disease) == 1:
                    FormatStrings_Disease = "and disease.DISEASE_ABBREVIATION = '" + str(self.Disease[0]) + "'"

            elif (self.StatusDisease == 1):
                listFormatString = []

                for Each_Group in self.Disease:
                    listDisease = ", ".join( [ ( str( DiseaseEnum[str(Each_Disease)].value ) ) for Each_Disease in Each_Group] )
                    listFormatString.append( 'matching_snp_disease.RS_ID IN ( SELECT RS_ID FROM matching_snp_disease WHERE RS_ID IN ( SELECT RS_ID FROM matching_snp_disease GROUP BY RS_ID HAVING COUNT(*) = ' + str(len(Each_Group)) + ' ) AND DISEASE_ID IN (' + str(listDisease) + ') GROUP BY RS_ID HAVING COUNT(distinct DISEASE_ID) = ' + str(len(Each_Group)) + ')' )

                FormatStrings_Disease = " and ( " + ( " OR ".join( [ ( str(Each_String) ) for Each_String in listFormatString]) ) + " ) "
                

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
        elif self.source_website == 4:
            return 'and matching_snp_disease.MatchBy IN ("huge", "kegg")'
        elif self.source_website == 5:
            return 'and matching_snp_disease.MatchBy IN ("huge", "pathway")'
        elif self.source_website == 6:
            return 'and matching_snp_disease.MatchBy IN ("kegg", "pathway")'


    def SQLCommand_Found_InDisease(self, FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Distance, FormatStrings_Relationship, FormatStrings_Disease, FormatStrings_GeneShip, FormatStrings_Source_Website):
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

        return mysqlCommand_FoundInDisease
    
    def SQLCommand_Found_NotInDisease(self, FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Distance, FormatStrings_Relationship, FormatStrings_GeneShip):
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
            FormatStrings_Distance,
            FormatStrings_Relationship,
            FormatStrings_GeneShip
        )

        return mysqlCommand_NotFoundInDisease

    def SQLCommand_NotFound_InDisease(self, FormatStrings_RSID_ProbeSetID):
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

    def SQLCommand_NotFound_NotInDisease(self, FormatStrings_RSID_ProbeSetID):
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

        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(status=0)
        FormatStrings_GeneID = self.CreateFormatStrings_GeneID()
        FormatStrings_GeneSymbol = self.CreateFormatStrings_GeneSymbol()
        FormatStrings_Chromosome = self.CreateFormatStrings_Chromosome()
        FormatStrings_Position = self.CreateFormatStrings_Position()
        FormatStrings_Distance = self.CreateFormatStrings_Distance()
        FormatStrings_Relationship = self.CreateFormatStrings_Relationship()
        FormatStrings_Disease = self.CreateFormatStrings_Disease()
        FormatStrings_GeneShip = self.CreateFormatStrings_GeneShip()
        FormatStrings_Source_Website = self.CreateFormatStrings_Source_Website()

        SQLCommand_Found_InDisease = self.SQLCommand_Found_InDisease(FormatStrings_RSID_ProbeSetID, FormatStrings_GeneID, FormatStrings_GeneSymbol, FormatStrings_Chromosome, FormatStrings_Position, FormatStrings_Distance, FormatStrings_Relationship, FormatStrings_Disease, FormatStrings_GeneShip, FormatStrings_Source_Website)
        print('SQLCommand_Found_InDisease :', SQLCommand_Found_InDisease)

        results_Found_InDisease = set( database.CreateTask(conn, SQLCommand_Found_InDisease, ()) )

        Result_Relate_InDisease = []
        Result_Relate_NotInDisease = []
        Result_Unrelate_InDisease = []
        Result_Unrelate_NotInDisease = []

        listUniqueRelated_RSID = []
        listUniqueRelated_ProbeSetID = []
        listUniqueUnrelated_RSID = []
        listUniqueUnrelated_ProbeSetID = []
        
        if ( results_Found_InDisease != [] ):
            print('\n List gene has found on disease \n')

            Index = 0
            for result in results_Found_InDisease:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                print(
                    '               INDEX :', Index, '\n'
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
                    '        DISEASE_NAME :', result[9], '\n'
                    'DISEASE_ABBREVIATION :', result[10], '\n'
                    '            MATCH_BY :', result[11], '\n'
                )

                listUniqueRelated_RSID, listUniqueRelated_ProbeSetID = self.ExtractRelatedGeneID(result[0], result[1], listUniqueRelated_RSID, listUniqueRelated_ProbeSetID)

                each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol]),result[9],result[10], result[11]]

                Index = Index + 1
                Result_Relate_InDisease.append(each_result)

        listUniqueUnrelated_RSID, listUniqueUnrelated_ProbeSetID = self.ExtractUnrelatedGeneID(listUniqueUnrelated_RSID, listUniqueUnrelated_ProbeSetID)
        FormatStrings_RSID_ProbeSetID = self.CreateFormatStrings_RSID_ProbeSetID(1, listUniqueUnrelated_RSID, listUniqueUnrelated_ProbeSetID)
        
        SQLCommand_NotFound_InDisease = self.SQLCommand_NotFound_InDisease(FormatStrings_RSID_ProbeSetID)
        print('SQLCommand_NotFound_InDisease :', SQLCommand_NotFound_InDisease)

        results_NotFound_InDisease = set( database.CreateTask(conn, SQLCommand_NotFound_InDisease, ()) )

        if ( results_NotFound_InDisease != [] ):
            print('\n List gene has not found on disease \n')

            Index = 0
            for result in results_NotFound_InDisease:
                mysqlCommand = """ 
                    SELECT
                        OTHER_SYMBOL
                    FROM other_symbol
                    WHERE GENE_ID = %s
                """

                other_symbol = database.CreateTask(conn, mysqlCommand, (result[8], ))

                print(
                    '               INDEX :', Index, '\n'
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
                )

                each_result = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],', '.join([str(elem)[2:-3] for elem in other_symbol])]
                Index = Index + 1
                Result_Unrelate_InDisease.append(each_result)

        database.CloseDatabase(conn)

        return Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease

if __name__ == "__main__":
    searchFunction = Search()
    searchFunction.SearchData()