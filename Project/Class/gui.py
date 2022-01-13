import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from Search import Search


class ChromosomeFilter(QDialog):
    def __init__(self):
        super(ChromosomeFilter, self).__init__()
        loadUi("D:\\NetAffx Project\\NetAffx-Project\\Project\\ui\\chromosomefilter.ui",self)
        self.ch_all.stateChanged.connect(self.clickboxall)
        self.Listcheckbox = [self.ch_all, self.ch_1, self.ch_2, self.ch_3, self.ch_4, self.ch_5, self.ch_6, self.ch_7, self.ch_8, self.ch_9, self.ch_10, self.ch_11, self.ch_12, self.ch_13
        , self.ch_14, self.ch_15, self.ch_16, self.ch_17, self.ch_18, self.ch_19, self.ch_20, self.ch_21, self.ch_22, self.ch_23]
        self.buttonBox.accepted.connect(self.displayFilter)
        self.display = []

    def clickboxall(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
            for i in self.Listcheckbox:
                i.setChecked(True)
        else:
            print('Unchecked')
            for i in self.Listcheckbox:
                i.setChecked(False)

    def displayFilter(self):
        for i in range(len(self.Listcheckbox)):
            if self.Listcheckbox[i].isChecked():
                self.display.append(i)

class PositionFilter(QDialog):
    def __init__(self):
        super(PositionFilter, self).__init__()
        loadUi("D:\\NetAffx Project\\NetAffx-Project\\Project\\ui\\PositionFilter.ui",self)
        self.display = []
        #self.comboBox.currentTextChanged.connect(self.combobox_changed)
        self.Add_btn_layout = QHBoxLayout()
        self.Add_btn_layout.addWidget(self.AddNewButton)
        self.AddNewButton.clicked.connect(self.AddNew)

        self.fillpos_btn_layout = QHBoxLayout()
        self.fillpos_btn_layout.addWidget(self.buttonBox, alignment=Qt.AlignRight)

        self.Layout = QVBoxLayout()
        self.Layout.addLayout(self.Add_btn_layout)
        self.Layout.addLayout(self.fillpos_btn_layout)
        self.setLayout(self.Layout)
        
        self.buttonBox.accepted.connect(self.PosFillDisplay)
    
    def combobox_changed(self):
        print(self.comboBox.currentText())
        state = self.comboBox.currentText()
        if state == "Between" :
            self.input1.setDisabled(False)
            self.input2.setDisabled(False)
        else:
            self.input1.setDisabled(False)
            self.input2.setDisabled(True)
    
    def AddNew(self):
        self.comboBox = QComboBox()
        self.comboBox.addItems(['Equal', 'Less than', 'More than', 'Between'])
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input2.setDisabled(True)
        self.confirm = QPushButton('Confirm')
        self.grid = QGridLayout()
        self.grid.addWidget(self.comboBox, 0, 0)
        self.grid.addWidget(self.input1, 0, 1)
        self.grid.addWidget(self.input2, 0, 2)
        self.grid.addWidget(self.confirm, 0, 3)
        self.Layout.addLayout(self.grid)

        self.comboBox.currentTextChanged.connect(self.combobox_changed)
        self.confirm.clicked.connect(self.confirmcondi)
        
    def confirmcondi(self):
        state = self.comboBox.currentText()
        val1 = self.input1.text()
        val2 = self.input2.text()
        self.input1.setDisabled(True)
        self.input2.setDisabled(True)
        self.comboBox.setDisabled(True)
        self.confirm.setDisabled(True)
        condi = [state, val1, val2]
        self.display.append(condi)
    
    def PosFillDisplay(self):
        print(self.display)
        self.close()

class DistanceFilter(QDialog):
    def __init__(self):
        super(DistanceFilter, self).__init__()
        loadUi("D:\\NetAffx Project\\NetAffx-Project\\Project\\ui\\DistanceFilter.ui",self)
        self.display = []
        self.Add_btn_layout = QHBoxLayout()
        self.Add_btn_layout.addWidget(self.Add_btn)
        self.Add_btn.clicked.connect(self.AddNew)

        self.fildist_btn_layout = QHBoxLayout()
        self.fildist_btn_layout.addWidget(self.buttonBox, alignment=Qt.AlignRight)

        self.Layout.addLayout(self.Add_btn_layout)
        self.Layout.addLayout(self.fildist_btn_layout)
        self.setLayout(self.Layout)
        
        # self.buttonBox.accepted.connect(self.PosFillDisplay)
    
    def combobox_changed(self):
        print(self.comboBox.currentText())
        state = self.comboBox.currentText()
        if state == "Between" :
            self.input1.setDisabled(False)
            self.input2.setDisabled(False)
        else:
            self.input1.setDisabled(False)
            self.input2.setDisabled(True)
    
    def AddNew(self):
        self.comboBox = QComboBox()
        self.comboBox.addItems(['Equal', 'Less than', 'More than', 'Between'])
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input2.setDisabled(True)
        self.confirm = QPushButton('Confirm')
        self.grid = QGridLayout()
        self.grid.addWidget(self.comboBox, 0, 0)
        self.grid.addWidget(self.input1, 0, 1)
        self.grid.addWidget(self.input2, 0, 2)
        self.grid.addWidget(self.confirm, 0, 3)
        self.Layout.addLayout(self.grid)
        self.comboBox.currentTextChanged.connect(self.combobox_changed)
        self.confirm.clicked.connect(self.confirmcondi)
    
    def confirmcondi(self):
        state = self.comboBox.currentText()
        val1 = self.input1.text()
        val2 = self.input2.text()
        self.input1.setDisabled(True)
        self.input2.setDisabled(True)
        self.comboBox.setDisabled(True)
        self.confirm.setDisabled(True)
        condi = [state, val1, val2]
        self.display.append(condi)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("D:\\NetAffx Project\\NetAffx-Project\\Project\\ui\\maingui.ui",self)
        self.browse.clicked.connect(self.browsefiles)
        self.search.clicked.connect(self.searchsnp)
        self.toolchromosome.clicked.connect(self.filterchromosome)
        self.toolposition.clicked.connect(self.filterposition)
        self.tooldistance.clicked.connect(self.filterdistance)
        self.filecsvname = ''
        

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\\NetAffx Project\\NetAffx-Project')
        self.filename.setText(fname[0])
        self.filecsvname = fname[0]
    
    def filterchromosome(self):
        print('clickchromosome')
        filterChro = ChromosomeFilter()
        filterChro.exec_()
        text_chromofilter = ''
        for i in filterChro.display:
            text_chromofilter = text_chromofilter + str(i) + ', ' 
        self.Chromo_display.setText(text_chromofilter[:-2])
    
    def filterposition(self):
        print('clickposition')
        filterPos = PositionFilter()
        filterPos.exec_()
        text_PosFilter = ''
        for i in filterPos.display:
            for j in i:
                text_PosFilter = text_PosFilter + " " + str(j)
            text_PosFilter = text_PosFilter + ','
        self.Posi_display.setText(text_PosFilter)
    
    def filterdistance(self):
        print('clickdistance')
        filterPos = DistanceFilter()
        filterPos.exec_()
        
    def searchsnp(self):
        print("textSNP :", self.inputSNP_display.toPlainText())
        print("csvSNPFile :", self.filename.text())
        print("Chromosome :", self.Chromo_display.toPlainText())
        print("Position :", self.Posi_display.toPlainText())
        print("GeneChip :", self.GeneChipBox.currentText())
        print("GeneID :", self.GeneID_display.toPlainText())
        print("GeneSymbol :", self.genesym_display.toPlainText())
        print("Distance :", self.dist_display.toPlainText())

        SearchFunction = Search()
        SearchFunction.Add_RSID_PROBE_SET(self.inputSNP_display.toPlainText())
    

app=QApplication(sys.argv)
mainwindow=MainWindow()
mainwindow.show()
sys.exit(app.exec_())