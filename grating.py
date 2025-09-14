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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 350)
        Dialog.move(1000, 0)

        #床面幅W
        self.label_W = QtGui.QLabel('W[mm',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 18, 60, 12))
        self.lineEdit_W = QtGui.QLineEdit('500',Dialog)
        self.lineEdit_W.setGeometry(QtCore.QRect(80, 15, 80, 22))
        self.lineEdit_W.setAlignment(QtCore.Qt.AlignCenter)
        #床面長L
        self.label_L = QtGui.QLabel('L[mm',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 38, 60, 12))
        self.lineEdit_L = QtGui.QLineEdit('500',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(80, 35, 80, 22))
        self.lineEdit_L.setAlignment(QtCore.Qt.AlignCenter)
        #床面高H
        self.label_H = QtGui.QLabel('t[mm',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 73, 60, 12))
        self.lineEdit_H = QtGui.QLineEdit('44',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(80, 65, 80, 22))
        self.lineEdit_H.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(75, 90, 50, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(75, 115, 50, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(75, 140, 50, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 170, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")
        fname='grating.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "grating_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        #self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "grating", None))

    def update(self):
          # スプレッドシートを選択
         #spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         #Gui.Selection.clearSelection()
         #Gui.Selection.addSelection(spreadsheet)
        #selection = Gui.Selection.getSelection()
        ## 選択したスプレッドシートを取得
        #if selection:
        #    for obj in selection:
        #        if obj.TypeId == "Spreadsheet::Sheet":
        #            # スプレッドシートが見つかった場合の処理
        #            spreadsheet = obj
         w0=self.lineEdit_W.text()
         l0=self.lineEdit_L.text()
         t0=self.lineEdit_H.text()
         spreadsheet.set('B2',w0)
         spreadsheet.set('B3',l0)
         spreadsheet.set('B4',t0)
         c00 = Gui.Selection.getSelection()
         if c00:
             obj = c00[0]
         try:
             #obj.addProperty("App::PropertyString", "Standard",'Standard')
             obj.Standard='W='+w0+'  L='+l0+'  t='+t0
             
         except:
             print('error')
             pass
         obj.mass=obj.Shape.Volume*obj.g0*1000/10**9         
         App.ActiveDocument.recompute()
         
    def create(self): 
         doc = App.ActiveDocument
         fname='grating.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'grating_data',fname) 
         #print(joined_path)
         try:
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

    def read_data(self):
         global spreadsheet
         global Grating
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.Label[:7]=='Grating':
                         Grating=obj
                     elif obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            