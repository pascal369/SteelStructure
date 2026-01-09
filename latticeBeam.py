# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import string
from tkinter.tix import ComboBox
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
#from prt_data.CSnap_data import paramCSnap

BShp=['40x40x3','40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
      '75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7','100x100x10','100x100x13']
LShp=['6x38','9x38','6x44','9x44','4.5x50','6x50','9x50','6x65','9x65','6x75',
      '9x75','6x90','9x90',]

# 画面を並べて表示する
class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 420)
        Dialog.move(1000, 0)
        
        #玄材
        self.label_BShp = QtGui.QLabel('chordMember',Dialog)
        self.label_BShp.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.label_BShp.setStyleSheet("color: black;")
        self.comboBox_BShp = QtGui.QComboBox(Dialog)
        self.comboBox_BShp.setGeometry(QtCore.QRect(110, 8, 100, 22))

        #ラチス材
        self.label_LShp = QtGui.QLabel('latticeMember',Dialog)
        self.label_LShp.setGeometry(QtCore.QRect(10, 42, 100, 12))
        self.label_LShp.setStyleSheet("color: black;")
        self.comboBox_LShp = QtGui.QComboBox(Dialog)
        self.comboBox_LShp.setGeometry(QtCore.QRect(110, 35, 100, 22))

        #梁成
        self.label_H = QtGui.QLabel('beamHight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 67, 100, 22))
        self.label_H.setStyleSheet("color: black;")
        self.spinBoxH=QtGui.QSpinBox(Dialog)
        self.spinBoxH.setGeometry(110, 62, 100, 30)
        self.spinBoxH.setMinimum(500)  # 最小値を0.0に設定
        self.spinBoxH.setMaximum(1000.0)  # 最大値を100.0に設定
        self.spinBoxH.setSingleStep(10)
        self.spinBoxH.setAlignment(QtCore.Qt.AlignCenter)

        #梁長
        self.label_L = QtGui.QLabel('span',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 98, 100, 22))
        self.label_L.setStyleSheet("color: black;")
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(110, 95, 100, 30)
        self.spinBoxL.setMinimum(1000)  # 最小値
        self.spinBoxL.setMaximum(20000)  # 最大値
        self.spinBoxL.setSingleStep(50) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)

        #ガセットプレート幅
        self.label_GPL = QtGui.QLabel('GPL width',Dialog)
        self.label_GPL.setGeometry(QtCore.QRect(10, 133, 100, 22))
        self.label_GPL.setStyleSheet("color: black;")
        self.le_GPL = QtGui.QLineEdit('150',Dialog)
        self.le_GPL.setGeometry(QtCore.QRect(110, 130, 100, 20))
        self.le_GPL.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(45, 155, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 155, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(45, 180, 185, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 205, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_BShp.addItems(BShp)
        self.comboBox_BShp.setEditable(True)

        self.comboBox_LShp.addItems(LShp)
        self.comboBox_LShp.setEditable(True)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)

        self.spinBoxH.valueChanged[int].connect(self.spinMoveH) 
        self.spinBoxL.valueChanged[int].connect(self.spinMoveL) 

        fname='LatticeBeam.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Beam_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Lattice Beam", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def spinMoveH(self):
         dL=self.spinBoxH.value()
         spreadsheet.set('H0',str(dL))
         App.ActiveDocument.recompute() 

    def spinMoveL(self):
         dL=self.spinBoxL.value()
         spreadsheet.set('L0',str(dL))
         App.ActiveDocument.recompute() 

    def read_data(self):
         global angle
         global spreadsheet
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label[:10]=='AngleSteel':
                         angle=obj
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_BShp.setCurrentText(spreadsheet.getContents('shp')[1:])
                         self.comboBox_LShp.setCurrentText(spreadsheet.getContents('Lshp')[1:])
                         #self.le_H.setText(spreadsheet.getContents('B2')) 
                         #self.le_L.setText(spreadsheet.getContents('B3')) 
                         self.le_GPL.setText(spreadsheet.getContents('B9')) 
                         self.spinBoxH.setValue(int(spreadsheet.getContents('H0')))
                         self.spinBoxL.setValue(int(spreadsheet.getContents('L0')))

    def update(self):
         Bshp=self.comboBox_BShp.currentText()#玄材
         Lshp=self.comboBox_LShp.currentText()#ラチス材
         Bhight=self.spinBoxH.value()#梁成
         Blength=self.spinBoxL.value()#梁長
         Gb0=self.le_GPL.text()#ガセットプレート幅
         #print(angle,Bshp)
         angle.size = str(Bshp)
         #玄材ゲージライン 
         for i in range(17,32):
             Bshp3=spreadsheet.getContents('A'+str(i))
             if Bshp==Bshp3[1:]:
                 break
         row_B=i  
         GL0=spreadsheet.getContents('D'+str(row_B)) 
         
         #ラチス個数
         for n in range(1,100):
             rp03=(float(Blength)-2*float(GL0))/n
             if float(rp03)<=float(Bhight):
                 break
         rn0=n  
         #ラチス材幅、板厚
         for i in range(34,46):
             
             Lshp3=spreadsheet.getContents('A'+str(i))
             #print(Lshp,Lshp3)
             if Lshp==Lshp3[1:]:
                 break
         row_L=i  
         Lt0=spreadsheet.getContents('B'+str(row_L))     
         Lb0=spreadsheet.getContents('C'+str(row_L))      
         spreadsheet.set('H0',str(Bhight))
         #spreadsheet.set('L0',Blength)
         spreadsheet.set('shp',Bshp)
         spreadsheet.set('GL0',GL0)
         spreadsheet.set('Lshp',Lshp)
         spreadsheet.set('Lb0',Lb0)
         spreadsheet.set('Gt0',Lt0)
         spreadsheet.set('Gb0',Gb0)
         spreadsheet.set('rn0',str(rn0))
         #App.ActiveDocument.recompute() 

         c00 = Gui.Selection.getSelection()
         if c00:
             obj = c00[0]
         try:
             obj.Standard='L'+Bshp+'  L='+str(Blength)+'  H='+str(Bhight)
             print(Blength)
         except:
             print('error')
             pass
         obj.mass=obj.Shape.Volume*obj.g0*1000/10**9 
         App.ActiveDocument.recompute()
                
    def create(self): 
         fname='latticeBeam.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Beam_data',fname) 
         try:
            doc=App.activeDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
            
         objs=doc.Objects
         if objs:
             last_obj=objs[-1] 
         Gui.activateWorkbench("DraftWorkbench")
         Gui.Selection.addSelection(last_obj)
         Gui.runCommand('Draft_Move',0)  

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        