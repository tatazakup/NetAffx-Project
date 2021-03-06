from Initialization import Database, FilePath
from AnnotationFile import Manage_AnnotationFile
from pathway import PathwayDataFromKEGG, PathwayOfDis
from ncbi import Ncbi
from Disease import Disease
from Search import Search
from datetime import datetime
import pandas as pd

class TestCase():
    def __init__(self):
        self.TestSearch = Search()
        self.Allpath = FilePath()
        return

    def ReadCSVFile(self, filePath):
        return pd.read_csv( filePath )

    def CheckAccuracy(self, inputData, correctInformation, TestName):
        check = all(item in inputData for item in correctInformation)

        if check is True: print('Test', str(TestName), 'is correct')
        else: print('Test', str(TestName), 'is incorrect')

    def CheckInputData(self, checkData, FilenameData):
        if checkData != []: listDataFromFile = checkData
        else:
            listDataFromFile = []
            FileData = self.ReadCSVFile(FilenameData)
            # listDataFromFile = [[row[col] for col in FileData.columns] for row in FileData.to_dict('records')]

            for row in FileData.to_dict('records'):
                arrayRow = []
                index = 0
                for col in FileData.columns:                    
                    if (index == 2): arrayRow.append(str(row[col]))
                    elif (index == 9): 
                        if (str(row[col]) == "nan"): arrayRow.append('')
                        else: arrayRow.append(str(row[col]))
                    else: arrayRow.append(row[col])
                    index = index + 1
                listDataFromFile.append(arrayRow)

        return listDataFromFile

    def ProcessAccuracySearch(self, PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease):
        Filename_R_D = PREFIX + 'RELATE_INDISEASE.csv'
        Filename_R_ND = PREFIX + 'RELATE_NOTINDISEASE.csv'
        Filename_NR_D = PREFIX + 'UNRELATE_INDISEASE.csv'
        Filename_NR_ND = PREFIX + 'UNRELATE_NOTINDISEASE.csv'

        PathToRelateInDisease = self.Allpath.GetPathToTestCase() + '/' + Filename_R_D
        PathToRelateNotInDisease = self.Allpath.GetPathToTestCase() + '/' + Filename_R_ND
        PathToUnRelateInDisease = self.Allpath.GetPathToTestCase() + '/' + Filename_NR_D
        PathToUnRelateNotInDisease = self.Allpath.GetPathToTestCase() + '/' + Filename_NR_ND

        ListData_R_D_FromFile = self.CheckInputData(Input_Relate_InDisease, PathToRelateInDisease)
        ListData_R_ND_FromFile = self.CheckInputData(Input_Relate_NotInDisease, PathToRelateNotInDisease)
        ListData_NR_D_FromFile = self.CheckInputData(Input_UnRelate_InDisease, PathToUnRelateInDisease)
        ListData_NR_ND_FromFile = self.CheckInputData(Input_UnRelate_NotInDisease, PathToUnRelateNotInDisease)

        print('Result_Relate_NotInDisease :', Result_Relate_NotInDisease)
        print('ListData_R_ND_FromFile :', ListData_R_ND_FromFile)

        self.CheckAccuracy(Result_Relate_InDisease, ListData_R_D_FromFile, Filename_R_D)
        self.CheckAccuracy(Result_Relate_NotInDisease, ListData_R_ND_FromFile, Filename_R_ND)
        self.CheckAccuracy(Result_Unrelate_InDisease, ListData_NR_D_FromFile, Filename_NR_D)
        self.CheckAccuracy(Result_Unrelate_NotInDisease, ListData_NR_ND_FromFile, Filename_NR_ND)
        return

    # Gene ID
    def SEARCH_GENE_ID_WITH_CONDITION_00(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_00_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])      

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_ID_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([10402])        

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_ID_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([10402, 23657, 55486])        

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_ID_WITH_CONDITION_03(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([1])        

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)

        return


    # GENE SYMBOL
    def SEARCH_GENE_SYMBOL_WITH_CONDITION_00(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_00_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABCC5'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABCC5', 'PARL'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_03(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC33'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_04(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_04_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC33', 'PRO2207'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_05(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_05_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # CHROMOSOME
    def SEARCH_CHROMOSOME_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([0])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_CHROMOSOME_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_CHROMOSOME_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1, 2, 10, 11])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_CHROMOSOME_WITH_CONDITION_03(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1, 2, 10])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # POSITION
    def SEARCH_POSITION_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_POSITION_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])
        TestSearch.Add_Position([ [1, 100000] ])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return
    
    def SEARCH_POSITION_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])
        TestSearch.Add_Position([ [1, 100000], [2, 500000] ])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # GENESHIP
    def SEARCH_GENESHIP_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(0)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_GENESHIP_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return
    
    def SEARCH_GENESHIP_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(2)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # RELATIONSHIP_DISTANCE
    def SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64372]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64372], ['downstream', 196896]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64371]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # DISEASE
    def SEARCH_DISEASE_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_DISEASE_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])
        TestSearch.Add_Disease(['T1D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return
        
    def SEARCH_DISEASE_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])
        TestSearch.Add_Disease(['T1D', 'T2D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    # SOURCE WEBSITE
    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_source_website(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000078', 'rs5745711'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_source_website(3)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_source_website(5)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return
    
    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData([])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData([])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        """Test search all data with out condition"""

        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_source_website(7)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    # Within or Near Gene (Associated Gene)
    def Test_SNPAssociatedWithT1D(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithT1D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs3129768', 'rs4530903', 'rs2647015', 'rs9275765', 'rs4530903'])
        TestSearch.Add_Disease(['T1D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithT2D(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithT2D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs3217986', 'SNP_A-2224457', 'rs10743598', 'rs1029340'])
        TestSearch.Add_Disease(['T2D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithBD(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithBD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs5752827', 'SNP_A-2195650', 'rs1000192', 'SNP_A-4250467'])
        TestSearch.Add_Disease(['BD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithCAD(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithCAD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1020256', 'SNP_A-4213970', 'rs10807172', 'SNP_A-2243662'])
        TestSearch.Add_Disease(['CAD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithCD(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithCD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2266236', 'rs10264856', 'rs1810563', 'SNP_A-1815331'])
        TestSearch.Add_Disease(['CD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithHT(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithHT_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4543', 'SNP_A-2245620', 'rs11253209', 'SNP_A-1911234'])
        TestSearch.Add_Disease(['HT'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithRA(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithRA_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2185852', 'rs11569334', 'rs10494777', 'rs1006509'])
        TestSearch.Add_Disease(['RA'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        
        return

    def Test_SNPAssociatedWithT1DByKeGG_Upstream2000_(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithT1DByKeGG_Upstream2000_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9296073', 'rs7757722', 'rs2395451', 'rs7757391'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_Relationship_Distance([['upstream', 2000]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPAssociatedWithT2DByHuge_Downstream2000(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithT2DByHuge_Downstream2000_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs11568046', 'rs13034231', 'rs1644402', 'rs1757067'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_Relationship_Distance([['downstream', 500]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPAssociatedWithBDByPathway_Intron(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithBDByPathway_Intron_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10513896', 'rs9397797', 'rs12036786', 'rs1065457'])
        TestSearch.Add_Disease(['BD'])
        TestSearch.Add_Relationship_Distance(['intron'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPAssociatedWithCAD_Nsp(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithCAD_Nsp_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2243662', 'SNP_A-1957669', 'rs7026498', 'rs1027311', 'SNP_A-4208936', 'SNP_A-4229912'])
        TestSearch.Add_Disease(['CAD'])
        TestSearch.Add_Geneship(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPAssociatedWithCD_Sty(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithCD_Sty_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1077861', 'rs1000113', 'rs12720067', 'rs10128203', 'rs10754805', 'rs12474201'])
        TestSearch.Add_Disease(['CD'])
        TestSearch.Add_Geneship(2)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPAssociatedWithHT_CHR8(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPAssociatedWithHT_CHR8_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10093618', 'rs7844961', 'rs10100812', 'rs10503813', 'rs7819943'])
        TestSearch.Add_Disease(['HT'])
        TestSearch.Add_Chromosome(8)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    
    # Within or Near Gene (Non Associated Gene)
    def Test_SNPUpstream_nonAssT1D(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPUpstream_nonAssT1D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs17054099', 'rs11040883', 'rs11804609', 'rs6634846', 'rs11734396'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_Relationship_Distance([['upstream', 2000]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPDownstream_nonAssT2D(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPDownstream_nonAssT2D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs11574647', 'rs767652', 'rs11040883', 'rs9353470', 'rs874158'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_Relationship_Distance([['downstream', 500]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPwithin_nonAssBD(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPwithin_nonAssBD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4594580', 'rs2546001', 'rs2228006', 'rs1805794', 'rs2288242'])
        TestSearch.Add_Disease(['BD'])
        TestSearch.Add_Relationship_Distance([['downstream', 500]])
        TestSearch.Add_Relationship_Distance(['intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    # OutSide Gene
    def Test_SNPoutside1(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPoutside1_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs233978', 'rs9965312', 'rs41464449', 'rs251292', 'rs7660291'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPoutside2(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPoutside2_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9887913', 'rs4775229', 'rs1125082', 'rs11768639', 'rs3753452'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPoutside3(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPoutside3_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9887913', 'rs4775229', 'rs1125082', 'rs11768639', 'rs3753452'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPoutside_asso(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPoutside_asso_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs233978', 'rs9965312', 'rs251292', 'rs9887913', 'rs1125082'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return

    def Test_SNPoutside_nonasso(self, Input_Relate_InDisease = [], Input_Relate_NotInDisease = [], Input_UnRelate_InDisease = [], Input_UnRelate_NotInDisease = []):
        PREFIX = 'Test_SNPoutside_nonasso_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs41464449', 'rs7660291', 'rs4775229', 'rs3753452', 'rs10120738'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessAccuracySearch(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease, Input_Relate_InDisease, Input_Relate_NotInDisease, Input_UnRelate_InDisease, Input_UnRelate_NotInDisease)
        return


    def UPDATE_NCBI_WITH_CONDITION_01(self):
        """Test Update ncbi data with delete GENE_ID(388) on other_symbol table"""

        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            DELETE FROM other_symbol WHERE GENE_ID = %s;
        """
        database.CreateTask(conn, mysqlCommand, (338, ))

        mysqlCommand = """
            UPDATE ncbi SET
            UPDATE_AT = %s WHERE
            GENE_ID = %s
        """
        database.CreateTask(conn, mysqlCommand, (datetime.fromtimestamp(1643000000).strftime('%Y-%m-%d %H:%M:%S'), 338))
        database.CloseDatabase(conn)

        ncbi = Ncbi(1)
        ncbi.UpdateNcbiInformation()

        return

    def UPDATE_NCBI_WITH_CONDITION_02(self):
        """Test Delete 1 ncbi data with delete other_symbol table on GENE_ID(338)"""

        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            DELETE FROM other_symbol WHERE GENE_ID = %s and OTHER_SYMBOL = %s;
        """
        database.CreateTask(conn, mysqlCommand, (338, 'FCHL2', ))

        mysqlCommand = """
            UPDATE ncbi SET
            UPDATE_AT = %s WHERE
            GENE_ID = %s
        """
        database.CreateTask(conn, mysqlCommand, (datetime.fromtimestamp(1643000000).strftime('%Y-%m-%d %H:%M:%S'), 338))
        database.CloseDatabase(conn)

        ncbi = Ncbi(1)
        ncbi.UpdateNcbiInformation()

        return

    def UPDATE_NCBI_WITH_CONDITION_03(self):
        """Test Add new 1 ncbi data with add other_symbol table on GENE_ID(338)"""

        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            INSERT IGNORE INTO other_symbol (GENE_ID, OTHER_SYMBOL) VALUE (%s, %s);
        """
        database.CreateTask(conn, mysqlCommand, (338, 'FCHL1', ))

        mysqlCommand = """
            UPDATE ncbi SET
            UPDATE_AT = %s WHERE
            GENE_ID = %s
        """
        database.CreateTask(conn, mysqlCommand, (datetime.fromtimestamp(1643000000).strftime('%Y-%m-%d %H:%M:%S'), 338))
        database.CloseDatabase(conn)

        ncbi = Ncbi(1)
        ncbi.UpdateNcbiInformation()

        return

    # UPDATE DISEASE
    def UPDATE_DISEASE_WITH_CONDITION_01(self):
        """ Disease ?????? Website ????????? """

        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            INSERT IGNORE INTO gene_disease (GENE_SYMBOL, DISEASE_ID) VALUE (%s, %s);
        """
        database.CreateTask(conn, mysqlCommand, ('TEST_DISEASE_1', 1, ))
        database.CloseDatabase(conn)

        disease = Disease()
        disease.UpdateDiseaseDataset()
        
        return

    def UPDATE_DISEASE_WITH_CONDITION_02(self):
        """ Disease ?????? Database ?????????????????? """

        database = Database()
        conn = database.ConnectDatabase()
        mysqlCommand = """
            DELETE FROM gene_disease WHERE GENE_SYMBOL = %s and DISEASE_ID = %s;
        """
        database.CreateTask(conn, mysqlCommand, ('INS', 1, ))
        database.CloseDatabase(conn)

        disease = Disease()
        disease.UpdateDiseaseDataset()
        
        return
    
    # Manage AnnotationFile
    def Manage_AnnotationFile_(self, RSID, Genechip):
        Separate_Gene = Manage_AnnotationFile()
        snp = Separate_Gene.TestSeparateGene(RSID, Genechip)
        for i in snp.Associated_Gene:
            i.show()
            print(' ')
        
        ListS = []
        ListS.append(snp)
        Separate_Gene.SaveSNP(ListS)
    
    # Create Data Pathway
    def Get_GeneOfPathway(self, PathwayID):
        Data_Pathway = PathwayDataFromKEGG()
        Data_Pathway.testGetGenePathway(PathwayID)
        print('number of gene in ', PathwayID, ' =', len(Data_Pathway.listpathway))
        return Data_Pathway.listpathway
        
    def Get_PathwayOfDisease(self, Disease):
        Pathway_Dis = PathwayOfDis()
        ListPathwayID = Pathway_Dis.testFetchPathwayEachDisease(Disease)
        print('number of Pathway in ', Disease, ' =', len(ListPathwayID))
        return ListPathwayID
    
    def Get_AssociatedGeneOfDiseaseByPathway(self, Disease):
        numberGene = 0
        ListPathwayID = self.Get_PathwayOfDisease(Disease)
        for pathwayID in ListPathwayID:
            listGeneInPathway = self.Get_GeneOfPathway(pathwayID)
            numberGene += len(listGeneInPathway)
        print('number of associated gene in This Disease by Pathway :', numberGene)


class CreateTestCase():
    def __init__(self):
        self.listcolumns_FD = ['RSID', 'PROBESET_ID', 'CHROMOSOME', 'POSITION', 'SOURCE_GENESHIP', 'RELATIONSHIP', 'DISTANCE', 'GENE_SYMBOL', 'GENE_ID', 'OTHER_SYMBOL', 'DISEASE_NAME', 'DISEASE_ABBREVIATION', 'MATCH_BY']
        self.listcolumns_NFD = ['RSID', 'PROBESET_ID', 'CHROMOSOME', 'POSITION', 'SOURCE_GENESHIP', 'RELATIONSHIP', 'DISTANCE', 'GENE_SYMBOL', 'GENE_ID', 'OTHER_SYMBOL']

        self.allpath = FilePath()

        self.CREATE_SEARCH_ALL_DATA_01()

        self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_00()
        self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_01()
        self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_02()
        self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_03()

        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_00()
        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_01()
        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_02()
        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_03()
        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_04()
        self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_05()

        self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_ALL()
        self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_01()
        self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_02()
        self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_03()

        self.CREATE_SEARCH_POSITION_WITH_CONDITION_ALL()
        self.CREATE_SEARCH_POSITION_WITH_CONDITION_01()
        self.CREATE_SEARCH_POSITION_WITH_CONDITION_02()

        self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_ALL()   
        self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_01()   
        self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_02()

        self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL()
        self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01()
        self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02()
        self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03()

        self.CREATE_SEARCH_DISEASE_WITH_CONDITION_ALL()
        self.CREATE_SEARCH_DISEASE_WITH_CONDITION_01()
        self.CREATE_SEARCH_DISEASE_WITH_CONDITION_02()

        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07()

        self.CREATE_Test_SNPAssociatedWithT1D()
        self.CREATE_Test_SNPAssociatedWithT2D()
        self.CREATE_Test_SNPAssociatedWithBD()
        self.CREATE_Test_SNPAssociatedWithCAD()
        self.CREATE_Test_SNPAssociatedWithCD()
        self.CREATE_Test_SNPAssociatedWithHT()
        self.CREATE_Test_SNPAssociatedWithRA()
        self.CREATE_Test_SNPAssociatedWithT1DByKeGG_Upstream2000()
        self.CREATE_Test_SNPAssociatedWithT2DByHuge_Downstream2000()
        self.CREATE_Test_SNPAssociatedWithBDByPathway_Intron()
        self.CREATE_Test_SNPAssociatedWithCAD_Nsp()
        self.CREATE_Test_SNPAssociatedWithCD_Sty()
        self.CREATE_Test_SNPAssociatedWithHT_CHR8()

        self.CREATE_Test_SNPUpstream_nonAssT1D()
        self.CREATE_Test_SNPDownstream_nonAssT2D()
        self.CREATE_Test_SNPwithin_nonAssBD()

        self.CREATE_Test_SNPoutside1()
        self.CREATE_Test_SNPoutside2()
        self.CREATE_Test_SNPoutside3()

        self.CREATE_Test_SNPoutside_asso()
        self.CREATE_Test_SNPoutside_nonasso()

        return

    def ImportDataTo_FD(self, fileName, data):
        path_output = self.allpath.GetPathToTestCase() + '/' + fileName
        df = pd.DataFrame(data,columns = self.listcolumns_FD)
        df.to_csv(path_output,index=False)

    def ImportDataTo_NFD(self, fileName, data):
        path_output = self.allpath.GetPathToTestCase() + '/' + fileName
        df = pd.DataFrame(data,columns = self.listcolumns_NFD)
        df.to_csv(path_output,index=False)

    def ProcessCreateDataset(self, PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease):
        Filename_R_D = PREFIX + 'RELATE_INDISEASE.csv'
        Filename_R_ND = PREFIX + 'RELATE_NOTINDISEASE.csv'
        Filename_NR_D = PREFIX + 'UNRELATE_INDISEASE.csv'
        Filename_NR_ND = PREFIX + 'UNRELATE_NOTINDISEASE.csv'

        self.ImportDataTo_FD(Filename_R_D, Result_Relate_InDisease)
        self.ImportDataTo_NFD(Filename_R_ND, Result_Relate_NotInDisease)
        self.ImportDataTo_FD(Filename_NR_D, Result_Unrelate_InDisease)
        self.ImportDataTo_NFD(Filename_NR_ND, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_ALL_DATA_01(self):
        PREFIX = 'SEARCH_ALL_DATA_01_'
        TestSearch = Search()
        Results_FD, Result_NFD = TestSearch.SearchData()
        self.ImportDataTo_FD(PREFIX + 'FD.csv', Results_FD)
        self.ImportDataTo_NFD(PREFIX + '_NFD.csv', Result_NFD)
        return

    # Gene ID
    def CREATE_SEARCH_GENE_ID_WITH_CONDITION_00(self):
        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_00_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_ID_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([10402])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_ID_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([10402, 23657, 55486])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_ID_WITH_CONDITION_03(self):
        PREFIX = 'SEARCH_GENE_ID_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneID([1])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    # GENE SYMBOL
    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_00(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_00_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABCC5'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABCC5', 'PARL'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_03(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC33'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_04(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_04_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC33', 'PRO2207'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_05(self):
        PREFIX = 'SEARCH_GENE_SYMBOL_WITH_CONDITION_05_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000012', 'rs1000002', 'rs1000003', 'rs10000033', 'rs10000037'])
        TestSearch.Add_GeneSymbol(['ABC'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    # CHROMOSOME
    def CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([0])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1, 2, 10, 11])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_03(self):
        PREFIX = 'SEARCH_CHROMOSOME_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000050', 'rs1000017', 'rs1000039', 'rs1000061', 'rs1000042'])
        TestSearch.Add_Chromosome([1, 2, 10])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return


    # POSITION
    def CREATE_SEARCH_POSITION_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_POSITION_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])
        TestSearch.Add_Position([[1, 100000]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_POSITION_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_POSITION_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10452313', 'rs10001263', 'rs10969094', 'rs1048466', 'rs10757847'])
        TestSearch.Add_Position([ [1, 100000], [2, 500000] ])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return


    # GENESHIP
    def CREATE_SEARCH_GENESHIP_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(0)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENESHIP_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_GENESHIP_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_GENESHIP_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000042', 'rs1000269', 'rs1000411', 'rs1000552', 'rs1001796'])
        TestSearch.Add_Geneship(2)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    # RELATIONSHIP_DISTANCE
    def CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64372]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64372], ['downstream', 196896]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03(self):
        PREFIX = 'SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4912122', 'rs41464449', 'rs1705415', 'rs7553394'])
        TestSearch.Add_Relationship_Distance([['upstream', 64371]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    # DISEASE
    def CREATE_SEARCH_DISEASE_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_DISEASE_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])
        TestSearch.Add_Disease(['T1D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_DISEASE_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_DISEASE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10000203', 'rs10000241', 'rs1000078', 'rs10012946'])
        TestSearch.Add_Disease(['T1D', 'T2D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    # SOURCE WEBSITE
    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_source_website(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1000078', 'rs5745711'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_source_website(3)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_source_website(5)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData([])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData([])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07(self):
        PREFIX = 'SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10189577', 'rs1000078', 'rs5745711', 'rs1610274', 'rs3217986'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_source_website(7)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        return


    # Within or Near Gene (Associated Gene)
    def CREATE_Test_SNPAssociatedWithT1D(self):
        PREFIX = 'Test_SNPAssociatedWithT1D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs3129768', 'rs4530903', 'rs2647015', 'rs9275765', 'rs4530903'])
        TestSearch.Add_Disease(['T1D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithT2D(self):
        PREFIX = 'Test_SNPAssociatedWithT2D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs3217986', 'SNP_A-2224457', 'rs10743598', 'rs1029340'])
        TestSearch.Add_Disease(['T2D'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithBD(self):
        PREFIX = 'Test_SNPAssociatedWithBD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs5752827', 'SNP_A-2195650', 'rs1000192', 'SNP_A-4250467'])
        TestSearch.Add_Disease(['BD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithCAD(self):
        PREFIX = 'Test_SNPAssociatedWithCAD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1020256', 'SNP_A-4213970', 'rs10807172', 'SNP_A-2243662'])
        TestSearch.Add_Disease(['CAD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithCD(self):
        PREFIX = 'Test_SNPAssociatedWithCD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2266236', 'rs10264856', 'rs1810563', 'SNP_A-1815331'])
        TestSearch.Add_Disease(['CD'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithHT(self):
        PREFIX = 'Test_SNPAssociatedWithHT_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4543', 'SNP_A-2245620', 'rs11253209', 'SNP_A-1911234'])
        TestSearch.Add_Disease(['HT'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithRA(self):
        PREFIX = 'Test_SNPAssociatedWithRA_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2185852', 'rs11569334', 'rs10494777', 'rs1006509'])
        TestSearch.Add_Disease(['RA'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithT1DByKeGG_Upstream2000(self):
        PREFIX = 'Test_SNPAssociatedWithT1DByKeGG_Upstream2000_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9296073', 'rs7757722', 'rs2395451', 'rs7757391'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_Relationship_Distance([['upstream', 2000]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithT2DByHuge_Downstream2000(self):
        PREFIX = 'Test_SNPAssociatedWithT2DByHuge_Downstream2000_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs11568046', 'rs13034231', 'rs1644402', 'rs1757067'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_Relationship_Distance([['downstream', 500]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithBDByPathway_Intron(self):
        PREFIX = 'Test_SNPAssociatedWithBDByPathway_Intron_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10513896', 'rs9397797', 'rs12036786', 'rs1065457'])
        TestSearch.Add_Disease(['BD'])
        TestSearch.Add_Relationship_Distance(['intron'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithCAD_Nsp(self):
        PREFIX = 'Test_SNPAssociatedWithCAD_Nsp_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['SNP_A-2243662', 'SNP_A-1957669', 'rs7026498', 'rs1027311', 'SNP_A-4208936', 'SNP_A-4229912'])
        TestSearch.Add_Disease(['CAD'])
        TestSearch.Add_Geneship(1)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithCD_Sty(self):
        PREFIX = 'Test_SNPAssociatedWithCD_Sty_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs1077861', 'rs1000113', 'rs12720067', 'rs10128203', 'rs10754805', 'rs12474201'])
        TestSearch.Add_Disease(['CD'])
        TestSearch.Add_Geneship(2)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPAssociatedWithHT_CHR8(self):
        PREFIX = 'Test_SNPAssociatedWithHT_CHR8_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs10093618', 'rs7844961', 'rs10100812', 'rs10503813', 'rs7819943'])
        TestSearch.Add_Disease(['HT'])
        TestSearch.Add_Chromosome(8)

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    # Within or Near Gene (Non Associated Gene)
    def CREATE_Test_SNPUpstream_nonAssT1D(self):
        PREFIX = 'Test_SNPUpstream_nonAssT1D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs17054099', 'rs11040883', 'rs11804609', 'rs6634846', 'rs11734396'])
        TestSearch.Add_Disease(['T1D'])
        TestSearch.Add_Relationship_Distance([['upstream', 2000]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPDownstream_nonAssT2D(self):
        PREFIX = 'Test_SNPDownstream_nonAssT2D_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs11574647', 'rs767652', 'rs11040883', 'rs9353470', 'rs874158'])
        TestSearch.Add_Disease(['T2D'])
        TestSearch.Add_Relationship_Distance([['downstream', 500]])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPwithin_nonAssBD(self):
        PREFIX = 'Test_SNPwithin_nonAssBD_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs4594580', 'rs2546001', 'rs2228006', 'rs1805794', 'rs2288242'])
        TestSearch.Add_Disease(['BD'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    # OutSide Gene
    def CREATE_Test_SNPoutside1(self):
        PREFIX = 'Test_SNPoutside1_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs233978', 'rs9965312', 'rs41464449', 'rs251292', 'rs7660291'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPoutside2(self):
        PREFIX = 'Test_SNPoutside2_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9887913', 'rs4775229', 'rs1125082', 'rs11768639', 'rs3753452'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPoutside3(self):
        PREFIX = 'Test_SNPoutside3_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs9887913', 'rs4775229', 'rs1125082', 'rs11768639', 'rs3753452'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPoutside_asso(self):
        PREFIX = 'Test_SNPoutside_asso_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs233978', 'rs9965312', 'rs251292', 'rs9887913', 'rs1125082'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return

    def CREATE_Test_SNPoutside_nonasso(self):
        PREFIX = 'Test_SNPoutside_nonasso_'

        TestSearch = Search()
        TestSearch.ChangeStatusTest(True)
        TestSearch.ImportData(['rs41464449', 'rs7660291', 'rs4775229', 'rs3753452', 'rs10120738'])
        TestSearch.Add_Relationship_Distance([['downstream', 500], ['upstream', 2000], 'intron', 'synon', 'exon', 'CDS', 'missense', 'nonsense', 'UTR-3', 'UTR-5', 'splice-site'])

        Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease = TestSearch.SearchData()
        self.ProcessCreateDataset(PREFIX, Result_Relate_InDisease, Result_Relate_NotInDisease, Result_Unrelate_InDisease, Result_Unrelate_NotInDisease)
        
        return


if __name__ == "__main__":
    createTestCase = CreateTestCase()

    testCase = TestCase()
    # testCase.Test_SNPoutside1()

