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
        Dialog.resize(250, 300)
        Dialog.move(1000, 0)

        #高さ
        self.label_H = QtGui.QLabel('Hight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.le_H = QtGui.QLineEdit('800',Dialog)
        self.le_H.setGeometry(QtCore.QRect(110, 10, 50, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)

        #長さ
        self.label_L = QtGui.QLabel('Length',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.le_L = QtGui.QLineEdit('1000',Dialog)
        self.le_L.setGeometry(QtCore.QRect(110, 35, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 60, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 60, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 85, 180, 22))

        #spinBox
        self.label_spin=QtGui.QLabel('Length',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 110, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 110, 100, 30)
        self.spinBox.setMinimum(100)  # 最小値を0.0に設定
        self.spinBox.setMaximum(10000.0)  # 最大値を100.0に設定
        self.spinBox.setValue(1000.0)
        self.spinBox.setSingleStep(50) #step
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 140, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        self.spinBox.valueChanged[int].connect(self.spinMove) 
        self.le_L.textChanged.connect(self.update)

        fname='accodionGate.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "accodionGate_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "accodionGate", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  
        
    def read_data(self):
         global spreadsheet

         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.le_H.setText(spreadsheet.getContents('H0')) 
                         self.le_L.setText(spreadsheet.getContents('L0')) 
                         self.spinBox.setValue(int(spreadsheet.getContents('L0'))) 
    def update(self):

             hight=self.le_H.text()#高さ
             length=self.le_L.text()#長さ
             spreadsheet.set('H0',hight)
             spreadsheet.set('L0',length)
             App.ActiveDocument.recompute() 
                    
             return

    def create(self): 
         fname='accodionGate.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'accodionGate_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         Gui.SendMsgToActiveView("ViewFit")
    def spinMove(self):
         r0=float(self.le_L.text())
         r1 = self.spinBox.value()
         r3=r1
         self.le_L.setText(str(r3))
         App.ActiveDocument.recompute()      

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        # スクリプトのウィンドウを取得
        script_window = FreeCADGui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            