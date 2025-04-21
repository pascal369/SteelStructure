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

blt_size=['M3','M4','M5','M8','M10','M12','M14','M16']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 350)
        Dialog.move(1500, 0)
        
        #ねじ径　diameter
        self.label_blt = QtGui.QLabel('ねじ径',Dialog)
        self.label_blt.setGeometry(QtCore.QRect(10, 18, 150, 12))
        self.combo_blt = QtGui.QComboBox(Dialog)
        self.combo_blt.setGeometry(QtCore.QRect(80, 10, 50, 22))
        self.combo_blt.setEditable(True)
        #首下長さ length　
        self.label_t = QtGui.QLabel('首下長さ',Dialog)
        self.label_t.setGeometry(QtCore.QRect(10, 33, 150, 12))
        self.le_t = QtGui.QLineEdit('20',Dialog)
        self.le_t.setGeometry(QtCore.QRect(80, 60, 35, 22))
        #作成
        self.pushButton = QtGui.QPushButton('作成',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 85, 50, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('更新',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(70, 85, 50, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(130, 85, 50, 22))

         #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 135, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'ThreadHoll.png')
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.combo_blt.addItems(blt_size)


        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "EndPlate", None))
        
    def read_data(self):
         
         global spreadsheet
         global ThreadRod
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.Label=='ThreadRod':
                         ThreadRod=obj
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
                         
                         self.combo_blt.setCurrentText(spreadsheet.getContents('size')[1:])
                         self.le_t.setText(spreadsheet.getContents('length')) 
                         
    def update(self):
         
         #selection = Gui.Selection.getSelection()
        
         length=self.le_t.text()
         size=self.combo_blt.currentText()
         
         for i in range(2,10):
              size_value = spreadsheet.getContents('A'+str(i))
              if size == size_value[1:]:
                break
         Db=spreadsheet.getContents('B'+str(i)) 
         ThreadRod.diameter=size
         print(ThreadRod.diameter)
         
         
         #tw=washer.t
         #print(tw)
         #bolt.dia=size
        
         
        
         
         
         spreadsheet.set('size',size)
         spreadsheet.set('length',str(length))
         spreadsheet.set('Db',Db)
         
                            
         App.ActiveDocument.recompute()

    def create(self): 
        
         fname='ThreadedHoll.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,fname) 
         #print(joined_path)
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
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)                  