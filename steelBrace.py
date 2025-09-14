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

type=['01','02','03','04',]
angle=['20x20x3','20x20x3','25x25x3','30x30x3','30x30x5','40x40x3','40x40x5','50x50x4','50x50x6',
       '65x65x6','65x65x8','75x75x6','75x75x9','75x75x12','90x90x7','90x90x10','90x90x13',
       '100x100x7','100x100x10','100x100x13','130x130x9','130x130x12','130x130x15',
       '150x150x12','150x150x15','150x150x19','200x200x15','200x200x20','200x200x25']
angleW=['20','30','40','50','65','75','90','100','130','150','200']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 380)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 200, 200, 200))
        self.label_6.setText("")

        #type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 80, 22))
        #angle
        self.label_angle = QtGui.QLabel('AngleWidth',Dialog)
        self.label_angle.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.comboBox_angle = QtGui.QComboBox(Dialog)
        self.comboBox_angle.setGeometry(QtCore.QRect(80, 35, 80, 22))

        #幅W
        self.label_W = QtGui.QLabel('W[mm',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 63, 60, 12))
        self.lineEdit_W = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_W.setGeometry(QtCore.QRect(80, 60, 80, 22))
        self.lineEdit_W.setAlignment(QtCore.Qt.AlignCenter)
        #高H
        self.label_H = QtGui.QLabel('H[mm',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 88, 60, 12))
        self.lineEdit_H = QtGui.QLineEdit('2200',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(80, 85, 80, 22))
        self.lineEdit_H.setAlignment(QtCore.Qt.AlignCenter)
        #ガセットプレートサイズ
        self.label_L = QtGui.QLabel('GPL[mm',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 113, 60, 12))
        self.lineEdit_L = QtGui.QLineEdit('300',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(80, 110, 80, 22))
        self.lineEdit_L.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(75, 135, 50, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(75, 160, 50, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(75, 185, 50, 22))

        self.comboBox_type.addItems(type)
        self.comboBox_angle.addItems(angle)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.ontype)
        self.comboBox_type.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onImport)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "steelBraces", None))

    def ontype(self):
        mytype=self.comboBox_type.currentText()
        fname='steelBrace'+mytype+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'StlStu_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        return
    def onImport(self):
        global spreadsheet
        global anglesteel
        global anglesteelB
        selection = Gui.Selection.getSelection()
        #self.comboBox_angle.clear()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     #print(obj.Label)

                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj 
                     elif obj.Label=='AngleSteel':
                          anglesteel=obj
                     elif obj.Label=='AngleSteelB':
                          anglesteelB=obj     

        try:             
            self.lineEdit_W.setText(spreadsheet.getContents('W0'))    
            self.lineEdit_L.setText(spreadsheet.getContents('GPL'))          
            self.lineEdit_H.setText(spreadsheet.getContents('H0')) 
            self.comboBox_angle.setEditable(True)
            self.comboBox_angle.setCurrentText(spreadsheet.getContents('myAngle')[1:])
            self.comboBox_type.setCurrentText(spreadsheet.getContents('key')[1:])

        except:
            self.comboBox_angle.setCurrentText(spreadsheet.getContents('myAngle'))
            return
       
    def update(self):
             global B0
             key=self.comboBox_angle.currentText()
             
             for i in range(13,40):
                 #print(key,spreadsheet.getContents('A'+str(i)))
                 if key==spreadsheet.getContents('A'+str(i))[1:]:
                     #print(key,spreadsheet.getContents('A'+str(i)))
                     B0=spreadsheet.getContents('B'+str(i))
                     break
             try:
                 myW=self.lineEdit_W.text()
                 myL=self.lineEdit_L.text()
                 myH=self.lineEdit_H.text()
                 spreadsheet.set('B2',myW)
                 spreadsheet.set('B3',myH)
                 spreadsheet.set('B5',myL)
                 spreadsheet.set('B11',B0)
                 spreadsheet.set('myAngle',key)
                 anglesteel.size=key
                 anglesteelB.size=key
                 #print(key,B0)
             except:
                  pass    
             
             c00 = Gui.Selection.getSelection()
             if c00:
                 obj = c00[0]
             try:
                 obj.Standard='L'+key+'  W0='+myW+'  H0='+myH
                 print(obj.Standard)
             except:
                 pass
             obj.mass=obj.Shape.Volume*obj.g0*1000/10**9 
             App.ActiveDocument.recompute()
         
    def create(self): 
         doc = App.ActiveDocument
         mytype=self.comboBox_type.currentText()
         fname='steelBrace'+mytype+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'StlStu_data',fname) 
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