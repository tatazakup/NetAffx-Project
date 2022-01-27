from Initialization import Database, FilePath
from Ncbi import Ncbi
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

        if check is True:
            print('Test', str(TestName), 'is correct')
        else:
            print('Test', str(TestName), 'is incorrect')

    def CheckInputData(self, newData_FD, newDATA_NFD, FilenameFD, FilenameNFD):
        if newData_FD != []:
            LIST_FD_FROM_FILE = newData_FD
        else:
            File_FD = self.ReadCSVFile(FilenameFD)
            LIST_FD_FROM_FILE = [[row[col] for col in File_FD.columns] for row in File_FD.to_dict('records')]
        
        if newDATA_NFD != []:
            LIST_NFD_FROM_FILE = newDATA_NFD
        else:
            File_NFD = self.ReadCSVFile(FilenameNFD)
            LIST_NFD_FROM_FILE = [[row[col] for col in File_NFD.columns] for row in File_NFD.to_dict('records')]

        return LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE

    def SEARCH_ALL_DATA_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_ALL_DATA_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_ALL_DATA_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_ALL_DATA_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_ALL_DATA_01_NFD')

        return

    def SEARCH_GENE_ID_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_GeneID([2272])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'Search_GENE_ID_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'Search_GENE_ID_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_GENE_ID_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_GENE_ID_WITH_CONDITION_01_NFD')

        return

    def SEARCH_GENE_SYMBOL_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_GeneSymbol(['RFPL4B'])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'Search_GENE_SYMBOL_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'Search_GENE_SYMBOL_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_GENE_SYMBOL_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_GENE_SYMBOL_WITH_CONDITION_01_NFD')

        return

    def SEARCH_CHROMOSOME_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Chromosome([1])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'Search_CHROMOSOME_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'Search_CHROMOSOME_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_CHROMOSOME_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_CHROMOSOME_WITH_CONDITION_01_NFD')

        return

    def SEARCH_GENESHIP_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Geneship(1)

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_GENESHIP_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_GENESHIP_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_GENESHIP_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_GENESHIP_WITH_CONDITION_01_NFD')

        return
    
    def SEARCH_DISTANCE_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Distance([ [0, 1204066] ])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_DISTANCE_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_DISTANCE_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_DISTANCE_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_DISTANCE_WITH_CONDITION_01_NFD')

        return

    def SEARCH_RELATIONSHIP_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Relationship(['upstream'])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_RELATIONSHIP_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_RELATIONSHIP_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_RELATIONSHIP_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_RELATIONSHIP_WITH_CONDITION_01_NFD')

        return

    def SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Geneship(1)

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_GENESHIP_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_GENESHIP_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_GENESHIP_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_GENESHIP_WITH_CONDITION_01_NFD')

        return

    def SEARCH_DISEASE_WITH_CONDITION_01(self, newData_FD = [], newDATA_NFD = []):
        """Test search all data with out condition"""

        self.TestSearch.Add_Disease(['T1D'])

        PathToTestCase_FD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_DISEASE_WITH_CONDITION_01_FD.csv'
        PathToTestCase_NFD = self.Allpath.GetPathToTestCase() + '/' +  'SEARCH_DISEASE_WITH_CONDITION_01_NFD.csv'

        LIST_FD_FROM_FILE, LIST_NFD_FROM_FILE = self.CheckInputData(newData_FD, newDATA_NFD, PathToTestCase_FD, PathToTestCase_NFD)
        RESULT_FD, RESULT_NFD = self.TestSearch.SearchData()

        self.CheckAccuracy(RESULT_FD, LIST_FD_FROM_FILE, 'SEARCH_DISEASE_WITH_CONDITION_01_FD')
        self.CheckAccuracy(RESULT_NFD, LIST_NFD_FROM_FILE, 'SEARCH_DISEASE_WITH_CONDITION_01_NFD')

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
        disease = Disease()
        disease.UpdateDiseaseDataset()
        
        return

class CreateTestCase():
    def __init__(self):
        self.listcolumns_FD = ['RSID', 'PROBESET_ID', 'CHROMOSOME', 'POSITION',
        'SOURCE_GENESHIP', 'RELATIONSHIP', 'DISTANCE', 'GENE_SYMBOL', 'GENE_ID', 
        'OTHER_SYMBOL', 'DISEASE_NAME', 'DISEASE_ABBREVIATION', 'MATCH_BY']

        self.listcolumns_NFD = ['RSID', 'PROBESET_ID', 'CHROMOSOME', 'POSITION',
        'SOURCE_GENESHIP', 'RELATIONSHIP', 'DISTANCE', 'GENE_SYMBOL', 'GENE_ID', 
        'OTHER_SYMBOL']

        self.TestSearch = Search()
        self.allpath = FilePath()

        # self.CREATE_SEARCH_ALL_DATA_01()
        # self.CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_01()
        # self.CREATE_SEARCH_GENESHIP_WITH_CONDITION_01()
        # self.CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01()
        # self.CREATE_SEARCH_DISEASE_WITH_CONDITION_01()
        # self.CREATE_SEARCH_GENE_ID_WITH_CONDITION_01()
        # self.CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_01()
        # self.CREATE_SEARCH_DISTANCE_WITH_CONDITION_01()
        self.CREATE_SEARCH_RELATIONSHIP_WITH_CONDITION_01()
        return

    def ImportDataTo_FD(self, fileName, data):
        path_output = self.allpath.GetPathToTestCase() + '/' + fileName
        df = pd.DataFrame(data,columns = self.listcolumns_FD)
        df.to_csv(path_output,index=False)

    def ImportDataTo_NFD(self, fileName, data):
        path_output = self.allpath.GetPathToTestCase() + '/' + fileName
        df = pd.DataFrame(data,columns = self.listcolumns_NFD)
        df.to_csv(path_output,index=False)

    def CREATE_SEARCH_ALL_DATA_01(self):
        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_ALL_DATA_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_ALL_DATA_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_GENE_ID_WITH_CONDITION_01(self):

        self.TestSearch.Add_GeneID([2272])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_GENE_ID_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_GENE_ID_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_GENE_SYMBOL_WITH_CONDITION_01(self):

        self.TestSearch.Add_GeneSymbol(['RFPL4B'])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_GENE_SYMBOL_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_GENE_SYMBOL_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_CHROMOSOME_WITH_CONDITION_01(self):

        self.TestSearch.Add_Chromosome([1])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_CHROMOSOME_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_CHROMOSOME_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_GENESHIP_WITH_CONDITION_01(self):

        self.TestSearch.Add_Geneship(1)

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_GENESHIP_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_GENESHIP_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_DISTANCE_WITH_CONDITION_01(self):

        self.TestSearch.Add_Distance([ [0, 1204066] ])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_DISTANCE_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_DISTANCE_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_RELATIONSHIP_WITH_CONDITION_01(self):

        self.TestSearch.Add_Relationship(['upstream'])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_RELATIONSHIP_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_RELATIONSHIP_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01(self):

        self.TestSearch.Add_source_website(1)

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_SOURCE_WEBSITE_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

    def CREATE_SEARCH_DISEASE_WITH_CONDITION_01(self):
        self.TestSearch.Add_Disease(['T1D'])

        Results_FD, Result_NFD = self.TestSearch.SearchData()
        self.ImportDataTo_FD('SEARCH_DISEASE_WITH_CONDITION_01_FD.csv', Results_FD)
        self.ImportDataTo_NFD('SEARCH_DISEASE_WITH_CONDITION_01_NFD.csv', Result_NFD)
        return

if __name__ == "__main__":
    # createTestCase = CreateTestCase()

    testCase = TestCase()
    testCase.UPDATE_NCBI_WITH_CONDITION_03()