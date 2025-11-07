# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import math
import string
#from tkinter.tix import ComboBox
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


dia_data=['10','12','16','20','22','24','30',]
type_data=['A','B','C']

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

        #type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 8, 100, 22))

        
        #ロッド径 dia
        self.label_dia = QtGui.QLabel('Dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(110, 35, 100, 22))

        #ブレス長 L
        self.label_L = QtGui.QLabel('Length',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.label_L.setStyleSheet("color: black;")
        self.le_L = QtGui.QLineEdit('1000',Dialog)
        self.le_L.setGeometry(QtCore.QRect(110, 63, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #ブレス幅 W
        self.label_W = QtGui.QLabel('Width',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.label_W.setStyleSheet("color: black;")
        self.le_W = QtGui.QLineEdit('1000',Dialog)
        self.le_W.setGeometry(QtCore.QRect(110, 85, 50, 20))
        self.le_W.setAlignment(QtCore.Qt.AlignCenter)
        #ターンバックル位置Tp
        self.label_Lx = QtGui.QLabel('Turnbackle',Dialog)
        self.label_Lx.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.label_Lx.setStyleSheet("color: black;")
        self.le_Lx = QtGui.QLineEdit('500',Dialog)
        self.le_Lx.setGeometry(QtCore.QRect(110, 110, 50, 20))
        self.le_Lx.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 135, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 135, 60, 22))
        #importData
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 160, 180, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 190, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_dia.addItems(dia_data)
        self.comboBox_type.addItems(type_data)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "turnBackle", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def onType(self):
        #global fname
        global key
        #print('aaaaaaaaaaa')
        key=self.comboBox_type.currentText()
        self.le_W.hide()
        if key=='C':
            self.le_W.show()
        fname='turnBackle'+self.comboBox_type.currentText()+'.png'
        #print(key)
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "turnBackle_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
        App.ActiveDocument.recompute()

    def read_data(self):
         #global turnBackleC
         global spreadsheet
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #if obj.Label=='turnBackleC':
                     #    turnBackleC=obj
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         self.comboBox_type.setEditable(True) 
                         self.comboBox_type.setCurrentText(spreadsheet.getContents('A1')[1:])
                         #print(spreadsheet.getContents('A1'))
                         key=self.comboBox_type.currentText()
                         #print(key)
                         
                         self.comboBox_dia.setCurrentText(spreadsheet.getContents('dia'))
                         self.le_L.setText(spreadsheet.getContents('L0')) 
                         self.le_Lx.setText(spreadsheet.getContents('lx')) 
                         #print(key)
                         if key=='C':
                             self.le_W.show()
                             #print('bbbbbbbbbbbbbbbbbbbbbbbbbbb')
                             self.le_W.setText(spreadsheet.getContents('w0')) 
                             self.le_L.setText(spreadsheet.getContents('l0')) 

                 fname='turnBackle'+self.comboBox_type.currentText()+'.png'
                 base=os.path.dirname(os.path.abspath(__file__))
                 joined_path = os.path.join(base, "turnBackle_data",fname)
                 self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
                 App.ActiveDocument.recompute()
                     
    def update(self):
           #print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
           key=self.comboBox_type.currentText()
           dia=self.comboBox_dia.currentText()#dia
           L=self.le_L.text()#Lengrh
           lx=self.le_Lx.text()
           spreadsheet.set('dia',dia)#dia
           spreadsheet.set('lx',lx)
           if key=='C': 
               W=self.le_W.text()#Width
               spreadsheet.set('l0',L)
               spreadsheet.set('w0',W)
           else:
               spreadsheet.set('L0',L)
           #App.ActiveDocument.recompute()     
           #return       

           for j in range(20,27):
               dia3=spreadsheet.getContents('A'+str(j))
               #print(dia,dia3)
               if dia==dia3:
                   break
               l=spreadsheet.getContents('B'+str(j+1))
               a=spreadsheet.getContents('C'+str(j+1))
               b=spreadsheet.getContents('D'+str(j+1))
               c=spreadsheet.getContents('E'+str(j+1))
               e=spreadsheet.getContents('F'+str(j+1))
               f=spreadsheet.getContents('G'+str(j+1))
               g=spreadsheet.getContents('H'+str(j+1))
               r=spreadsheet.getContents('I'+str(j+1))
               

               spreadsheet.set('B7',l)
               spreadsheet.set('D7',a)
               spreadsheet.set('E7',b)
               spreadsheet.set('F7',c)
               spreadsheet.set('G7',e)
               spreadsheet.set('H7',f)
               spreadsheet.set('I7',g)
               spreadsheet.set('L7',r)

           
    
           for j in range(29,37):
               dia3=spreadsheet.getContents('A'+str(j))
               if dia==dia3:
                   break
               #print(dia,dia3,j)
               l=spreadsheet.getContents('B'+str(j+1))
               a=spreadsheet.getContents('C'+str(j+1))
               b=spreadsheet.getContents('D'+str(j+1))
               c=spreadsheet.getContents('E'+str(j+1))
               r=spreadsheet.getContents('F'+str(j+1))
               e=spreadsheet.getContents('G'+str(j+1))
               f=spreadsheet.getContents('H'+str(j+1))
               g=spreadsheet.getContents('I'+str(j+1))
               h=spreadsheet.getContents('J'+str(j+1))
               i=spreadsheet.getContents('K'+str(j+1))
 
               spreadsheet.set('B5',l)
               spreadsheet.set('C5','')
               spreadsheet.set('D5',a)
               spreadsheet.set('E5',b)
               spreadsheet.set('F5',c)
               spreadsheet.set('G5',e)
               spreadsheet.set('H5',f)
               spreadsheet.set('I5',g)
               spreadsheet.set('J5',h)
               spreadsheet.set('K5',i)
               spreadsheet.set('L5',r)
    
           for j in range(11,18):
               dia3=spreadsheet.getContents('A'+str(j))
               #print(dia,dia3)
               if dia==dia3:
                   break
               l=spreadsheet.getContents('B'+str(j+1))
               l1=spreadsheet.getContents('C'+str(j+1))
               a=spreadsheet.getContents('D'+str(j+1))
               b=spreadsheet.getContents('E'+str(j+1))
               c=spreadsheet.getContents('F'+str(j+1))
               t0=spreadsheet.getContents('G'+str(j+1))
 
               spreadsheet.set('B6',l)
               spreadsheet.set('C6',l1)
               spreadsheet.set('D6',a)
               spreadsheet.set('E6',b)
               spreadsheet.set('F6',c)
               #key=self.comboBox_type.currentText()
           App.ActiveDocument.recompute()  
           #return   
    
           if key=='B':
               spreadsheet.set('t0',t0)
           elif key=='C':
               l0=spreadsheet.getContents('l0')
               w0=spreadsheet.getContents('w0')
               sita=math.atan(float(l0)/float(w0))
               spreadsheet.set('sita',str(sita))
                
           App.ActiveDocument.recompute() 
           return
    def create(self): 
         doc=App.activeDocument
         key=self.comboBox_type.currentText()
         if key=='A':
             fname='turnBackleA.FCStd'
         elif key=='B':    
             fname='turnBackleB.FCStd'
         elif key=='C':    
             fname='turnBackleC.FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'turnBackle_data',fname) 
         print(joined_path)
         Gui.ActiveDocument.mergeProject(joined_path)
         #try:
         #    objs=doc.Objects
         #    if objs:
         #        last_obj=objs[-1] 
         #except:
         #    pass
         #Gui.activateWorkbench("DraftWorkbench")
         #Gui.Selection.addSelection(last_obj)
         Gui.runCommand('Draft_Move',0) 

class main():
        #print('ccccccccccccccccccccccccccccccccccccccccccccccccccc')
        d = QtGui.QWidget()
        
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
        