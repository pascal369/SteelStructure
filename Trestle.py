# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

type=['01','02','03','04','05']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 400)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 195, 200, 200))
        self.label_6.setText("")

        #type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 80, 22))
        #床面幅W
        self.label_W = QtGui.QLabel('W[mm',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 38, 60, 12))
        self.lineEdit_W = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_W.setGeometry(QtCore.QRect(80, 35, 80, 22))
        self.lineEdit_W.setAlignment(QtCore.Qt.AlignCenter)
        #床面長L
        self.label_L = QtGui.QLabel('L[mm',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 68, 60, 12))
        self.lineEdit_L = QtGui.QLineEdit('2000',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(80, 60, 80, 22))
        self.lineEdit_L.setAlignment(QtCore.Qt.AlignCenter)
        #床面高H
        self.label_H = QtGui.QLabel('H[mm',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 93, 60, 12))
        self.lineEdit_H = QtGui.QLineEdit('2200',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(80, 90, 80, 22))
        self.lineEdit_H.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 115, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 140, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 165, 80, 22))

        self.comboBox_type.addItems(type)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.ontype)
        self.comboBox_type.setCurrentIndex(0)

        self.comboBox_type.setEditable(True)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onImport)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "trestle", None))

    def ontype(self):
        global mytype
        mytype=self.comboBox_type.currentText()
        #print(mytype)
        fname='trestle'+mytype+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'StlStu_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        return
    def onImport(self):
        global spreadsheet
        global stair
        global SteelStair
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     print(obj.Label)
                     
                     
                     if obj.Label[:10]=='SteelStair':
                         SteelStair=obj     

                     elif obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj  
                     elif obj.Label[:5]=='stair':
                         stair=obj  
             self.lineEdit_W.setText(spreadsheet.getContents('W0'))    
             self.lineEdit_L.setText(spreadsheet.getContents('L0'))          
             self.lineEdit_H.setText(spreadsheet.getContents('H0'))  
             self.comboBox_type.setCurrentText(spreadsheet.getContents('key')[1:])
    def update(self):
         myW=self.lineEdit_W.text()
         myL=self.lineEdit_L.text()
         myH=self.lineEdit_H.text()
         spreadsheet.set('W0',myW)
         spreadsheet.set('L0',myL)
         spreadsheet.set('H0',myH)
         #print(myW)
         if mytype=='01':
             stair.H=float(myH)
             stair.L=float(myH)
         elif mytype=='02':
             SteelStair.H=float(myH)
             SteelStair.L=float(myH)   
         elif mytype=='03':
             SteelStair.H=float(myH)
             SteelStair.L=float(myH) 
             SteelStair.w=float(myL) 
             stair.H=float(myH)
             stair.L=float(myH)  
             stair.L1=float(myW)    
             stair.w0=float(myL)  

         App.ActiveDocument.recompute()
         
    def create(self): 
         mytype=self.comboBox_type.currentText()
         fname='trestle'+mytype+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'StlStu_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            