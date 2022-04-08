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

    # UPDATE NCBI
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
        """ Disease ใน Website หาย """

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
        """ Disease ใน Database ไม่ครบ """

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

        # self.CREATE_SEARCH_ALL_DATA_01()

        # self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_00()
        # self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_01()
        # self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_02()
        # self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_03()

        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_00()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_01()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_02()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_03()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_04()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_05()

        # self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_ALL()
        # self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_01()
        # self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_02()
        # self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_03()

        # self.CREATE_SEARCH_POSITION_WITH_CONDITION_ALL()
        # self.CREATE_SEARCH_POSITION_WITH_CONDITION_01()
        # self.CREATE_SEARCH_POSITION_WITH_CONDITION_02()

        # self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_ALL()   
        # self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_01()   
        # self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_02()

        # self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_ALL()
        # self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_01()
        # self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_02()
        # self.CREATE_SEARCH_RELATIONSHIP_DISTANCE_WITH_CONDITION_03()

        # self.CREATE_SEARCH_DISEASE_WITH_CONDITION_ALL()
        # self.CREATE_SEARCH_DISEASE_WITH_CONDITION_01()
        # self.CREATE_SEARCH_DISEASE_WITH_CONDITION_02()

        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_ALL()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_02()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_03()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_04()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_05()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_06()
        self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_07()

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

if __name__ == "__main__":
    createTestCase = CreateTestCase()

    testCase = TestCase()
    testCase.Get_AssociatedGeneOfDiseaseByPathway('Type 1 Diabetes Mellitus')

