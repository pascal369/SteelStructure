# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import math
import string
from tkinter.tix import ComboBox
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import Draft
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
#from prt_data.CSnap_data import paramCSnap

BShp=['40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
      '75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7','100x100x10','100x100x13']
LShp=['40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
      '75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7','100x100x10','100x100x13']

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
        Dialog.resize(250, 400)
        Dialog.move(1000, 0)
        
        #玄材
        self.label_BShp = QtGui.QLabel('chordMember',Dialog)
        self.label_BShp.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_BShp = QtGui.QComboBox(Dialog)
        self.comboBox_BShp.setGeometry(QtCore.QRect(110, 10, 100, 22))

        #ラチス材
        self.label_LShp = QtGui.QLabel('latticeMember',Dialog)
        self.label_LShp.setGeometry(QtCore.QRect(10, 42, 100, 12))
        self.comboBox_LShp = QtGui.QComboBox(Dialog)
        self.comboBox_LShp.setGeometry(QtCore.QRect(110, 35, 100, 22))

        #梁成
        self.label_H = QtGui.QLabel('beamHight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.spinBoxH=QtGui.QSpinBox(Dialog)
        self.spinBoxH.setGeometry(110, 60, 100, 30)
        self.spinBoxH.setMinimum(500)  # 最小値を0.0に設定
        self.spinBoxH.setMaximum(5000.0)  # 最大値を100.0に設定
        self.spinBoxH.setSingleStep(50)
        self.spinBoxH.setAlignment(QtCore.Qt.AlignCenter)

        #梁長
        self.label_L = QtGui.QLabel('span',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(110, 85, 100, 30)
        self.spinBoxL.setMinimum(1000)  # 最小値
        self.spinBoxL.setMaximum(50000)  # 最大値
        self.spinBoxL.setSingleStep(50) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)

        #端部ガセットプレート幅
        self.label_GPL = QtGui.QLabel('GPL_width',Dialog)
        self.label_GPL.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_GPL = QtGui.QLineEdit('150',Dialog)
        self.le_GPL.setGeometry(QtCore.QRect(110, 115, 50, 20))
        self.le_GPL.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 135, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 135, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 160, 180, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 190, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_BShp.addItems(BShp)
        self.comboBox_BShp.setEditable(True)

        self.comboBox_LShp.addItems(LShp)
        self.comboBox_LShp.setEditable(True)
        
        self.spinBoxH.valueChanged[int].connect(self.spinMove) 
        self.spinBoxL.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.spinMove)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)

        fname='TrussBeam.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Beam_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Truss Beam", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None)) 

    def spinMove(self):
         #
         try:
             H0=self.spinBoxH.value()
             L0=self.spinBoxL.value()
             #print(H0,L0)
             Bshp=self.comboBox_BShp.currentText()#玄材
             Lshp=self.comboBox_LShp.currentText()#ラチス材
             Gb0=float(self.le_GPL.text())#端部ガセット幅
             
             spreadsheet.set('shp',Bshp)#玄材
             #print(Lshp,Gb0)
             spreadsheet.set('Gb0',str(Gb0))#端部ガセット幅
             #print(Bshp)
             genzai.size = Bshp
             #print(Bshp)
             #玄材
             for i in range(20,35):
                 Bshp3=spreadsheet.getContents('A'+str(i))
                 #print(Bshp,Bshp3)
                 if Bshp==Bshp3[1:]:
                     break
             row_B=i  
             gL0=spreadsheet.getContents('D'+str(row_B))#ゲージ 
             #print(gL0)
             
             #ラチス材幅、板厚
             for i in range(20,35):
                 Lshp3=spreadsheet.getContents('A'+str(i))
                 #print(Lshp,Lshp3)
                 if Lshp==Lshp3[1:]:
                     break
             row_L=i 
            
             Lt0=spreadsheet.getContents('B'+str(row_L))     
             Lb0=spreadsheet.getContents('C'+str(row_L)) 

             gL1=spreadsheet.getContents('D'+str(row_L))
             
             H00=float(H0)-2.0*float(gL0)
             rp0=H00
    
             sita=math.atan(H00*2/rp0)*57.3
 
             lz=float(gL0)*math.sin(sita/57.3)
             l0=lz/math.sin(sita/57.3)
             lx=l0*math.cos(sita/57.3)
             
             a0=spreadsheet.getContents('a0')
             print(a0)
             
             AngleSteel.size=str(Lshp)
             
            
             rp0=spreadsheet.getContents('rp0')
             m0=float(L0)/float(rp0)
             m0=int(m0)
             rp0=(float(L0)-Gb0)/m0
             sita=math.atan(H00*2/rp0)*57.3
             spreadsheet.set('Lshp',Lshp)
             spreadsheet.set('gL0',gL0)
             spreadsheet.set('Lb0',Lb0)
             spreadsheet.set('Lt0',Lt0)
             spreadsheet.set('Gb0',str(Gb0))
             spreadsheet.set('rp0',str(rp0))
             spreadsheet.set('sita',str(sita))
             spreadsheet.set('gL1',gL1)
             spreadsheet.set('lx',str(lx))
             spreadsheet.set('lz',str(lz))
             spreadsheet.set('m0',str(m0-1))
             spreadsheet.set('a0',str(a0))
             spreadsheet.set('H0',str(H0))
             spreadsheet.set('L0',str(L0))
             App.ActiveDocument.recompute() 
         except:   
             pass  
        
    def read_data(self):
         global AngleSteel
         global genzai
         global spreadsheet
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label=="AngleSteel20":
                         AngleSteel=obj
                     elif obj.Label=='genzai01':
                         genzai=obj

                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_BShp.setCurrentText(spreadsheet.getContents('shp')[1:])
                         self.comboBox_LShp.setCurrentText(spreadsheet.getContents('Lshp')[1:])
                         self.le_GPL.setText(spreadsheet.getContents('Gb0')) 
                         self.spinBoxH.setValue(int(spreadsheet.getContents('H0')))
                         self.spinBoxL.setValue(int(spreadsheet.getContents('L0')))

    def update(self):
         Bshp=self.comboBox_BShp.currentText()#玄材
         Lshp=self.comboBox_LShp.currentText()#ラチス材
         Bhight=self.spinBoxH.value()#梁成
         Blength=self.spinBoxL.value()#梁長
         Gb0=self.le_GPL.text()#ガセットプレート幅
         #print(angle,Bshp)
         AngleSteel.size = str(Bshp)
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
         doc=App.activeDocument()
         fname='trussBeam.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Beam_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            #doc=App.newDocument()
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
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            