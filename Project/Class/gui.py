from ast import Return
from calendar import c
from cgi import test
from msilib.schema import File
from re import S
import re
import string
import sys
import os
from threading import Thread
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from click import progressbar
from Search import Search
import pandas as pd
from ncbi import Ncbi
from Disease import Disease
from pathway import PathwayDataFromKEGG, PathwayOfDis
from Initialization import Database, FilePath, MetaData
from AnnotationFile import Manage_AnnotationFile
from mapSNPwithDisease import mapSNP_Disease
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class CreateInitailDatabase(QDialog, FilePath):
    def __init__(self):
        super(CreateInitailDatabase, self).__init__()
        loadUi(self.GetPathToUI() + "/createinitial.ui",self)
        self.SchemaName = ''
        self.confirm_button.clicked.connect(self.clickconfirm)

    def closeEvent(self, event):
        self.reject()

    def clickconfirm(self):
        self.SchemaName = self.SchemaInput.text()
        self.close()

class ConfigDatabase(QDialog, FilePath):
    def __init__(self):
        super(ConfigDatabase, self).__init__()
        loadUi(self.GetPathToUI() + "/configdatabase.ui",self)

        objectConfig = MetaData()
        dataInConfig = self.TryFetchDataOnMetaData(objectConfig, 'config')

        self.HostIP = dataInConfig['database']['hostIP']
        self.SchemaName = dataInConfig['database']['database']
        self.Username = dataInConfig['database']['authentication']['user']
        self.Password = dataInConfig['database']['authentication']['password']
        self.HostInput.setText(self.HostIP)
        self.SchemaInput.setText(self.SchemaName)
        self.UserInput.setText(self.Username)
        self.PassInput.setText(self.Password)

        self.confirm_button.clicked.connect(self.clickconfirm)

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def closeEvent(self, event):
        self.reject()

    def clickconfirm(self):
        self.HostIP = self.HostInput.text()
        self.SchemaName = self.SchemaInput.text()
        self.Username = self.UserInput.text()
        self.Password = self.PassInput.text()
        if self.HostIP == '' or self.SchemaName == '' or self.Username == '' or self.Password == '' :
            QMessageBox.about(self, 'ERROR', "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        self.close()

class ChromosomeFilter(QDialog, FilePath):
    def __init__(self, oldCondition):
        super(ChromosomeFilter, self).__init__()
        loadUi(self.GetPathToUI() + "/chromosomefilter.ui",self)
        self.Listcheckbox = [self.ch_all, self.ch_1, self.ch_2, self.ch_3, self.ch_4, self.ch_5, self.ch_6, self.ch_7, self.ch_8, self.ch_9, self.ch_10, self.ch_11, self.ch_12, self.ch_13
        , self.ch_14, self.ch_15, self.ch_16, self.ch_17, self.ch_18, self.ch_19, self.ch_20, self.ch_21, self.ch_22, self.ch_X]
        
        # Old value
        self.list_condition = []
        listOldCondition = oldCondition.split(', ')
        for stringValue in listOldCondition:
            if stringValue == '':
                continue
            elif stringValue == "'X'":
                self.list_condition.append('X')
            else: 
                self.list_condition.append(int(stringValue))

        # Set Function of button
        self.ch_all.stateChanged.connect(self.clickboxall)
        self.confirm_button.clicked.connect(self.confirm)
    
    def closeEvent(self, event):
        self.reject()

    def clickboxall(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
            for i in self.Listcheckbox:
                i.setChecked(True)
        else:
            print('Unchecked')
            for i in self.Listcheckbox:
                i.setChecked(False)

    def confirm(self):
        self.list_condition = []
        for i in range(len(self.Listcheckbox)):
            if self.Listcheckbox[i].isChecked():
                if i == 23 :
                    self.list_condition.append('X')
                else :
                    self.list_condition.append(i)
        self.close()

class PositionFilter(QDialog, FilePath):
    def __init__(self):
        super(PositionFilter, self).__init__()
        loadUi(self.GetPathToUI() + "/PositionFilter.ui",self)
        self.display = []

        self.Add_btn_layout = QHBoxLayout()
        self.Add_btn_layout.addWidget(self.AddNewButton)
        self.Add_btn_layout.addWidget(self.buttonBox, alignment=Qt.AlignRight)
        self.AddNewButton.clicked.connect(self.AddNew)
        self.Layout = QVBoxLayout()
        self.Layout.addLayout(self.Add_btn_layout)
        self.setLayout(self.Layout)
        
        # set function button
        self.buttonBox.accepted.connect(self.PosFillDisplay)
        self.buttonBox.rejected.connect(self.close)

        # disable close button
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    
    def closeEvent(self, event):
        self.display = []

    def close(self):
        self.display = []
        self.reject()

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
        self.confirm.clicked.connect(self.confirmcondition)
        
    def confirmcondition(self):
        state = self.comboBox.currentText()
        val1 = self.input1.text()
        val2 = self.input2.text()
        if state == 'Equal':
            try:
                float(val1)
            except:
                QMessageBox.about(self, 'ERROR', "Cannot input value as string")
                return
            condition_num = 0
            condi = [condition_num, float(val1)]

        elif state == 'Less than':
            condition_num = 1
            condi = [condition_num, float(val1)]
        elif state == 'More than':
            condition_num = 2
            condi = [condition_num, float(val1)]
        elif state == 'Between':
            condition_num = 3
            condi = [condition_num, float(val1), float(val2)]
        self.input1.setDisabled(True)
        self.input2.setDisabled(True)
        self.comboBox.setDisabled(True)
        self.confirm.setDisabled(True)
        self.display.append(condi)

    def PosFillDisplay(self):
        self.reject()

class RelationshipFilter(QDialog, FilePath):
    def __init__(self):
        super(RelationshipFilter, self).__init__()
        loadUi(self.GetPathToUI() + "/RelationshipFilter3.ui",self)
        self.Listcheckbox = [self.checkBox_upstream, self.checkBox_downstream, self.checkBox_intron,
                            self.checkBox_exon, self.checkBox_synon,self.checkBox_CDS, 
                            self.checkBox_missense, self.checkBox_nonsense,
                            self.checkBox_UTR3, self.checkBox_UTR5, self.checkBox_spicesite]
        self.Condition_RelDist = []
        
        # Set Function of each button
        self.buttonBox.accepted.connect(self.Confirm)
        self.buttonBox.rejected.connect(self.Cancle)
        self.checkBox_upstream.stateChanged.connect(self.ClickUpstream)
        self.checkBox_downstream.stateChanged.connect(self.ClickDownstream)
    
    def ClickUpstream(self, state):
        if state == QtCore.Qt.Checked:
            self.Input_upstream.setEnabled(True)
        else:
            self.Input_upstream.clear()
            self.Input_upstream.setEnabled(False)

    def ClickDownstream(self, state):
        if state == QtCore.Qt.Checked:
            self.Input_downstream.setEnabled(True)
        else:
            self.Input_downstream.clear()
            self.Input_downstream.setEnabled(False)

    def Confirm(self):
        for i in range(len(self.Listcheckbox)):
            if self.Listcheckbox[i].isChecked():
                relationship_name = self.Listcheckbox[i].objectName()[9:]
                if relationship_name == 'upstream'  :
                    condition_group = []
                    distance_value = self.Input_upstream.text()
                    if distance_value == '':
                        QMessageBox.about(self, 'ERROR', "Please add distance of upstream!")
                        return
                    condition_group.extend([relationship_name, float(distance_value)])
                    self.Condition_RelDist.append(condition_group)
                elif relationship_name == 'downstream':
                    condition_group = []
                    distance_value = self.Input_downstream.text()
                    if distance_value == '':
                        QMessageBox.about(self, 'ERROR', "Please add distance of downstream!")
                        return
                    condition_group.extend([relationship_name, float(distance_value)])
                    self.Condition_RelDist.append(condition_group)
                else:
                    self.Condition_RelDist.append(relationship_name)
        print(self.Condition_RelDist)

    def Cancle(self):
        self.close()

class DiseaseFilter(QDialog, FilePath):
    def __init__(self):
        super(DiseaseFilter, self).__init__()
        loadUi(self.GetPathToUI() + "/DiseaseFilter4.ui",self)
        self.Listcheckbox = [self.BD, self.CAD, self.CD, self.HT, self.RA, self.T1D, self.T2D]
        self.Condition_Distance = []
        
        # Set Function of each button
        # self.buttonBox.accepted.connect(self.Confirm)
        # self.buttonBox.rejected.connect(self.Cancle)
        self.confirm_button.clicked.connect(self.Confirm)
        self.All.stateChanged.connect(self.clickboxall)
    
    def closeEvent(self, event):
        self.Condition_Distance = []

    def clickboxall(self, state):
        if state == QtCore.Qt.Checked:
            for i in self.Listcheckbox:
                i.setChecked(True)
                i.setEnabled(False)
        else:
            for i in self.Listcheckbox:
                i.setChecked(False)
                i.setEnabled(True)
    
    def Confirm(self):
        for i in range(len(self.Listcheckbox)):
            if self.Listcheckbox[i].isChecked():
                Disease_name = self.Listcheckbox[i].objectName()
                self.Condition_Distance.append(Disease_name)
        self.reject()

class SQLdialog(QDialog):
    def __init__(self):
        super(SQLdialog, self).__init__()
        loadUi(self.GetPathToUI() + "/SQLCommand.ui",self)
        self.searchsql_Button.clicked.connect(self.getCommand)
        self.command = ''
    
    def getCommand(self):
        # self.command = self.textSQL.toPlainText()
        pass


class pgb_Thread(QThread):

    send_signal = pyqtSignal(int, int , int)

    def __init__(self):
        super(pgb_Thread, self).__init__()

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def run(self):
        
        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
        time.sleep(2)
        while True:
            dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
            amountUniqueGene = dataInMapSnpWithNcbi['technical']['updateMeta']['amountUniqueGene']
            amountOfFinished = dataInMapSnpWithNcbi['technical']['updateMeta']['amountOfFinished']
            self.send_signal.emit(amountOfFinished, amountUniqueGene - amountOfFinished, amountUniqueGene) 
            print('sended')              

            if dataInMapSnpWithNcbi['technical']['updateMeta']['status'] != 1:
                return
            time.sleep(1)
            print('amountOfFinished :', amountOfFinished, '| amountUniqueGene :', amountUniqueGene)
    
    def stop(self):
        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
        dataInMapSnpWithNcbi['technical']['updateMeta']['status'] = 0
        dataInMapSnpWithNcbi['technical']['updateMeta']['amountUniqueGene'] = 0
        dataInMapSnpWithNcbi['technical']['updateMeta']['amountOfFinished'] = 0
        objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
        self.terminate()

    def pause(self):
        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
        dataInMapSnpWithNcbi['technical']['updateMeta']['status'] = 2
        objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)
        self.terminate()
        
class NCBI_Thread(QThread, FilePath):

    def __init__(self):
        super(NCBI_Thread, self).__init__()
        # FilePath.__init__()
        self.is_running = True

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def run(self):
        # NCBI process
        ncbi = Ncbi(1)
        ncbi.UpdateNcbiInformation()
    
class UpdateNCBI(QWidget, FilePath):
    def __init__(self):
        super().__init__()
        loadUi(self.GetPathToUI() + "/WindowNCBI.ui",self)
        self.start_btn.clicked.connect(self.doStart)
        self.pause_btn.clicked.connect(self.doPause)
        self.cancel_btn.clicked.connect(self.doCancel)

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def doStart(self):
        textbtn = self.start_btn.text()
        
        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
        if textbtn == 'CONTINUE': dataInMapSnpWithNcbi['technical']['updateMeta']['status'] = 3
        else: dataInMapSnpWithNcbi['technical']['updateMeta']['status'] = 1
        objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)

        self.worker = NCBI_Thread()
        self.worker.start()

        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.start_btn.setEnabled(False)
        self.start_btn.setText("CONTINUE")
        self.start_btn.setStyleSheet("background-color: rgb(85, 255, 255);")

        self.worker_pgb = pgb_Thread()
        self.worker_pgb.start()
        self.worker_pgb.send_signal.connect(self.SendSignal)
    
    def doPause(self):
        self.worker_pgb.pause()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
    
    def doCancel(self):
        self.worker_pgb.stop()
        self.close()
    
    def SendSignal(self ,intStart, intStop, valueStop):
        if valueStop != 0:
            self.updated_space.setText(str(intStart))
            self.remaining_space.setText(str(intStop))
            self.progressBar.setValue(intStart*100/valueStop)


class pgb_Dis_Thread(QThread):
    send_signal = pyqtSignal(int, int , int, str)
    
    def __init__(self):
        super(pgb_Dis_Thread, self).__init__()
    
    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def run(self):
        objectDisease = MetaData()
        diseaseInfo = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
        time.sleep(2)
        while True:
            diseaseInfo = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
            diseaseName = diseaseInfo['technical']['diseaseStatus']['updateMeta']['diseaseName']
            indexDisease = int(diseaseInfo['technical']['diseaseStatus']['updateMeta']['diseaseID'])
            amountDisease = diseaseInfo['technical']['diseases'][indexDisease - 1]['updateMeta']['amountDisease']
            amountOfFinished = diseaseInfo['technical']['diseases'][indexDisease - 1]['updateMeta']['amountOfFinished']
            self.send_signal.emit(amountOfFinished, amountDisease - amountOfFinished, amountDisease, diseaseName) 
            print('sended')              

            if diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] != 1:
                return
            time.sleep(1)
    
    def stop(self):
        objectDisease = MetaData()
        diseaseInfo = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
        diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] = 0
        diseaseInfo['technical']['diseaseStatus']['updateMeta']['diseaseID'] = 0
        diseaseInfo['technical']['diseaseStatus']['updateMeta']['diseaseName'] = ""
        objectDisease.SaveManualUpdateMetadata(diseaseInfo)
        self.terminate()

    def pause(self):
        objectDisease = MetaData()
        diseaseInfo = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
        diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] = 2
        objectDisease.SaveManualUpdateMetadata(diseaseInfo)
        self.terminate()

class DIS_Thread(QThread):
    def __init__(self):
        super(DIS_Thread, self).__init__()

    def run(self):
        disease = Disease()
        disease.UpdateDiseaseDataset()

class UpdateDisease(QWidget, FilePath):
    def __init__(self):
        super().__init__()
        loadUi(self.GetPathToUI() + "/WindowDISEASE.ui",self)
        self.start_btn.clicked.connect(self.doStart)
        self.pause_btn.clicked.connect(self.doPause)
        self.cancel_btn.clicked.connect(self.doCancel)

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def doStart(self):
        textbtn = self.start_btn.text()
        
        objectDisease = MetaData()
        diseaseInfo = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
        if textbtn == 'CONTINUE': diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] = 3
        else: diseaseInfo['technical']['diseaseStatus']['updateMeta']['status'] = 1
        objectDisease.SaveManualUpdateMetadata(diseaseInfo)

        # Run thread
        self.worker = DIS_Thread()
        self.worker.start()

        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.start_btn.setEnabled(False)
        self.start_btn.setText("CONTINUE")
        self.start_btn.setStyleSheet("background-color: rgb(85, 255, 255);")
        
        time.sleep(5)
        self.worker_pgb = pgb_Dis_Thread()
        self.worker_pgb.start()
        self.worker_pgb.send_signal.connect(self.SendSignal)
    
    def doPause(self):
        self.worker_pgb.pause()
        self.pause_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        
    def doCancel(self):
        self.worker_pgb.stop()
        self.close()
    
    def SendSignal(self ,intStart, intStop, valueStop, tagname):
        print('     reciev signal',intStart, intStop, valueStop, tagname)

        self.disease_space.setText(tagname)
        if valueStop != 0:
            self.updated_space.setText(str(intStart))
            self.remaining_space.setText(str(intStop))
            self.progressBar.setValue(intStart*100/valueStop)
        else:
            self.updated_space.setText("0")
            self.remaining_space.setText("0")
            self.progressBar.setValue(0)


class pgb_Pathway_Thread(QThread):
    send_signal = pyqtSignal(int, int , int, str)
    
    def __init__(self):
        super(pgb_Pathway_Thread, self).__init__()

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def run(self):
        objectDisease = MetaData()
        while True:
            pathwayinfo = self.TryFetchDataOnMetaData(objectDisease, 'Pathway')
            statusvalue = pathwayinfo['Status']['textStatus']
            amountDisease = pathwayinfo['Status']['amountState']
            amountOfFinished = pathwayinfo['Status']['amountOfFinished']
            self.send_signal.emit(amountOfFinished, amountDisease - amountOfFinished, amountDisease, statusvalue) 

    def stop(self):
        self.terminate()

class Pathway_Thread(QThread):
    def __init__(self):
        super(Pathway_Thread, self).__init__()

    def run(self):
        Data_Pathway = PathwayDataFromKEGG()
        Data_Pathway.GetGenePathway()
        Pathway_Dis = PathwayOfDis()
        Pathway_Dis.FetchPathwayEachDisease()
        Pathway_Dis.Find_GeneInPathwayOfDisease(Data_Pathway.listpathway)
        Pathway_Dis.SaveGenePathway2db()

    def stop(self):
        self.terminate()

class UpdatePathway(QWidget, FilePath):
    def __init__(self):
        super().__init__()
        loadUi(self.GetPathToUI() + "/WindowPathway.ui",self)
        self.start_btn.clicked.connect(self.doStart)
        self.cancel_btn.clicked.connect(self.doCancel)
    
    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def doStart(self):
        # Run thread
        self.worker = Pathway_Thread()
        self.worker.start()

        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        # Run progressbar thread
        self.worker_pgb = pgb_Pathway_Thread()
        self.worker_pgb.start()
        self.worker_pgb.send_signal.connect(self.SendSignal)

    def doCancel(self):
        objectDisease = MetaData()
        pathwayinfo = self.TryFetchDataOnMetaData(objectDisease, 'Pathway')
        pathwayinfo['Status']['textStatus'] = ""
        pathwayinfo['Status']['amountOfFinished'] = 0
        objectDisease.SaveManualUpdateMetadata(pathwayinfo)
        self.worker.stop()
        self.worker_pgb.stop()
        self.close()
    
    def SendSignal(self ,intStart, intStop, valueStop, status):
        print('     reciev signal',intStart, intStop, valueStop, status)
        self.status_space.setText(status)
        if valueStop != 0:
            self.progressBar.setValue(intStart*100/valueStop)
        else:
            self.progressBar.setValue(0)
        if intStart == valueStop:
            self.cancel_btn.setText("Finish")
            self.cancel_btn.setStyleSheet("background-color: rgb(85, 255, 255);")


class SelectSearch(QDialog, FilePath):
    def __init__(self):
        super(SelectSearch, self).__init__()
        loadUi(self.GetPathToUI() + "/SelectSearch.ui",self)
        self.buttonBox.accepted.connect(self.OpenResult)
        self.All.stateChanged.connect(self.clickboxall)
        self.Listcheckbox = [self.All, self.CHROMOSOME, self.DISEASE_ABBREVIATION, self.DISEASE_NAME, 
                            self.DISTANCE, self.GENE_ID, self.GENE_SYMBOL, self.MATCH_BY, 
                            self.OTHER_SYMBOL, self.POSITION, self.PROBESET_ID, self.RELATIONSHIP, 
                            self.RSID, self.SOURCE_GENESHIP]
        self.selected = []
    
    def clickboxall(self, state):
        if state == QtCore.Qt.Checked:
            print('All Checked')
            for i in self.Listcheckbox:
                i.setChecked(True)
        else:
            print('All Unchecked')
            for i in self.Listcheckbox:
                i.setChecked(False)

    def OpenResult(self):
        for i in range(len(self.Listcheckbox)):
            if self.Listcheckbox[i].isChecked():
                SelectedAttr = self.Listcheckbox[i].objectName()
                self.selected.append(SelectedAttr)

class ShowSNP(QDialog, FilePath):
    def __init__(self, dataframe):
        super(ShowSNP, self).__init__()
        loadUi(self.GetPathToUI() + "/ShowSNP.ui",self)
        self.df = dataframe
        self.showSNP_model = pandasModel( self.df)
        self.tableView.setModel(self.showSNP_model)
        self.pushButton.clicked.connect(self.export)
    
    def export(self):
        default_dir ="/home/qt_user/name"
        default_filename = os.path.join(default_dir)
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", default_filename, "Comma-Separated Value (*.csv)"
        )
        if filename:
            print(filename)
            self.df.to_csv(filename,index=False)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None    

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



class MainWindow(QMainWindow, FilePath):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi(self.GetPathToUI() + "/maingui.ui",self)

        # Connect Cliked to Function
        self.actionCreate.triggered.connect(self.createInitial)
        self.actionUpdate_NCBI.triggered.connect(self.clickUpdateNcbi)
        self.actionUpdate_Disease.triggered.connect(self.clickUpdateDis)
        self.actionUpdate_Pathway.triggered.connect(self.clickUpdatePathway)
        self.actionDatabase.triggered.connect(self.ConfigDatabase)

        self.browse.clicked.connect(self.browsefiles)
        self.toolchromosome.clicked.connect(self.filterchromosome)
        self.toolposition.clicked.connect(self.filterposition)
        self.toolrelationship.clicked.connect(self.filterrelationship)
        self.tooldisease.clicked.connect(self.filterdisease)
        
        self.searchSQL_btn.clicked.connect(self.SearchSQL)
        self.search.clicked.connect(self.searchsnp)

        self.filecsvname = ''
        self.SearchFunction = Search()
        self.FilterDistance = []
    
    def browsefiles(self):
        # Call Dialog Gui
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:\\')
        if fname != "":
            self.filename.setText(fname[0])
            self.filecsvname = fname[0]
            self.dfsnp_csv = pd.read_csv(self.filecsvname, header=None)
            self.listsnp_csv = self.dfsnp_csv[0].tolist()
            
            # Create Str from List to Display on GUI
            text_listsnp = str(self.listsnp_csv)
            self.inputSNP_display.setText(text_listsnp[1:-1])
    
    def SearchSQL(self):
        self.SQLcom = SQLdialog()
        self.SQLcom.exec_()
        print(self.SQLcom.command)

    def clickUpdateNcbi(self):
        self.Update_NCBI = UpdateNCBI()
        self.Update_NCBI.show()
    
    def clickUpdateDis(self):
        self.Update_DIS = UpdateDisease()
        self.Update_DIS.show()

    def clickUpdatePathway(self):
        self.Update_Pathway = UpdatePathway()
        self.Update_Pathway.show()

    def TryFetchDataOnMetaData(self, objectMetaData, metaname):
        isCompleted = False
        while ( isCompleted == False):
            try:       
                dataInMetaData = objectMetaData.ReadMetadata(metaname)
                isCompleted = True
            except:
                time.sleep(0.1)
                pass
        return dataInMetaData

    def createInitial(self):
        # Call Dialog GUI
        self.CallCreate = CreateInitailDatabase()
        self.CallCreate.exec_()

        database = Database()
        database.InitialDatabase(self.CallCreate.SchemaName)

        manage_AnnotationFile = Manage_AnnotationFile()
        listAnnotation = manage_AnnotationFile.SeparateGene()
        manage_AnnotationFile.SaveSNP(listAnnotation)

        objectMapSnpWithNcbi = MetaData()
        dataInMapSnpWithNcbi = self.TryFetchDataOnMetaData(objectMapSnpWithNcbi, 'MapSnpWithNcbi')
        dataInMapSnpWithNcbi['technical']['createMeta']['status'] = 1
        objectMapSnpWithNcbi.SaveManualUpdateMetadata(dataInMapSnpWithNcbi)

        ncbi = Ncbi(1)
        ncbi.CreateNcbiInformation()

        objectDisease = MetaData()
        dataInDisease = self.TryFetchDataOnMetaData(objectDisease, 'Disease')
        dataInDisease['technical']['diseaseStatus']['createMeta']['status'] = 1
        objectDisease.SaveManualUpdateMetadata(dataInDisease)

        disease = Disease()
        disease.CreateDiseaseDataset()

        Data_Pathway = PathwayDataFromKEGG()
        Data_Pathway.GetGenePathway()
        Pathway_Dis = PathwayOfDis()
        Pathway_Dis.FetchPathwayEachDisease()
        Pathway_Dis.Find_GeneInPathwayOfDisease(Data_Pathway.listpathway)
        Pathway_Dis.SaveGenePathway2db()

        matching = mapSNP_Disease()
        matching.MapBoth()

    def ConfigDatabase(self):
        # Call Dialog GUI
        self.CallConfig = ConfigDatabase()
        self.CallConfig.exec_()

        objectConfig = MetaData()
        dataInConfig = self.TryFetchDataOnMetaData(objectConfig, 'config')
        dataInConfig['database']['hostIP'] = self.CallConfig.HostIP
        dataInConfig['database']['database'] = self.CallConfig.SchemaName
        dataInConfig['database']['authentication']['user'] = self.CallConfig.Username
        dataInConfig['database']['authentication']['password'] = self.CallConfig.Password
        objectConfig.SaveManualUpdateMetadata(dataInConfig)

        print(self.CallConfig.HostIP)
        print(self.CallConfig.SchemaName)
        print(self.CallConfig.Username)
        print(self.CallConfig.Password)

    def filterchromosome(self):
        # Get old value
        oldCondition = self.Chromo_display.toPlainText()

        # Call Dialog GUI
        self.filterChro = ChromosomeFilter(oldCondition)
        self.filterChro.exec_()
        
        # Create Str from List to Display on GUI
        text_chromofilter = str(self.filterChro.list_condition)
        self.Chromo_display.setText(text_chromofilter[1:-1])

        # Add FilterCondition To Search
        self.SearchFunction.Add_Chromosome(self.filterChro.list_condition)
    
    def filterposition(self):
        # Call Dialog GUI
        self.filterPos = PositionFilter()
        self.filterPos.exec_()
        
        # Create Str from List to Display on GUI
        text_PosFilter = str(self.filterPos.display)
        self.Posi_display.setText(text_PosFilter[1:-1])

        self.SearchFunction.Add_Position(self.filterPos.display)
    
    def filterrelationship(self):
        self.filterRel = RelationshipFilter()
        self.filterRel.exec_()
        
        # Create Str from List to Display on GUI
        text_RelDistFilter = str(self.filterRel.Condition_RelDist)
        self.rel_display.setText(text_RelDistFilter[1:-1])

        # Add FilterCondition To Search
        self.SearchFunction.Add_Relationship_Distance(self.filterRel.Condition_RelDist)
    
    def filterdisease(self):
        # Call Dialog Gui
        self.filterDise = DiseaseFilter()
        self.filterDise.exec_()

        # Create Str from List to Display on GUI
        text_DiseFilter = str(self.filterDise.Condition_Distance)
        self.dise_display.setText(text_DiseFilter[1:-1])
        
        # Add FilterCondition To Search
        self.SearchFunction.ChangeStatus_Disease(0)
        self.SearchFunction.Add_Disease(self.filterDise.Condition_Distance)

        # Enable Filter Source Website
        if len(self.filterDise.Condition_Distance) != 0:
            self.sourcewebBox.setEnabled(True)
        else:
            self.sourcewebBox.setEnabled(False)

    def SelectColumn(self, listHeader, listdata):
        list_index = []
        list_header = []
        list_selectedresult = []
        for i in listHeader:
            if i == 'All' :
                list_index.extend([0,1,2,3,4,5,6,7,8,9,10,11,12])
                break
            elif i == 'CHROMOSOME':
                list_index.append(2)
            elif i == 'DISEASE_ABBREVIATION':
                list_index.append(11)
            elif i == 'DISEASE_NAME':
                list_index.append(10)
            elif i == 'DISTANCE':
                list_index.append(6)
            elif i == 'GENE_ID':
                list_index.append(8)
            elif i == 'GENE_SYMBOL':
                list_index.append(7)
            elif i == 'MATCH_BY':
                list_index.append(12)
            elif i == 'OTHER_SYMBOL':
                list_index.append(9)
            elif i == 'POSITION':
                list_index.append(3)
            elif i == 'PROBESET_ID':
                list_index.append(1)    
            elif i == 'RELATIONSHIP':
                list_index.append(5)    
            elif i == 'RSID':
                list_index.append(0)    
            elif i == 'SOURCE_GENESHIP':
                list_index.append(4)
        list_index.sort()
        for i in list_index:
            if i == 0:
                list_header.append('RSID')
            elif i == 1:
                list_header.append('PROBESET_ID')
            elif i == 2:
                list_header.append('CHROMOSOME')
            elif i == 3:
                list_header.append('POSITION')
            elif i == 4:
                list_header.append('SOURCE_GENESHIP')
            elif i == 5:
                list_header.append('RELATIONSHIP')
            elif i == 6:
                list_header.append('DISTANCE')
            elif i == 7:
                list_header.append('GENE_SYMBOL')
            elif i == 8:
                list_header.append('GENE_ID')
            elif i == 9:
                list_header.append('OTHER_SYMBOL')
            elif i == 10:
                list_header.append('DISEASE_NAME')
            elif i == 11:
                list_header.append('DISEASE_ABBREVIATION')
            elif i == 12:
                list_header.append('MATCH_BY')
        for i in listdata:
            access_map = map(i.__getitem__, list_index)
            i[2] = str(i[2])
            i[8] = str(i[8])
            accessed_list = list(access_map)
            list_selectedresult.append(accessed_list)
        return list_selectedresult, list_header

    def SelectColumn_NoDISEASE(self, listHeader, listdata):
        list_index = []
        list_header = []
        list_selectedresult = []
        for i in listHeader:
            if i == 'All' :
                list_index.extend([0,1,2,3,4,5,6,7,8,9])
                break
            elif i == 'CHROMOSOME':
                list_index.append(2)
            elif i == 'DISEASE_ABBREVIATION':
                continue
            elif i == 'DISEASE_NAME':
                continue
            elif i == 'DISTANCE':
                list_index.append(6)
            elif i == 'GENE_ID':
                list_index.append(8)
            elif i == 'GENE_SYMBOL':
                list_index.append(7)
            elif i == 'MATCH_BY':
                continue
            elif i == 'OTHER_SYMBOL':
                list_index.append(9)
            elif i == 'POSITION':
                list_index.append(3)
            elif i == 'PROBESET_ID':
                list_index.append(1)    
            elif i == 'RELATIONSHIP':
                list_index.append(5)    
            elif i == 'RSID':
                list_index.append(0)    
            elif i == 'SOURCE_GENESHIP':
                list_index.append(4)
        list_index.sort()
        for i in list_index:
            if i == 0:
                list_header.append('RSID')
            elif i == 1:
                list_header.append('PROBESET_ID')
            elif i == 2:
                list_header.append('CHROMOSOME')
            elif i == 3:
                list_header.append('POSITION')
            elif i == 4:
                list_header.append('SOURCE_GENESHIP')
            elif i == 5:
                list_header.append('RELATIONSHIP')
            elif i == 6:
                list_header.append('DISTANCE')
            elif i == 7:
                list_header.append('GENE_SYMBOL')
            elif i == 8:
                list_header.append('GENE_ID')
            elif i == 9:
                list_header.append('OTHER_SYMBOL')
        for i in listdata:
            access_map = map(i.__getitem__, list_index)
            i[2] = str(i[2])
            i[8] = str(i[8])
            accessed_list = list(access_map)
            list_selectedresult.append(accessed_list)
        return list_selectedresult, list_header
    
    def barplot(self, xlist, ylist):
        y_pos = np.arange(len(ylist))

        # Create bars
        plt.bar(y_pos, xlist)

        # Create names on the x-axis
        plt.xticks(y_pos, ylist)

        # Show graphic
        plt.show()

    def DfToAxis(self, dataframe, header):
        df = dataframe[header].value_counts().reset_index()
        df.columns = [header, 'count']
        List_index = df[header].tolist()
        List_count = df['count'].tolist()

        # mix Pathway
        if header == 'MATCH_BY':
            index_pathway = []
            countPathway = 0 
            for txtIndex in List_index:
                if txtIndex[:7] == "Pathway":
                    index_pathway.append(List_index.index(txtIndex))
            for index in sorted(index_pathway, reverse=True):
                del List_index[index]
                countPathway += List_count[index]
                del List_count[index]
            List_index.append("Pathway")
            List_count.append(countPathway)

        return List_count, List_index
    
    def DfToAxisFocusSNP(self, dataframe, header):
        df = dataframe
        col_SNP = df['RSID'].tolist()
        for SNP in col_SNP:
            selectsnp = df.loc[df['RSID'] == SNP]
            list_index = selectsnp.index.tolist()
            df = df.drop(list_index[1:])
        newdf = df[header].value_counts().reset_index()
        newdf.columns = [header, 'count']
        List_index = newdf[header].tolist()
        List_count = newdf['count'].tolist()
        return List_count, List_index
    
    def ShowSNP_Rank(self, data, header, text):
        text = text.split(' ')[-1]
        if header == "MATCH_BY":
            get_SNP_Fil = data.MATCH_BY.str.contains(text,case=False)
        else:
            get_SNP_Fil = data[header] == text
        self.ShowSNP_Chr = ShowSNP(data[get_SNP_Fil])
        self.ShowSNP_Chr.exec_()

    def exportlistdata(self, list):
        self.df = pd.DataFrame(list[1:], columns=list[0])
        print(self.df)
        default_dir ="/home/qt_user/name"
        default_filename = os.path.join(default_dir)
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", default_filename, "Comma-Separated Value (*.csv)"
        )
        if filename:
            print(filename)
            self.df.to_csv(filename,index=False)

    def sortChromosome(self, x, y):
        listx = []
        listnum = []
        for i in y :
            if i == 'X':
                listx.append('X')
            else:
                listnum.append(int(i))

        if len(listx) != 0:
            index_x = y.index('X')
            getvalue_x = x[index_x]
            x.pop(index_x)
            Z = [i for _,i in sorted(zip(listnum,x))]
            Z.append(getvalue_x)
            listnum.sort()
            list_string = map(str, listnum) 
            newY = list(list_string)
            newY.append(listx[0])
            return Z, newY
        else:
            Z = [i for _,i in sorted(zip(listnum,x))]
            listnum.sort()
            list_string = map(str, listnum) 
            newY = list(list_string)
            return Z, newY

    def CheckStateGenechip(self, genechip):
        if genechip == 'All':
            return 0
        elif genechip == 'Nsp':
            return 1
        elif genechip == 'Sty':
            return 2 

    def CheckStateSourceWeb(self, SourceWeb):
        if SourceWeb == 'All':
            return 0
        elif SourceWeb == 'Huge':
            return 1
        elif SourceWeb == 'Kegg':
            return 2
        elif SourceWeb == 'Pathway':
            return 3
        elif SourceWeb == 'Huge, Kegg':
            return 4
        elif SourceWeb == 'Huge, Pathway':
            return 5
        elif SourceWeb == 'Kegg, Pathway':
            return 6
        elif SourceWeb == 'Huge, Kegg, Pathway':
            return 7

    def ListSTRtoListINT(self, list):
        list_int = []
        for i in list:
            if ( str(i) == ''):
                continue
            list_int.append(int(i))
        return list_int

    def SliceListDimension2(self, list, indexstart, indexstop):
        nplist = np.array(list)
        slice_nplist = nplist[:, indexstart: indexstop]
        slice_list = slice_nplist.tolist()
        NotExist = []
        for snp in slice_list:
            if snp not in NotExist:
                NotExist.append(snp)
        NotExist.sort(key=lambda x: x[0])
        return NotExist
    
    def sortbySNP(self,list):
        list.sort(key=lambda x: x[0])
        return list

    def searchsnp(self):
        # ---- Display Input SNP ----
        inputsnp_str = self.inputSNP_display.toPlainText()
        listinput = inputsnp_str.split(", ")
        if listinput[0][0] == "'":
            for i in range(len(listinput)):
                if listinput[i][:3] == "'\n":
                    listinput[i] = listinput[i][3:-3]
                else:    
                    listinput[i] = listinput[i][1:-1]
        if listinput[0] == '': # alert not input snp
            QMessageBox.about(self, 'ERROR', "Please Add input SNP")
            return
        else:
            self.SearchFunction.ImportData(listinput)
        print(" Input Snp = ", listinput)

        # ---- Display Chromosome ----
        print("Chromosome :", self.Chromo_display.toPlainText())
        
        # ---- Display Position ----
        print("Position :", self.Posi_display.toPlainText())
        
        # ---- Display GeneChip ----
        print("GeneChip :", self.GeneChipBox.currentText())
        genechip_state = self.CheckStateGenechip(self.GeneChipBox.currentText())
        self.SearchFunction.Add_Geneship(genechip_state)

        # ---- Display GeneID ----
        inputgeneid_str = self.GeneID_display.toPlainText()
        listinputgeneid = inputgeneid_str.split(", ")
        listinputgeneid_int = self.ListSTRtoListINT(listinputgeneid)
        print("Input geneid :", listinputgeneid_int)
        self.SearchFunction.Add_GeneID(listinputgeneid_int)

        # ---- Display GeneSymbol ----
        inputgenesym_str = self.genesym_display.toPlainText()
        listinputgenesym = inputgenesym_str.split(", ")
        print("Input GeneSymbol :", listinputgenesym)
        self.SearchFunction.Add_GeneSymbol(listinputgenesym)

        # ---- Display Relationship&Distance ----
        print("Relationship :", self.rel_display.toPlainText())

        # ---- Display Disease ----
        print("Disease :", self.dise_display.toPlainText())

        # ---- Display SourceWebsite ----
        print("SourceWeb :", self.sourcewebBox.currentText())
        SourceWeb_state = self.CheckStateSourceWeb(self.sourcewebBox.currentText())
        self.SearchFunction.Add_source_website(SourceWeb_state)

        # ---- open GUI select some column ----
        self.Select_Search = SelectSearch()
        self.Select_Search.exec_()

        self.InCon_FoundDisease, self.InCon_NotFoundDisease, self.OutCon_FoundDisease, self.OutCon_NotFoundDisease = self.SearchFunction.SearchData()
        print('InCon Disease len', len(self.InCon_FoundDisease), '  :  ', self.InCon_FoundDisease)
        print('InCon NotDisease len', len(self.InCon_NotFoundDisease), '  :  ', self.InCon_NotFoundDisease)
        print('OutCon Disease len', len(self.OutCon_FoundDisease), '  :  ', self.OutCon_FoundDisease)
        print('OutCon NotDisease len', len(self.OutCon_NotFoundDisease), '  :  ', self.OutCon_NotFoundDisease)

        # ---- check select Disease ----
        if len(self.dise_display.toPlainText()) == 0 : # Not Choose Disease Table1 Show InConDisease+InConNotDisease
            if len(self.InCon_FoundDisease)!= 0:
                slice_InCon_FoundDisease = self.SliceListDimension2(self.InCon_FoundDisease,0,-3)
                self.InCon_NotFoundDisease.extend(slice_InCon_FoundDisease)
            self.showresult_FD, self.header_FD = self.SelectColumn_NoDISEASE(self.Select_Search.selected, self.InCon_NotFoundDisease)
            if len(self.OutCon_FoundDisease) != 0 :
                slice_OutCon_FoundDisease = self.SliceListDimension2(self.OutCon_FoundDisease,0,-3)
                self.OutCon_NotFoundDisease.extend(slice_OutCon_FoundDisease)
            self.showresult_NF, self.header_NF = self.SelectColumn_NoDISEASE(self.Select_Search.selected, self.OutCon_NotFoundDisease)
        else:   # Choose Disease Table1 Show InConDisease
            self.showresult_FD, self.header_FD = self.SelectColumn(self.Select_Search.selected, self.InCon_FoundDisease)
            self.OutCon_NotFoundDisease.extend(self.InCon_NotFoundDisease)
            if len(self.OutCon_FoundDisease) != 0 :
                slice_OutCon_FoundDisease = self.SliceListDimension2(self.OutCon_FoundDisease,0,-3)
                self.OutCon_NotFoundDisease.extend(slice_OutCon_FoundDisease)
            self.showresult_NF, self.header_NF = self.SelectColumn_NoDISEASE(self.Select_Search.selected, self.OutCon_NotFoundDisease)

        self.showresult_FD = self.sortbySNP(self.showresult_FD)
        self.showresult_NF = self.sortbySNP(self.showresult_NF)

        # ---------------- Table -----------------
        self.showresult_FD.insert(0,self.header_FD) # Add Header
        self.showresult_NF.insert(0,self.header_NF) 
        self.model = TableModel(self.showresult_FD)
        self.tableView_1.setModel(self.model)
        self.model_NF = TableModel(self.showresult_NF)
        self.tableView_2.setModel(self.model_NF)
        self.ex_table_f.setEnabled(True)
        self.ex_table_f.clicked.connect(lambda: self.exportlistdata(self.showresult_FD))
        self.ex_table_nf.setEnabled(True)
        self.ex_table_nf.clicked.connect(lambda: self.exportlistdata(self.showresult_NF))
        # ---------------- Table -----------------

        # ---------------- Chart -----------------
        df_Result_FD = pd.DataFrame(self.showresult_FD[1:], columns= self.header_FD)

        if 'CHROMOSOME' in self.header_FD:
            x, y = self.DfToAxisFocusSNP(df_Result_FD, 'CHROMOSOME')
            newX, newY = self.sortChromosome(x, y)
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(newY, newX)
            toolbar = NavigationToolbar(sc, self)
            # remove Old Chart
            for i in reversed(range(self.Chr_BarBox.count())): 
                self.Chr_BarBox.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.Chr_layout.count())): 
                self.Chr_layout.itemAt(i).widget().setParent(None)
            # add New Chart
            self.Chr_BarBox.addWidget(toolbar)
            self.Chr_BarBox.addWidget(sc)
            self.Chr_groupbox = QGroupBox()
            self.Chr_form = QFormLayout()
            for index in range(len(x)):
                chr_text = 'Chromosome ' + y[index] + ' : ' + str(x[index]) + '\n'
                self.Chr_label = QLabel(chr_text)
                self.btn_detail_chr = QPushButton('Chromosome {}'.format(y[index]), self)
                text = self.btn_detail_chr.text()
                self.btn_detail_chr.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_FD, 'CHROMOSOME', text),
                    ))
                self.grid_chr = QGridLayout()
                self.grid_chr.addWidget(self.Chr_label, 0, 0)
                self.grid_chr.addWidget(self.btn_detail_chr, 0, 1)
                self.Chr_form.addRow(self.grid_chr)
            self.Chr_groupbox.setLayout(self.Chr_form)
            scroll = QScrollArea()
            scroll.setWidget(self.Chr_groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.Chr_layout.addWidget(scroll)

        if 'RELATIONSHIP' in self.header_FD:
            x, y = self.DfToAxis(df_Result_FD, 'RELATIONSHIP')
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.barh(y, x)
            toolbar = NavigationToolbar(sc, self)
            # remove Old Chart
            for i in reversed(range(self.Rel_BarBox.count())): 
                self.Rel_BarBox.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.Rel_layout.count())): 
                self.Rel_layout.itemAt(i).widget().setParent(None)
            # add New Chart
            self.Rel_BarBox.addWidget(toolbar)
            self.Rel_BarBox.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text =  y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_FD, 'RELATIONSHIP', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.Rel_layout.addWidget(scroll)
    
        if 'SOURCE_GENESHIP' in self.header_FD:
            x, y = self.DfToAxisFocusSNP(df_Result_FD, 'SOURCE_GENESHIP')
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(y, x)
            toolbar = NavigationToolbar(sc, self)
            for i in reversed(range(self.GC_BarBox.count())): 
                self.GC_BarBox.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.GC_layout.count())): 
                self.GC_layout.itemAt(i).widget().setParent(None)
            self.GC_BarBox.addWidget(toolbar)
            self.GC_BarBox.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text =  y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_FD, 'SOURCE_GENESHIP', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.GC_layout.addWidget(scroll)
        
        if 'MATCH_BY' in self.header_FD:
            x, y = self.DfToAxis(df_Result_FD, 'MATCH_BY')
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(y, x)
            toolbar = NavigationToolbar(sc, self)
            for i in reversed(range(self.MB_BarBox.count())): 
                self.MB_BarBox.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.MB_layout.count())): 
                self.MB_layout.itemAt(i).widget().setParent(None)
            self.MB_BarBox.addWidget(toolbar)
            self.MB_BarBox.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text = y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_FD, 'MATCH_BY', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.MB_layout.addWidget(scroll)
        
        df_Result_NF = pd.DataFrame(self.showresult_NF[1:], columns= self.header_NF)

        if 'CHROMOSOME' in self.header_NF:
            x, y = self.DfToAxisFocusSNP(df_Result_NF, 'CHROMOSOME')
            newX, newY = self.sortChromosome(x, y)
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(newY, newX)
            toolbar = NavigationToolbar(sc, self)
            for i in reversed(range(self.Chr_BarBox_2.count())): 
                self.Chr_BarBox_2.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.Chr_layout2.count())): 
                self.Chr_layout2.itemAt(i).widget().setParent(None)
            self.Chr_BarBox_2.addWidget(toolbar)
            self.Chr_BarBox_2.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text = 'Chromosome ' + y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP Chromosome {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_NF, 'CHROMOSOME', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.Chr_layout2.addWidget(scroll)

        if 'RELATIONSHIP' in self.header_NF:
            x, y = self.DfToAxis(df_Result_NF, 'RELATIONSHIP')
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.barh(y, x)
            toolbar = NavigationToolbar(sc, self)
            for i in reversed(range(self.Rel_BarBox_2.count())): 
                self.Rel_BarBox_2.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.Rel_layout2.count())): 
                self.Rel_layout2.itemAt(i).widget().setParent(None)
            self.Rel_BarBox_2.addWidget(toolbar)
            self.Rel_BarBox_2.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text =  y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_NF, 'RELATIONSHIP', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.Rel_layout2.addWidget(scroll)
    
        if 'SOURCE_GENESHIP' in self.header_NF:
            x, y = self.DfToAxisFocusSNP(df_Result_NF, 'SOURCE_GENESHIP')
            sc = MplCanvas(self, width=5, height=4, dpi=100)
            sc.axes.bar(y, x)
            toolbar = NavigationToolbar(sc, self)
            for i in reversed(range(self.GC_BarBox_2.count())): 
                self.GC_BarBox_2.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.GC_layout2.count())): 
                self.GC_layout2.itemAt(i).widget().setParent(None)
            self.GC_BarBox_2.addWidget(toolbar)
            self.GC_BarBox_2.addWidget(sc)
            self.groupbox = QGroupBox()
            self.form = QFormLayout()
            for index in range(len(x)):
                text = y[index] + ' : ' + str(x[index]) + '\n'
                self.label = QLabel(text)
                self.btn_detail = QPushButton('Show SNP {}'.format(y[index]), self)
                text = self.btn_detail.text()
                self.btn_detail.clicked.connect(
                    lambda ch, text=text : (
                    print("\nclicked--> {}".format(text)),
                    self.ShowSNP_Rank(df_Result_NF, 'SOURCE_GENESHIP', text),
                    ))
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 0, 0)
                self.grid.addWidget(self.btn_detail, 0, 1)
                self.form.addRow(self.grid)
            self.groupbox.setLayout(self.form)
            scroll = QScrollArea()
            scroll.setWidget(self.groupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(200)
            self.GC_layout2.addWidget(scroll)
        # ---------------- Chart -----------------

app=QApplication(sys.argv)
mainwindow=MainWindow()
mainwindow.show()
sys.exit(app.exec_())
