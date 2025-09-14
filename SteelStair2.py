# -*- coding: utf-8 -*-

import os
import sys
import csv
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import FreeCAD
import FreeCADGui as Gui
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import FreeCADGui
from StlStr_data2 import ParamStair2
from StlStr_data2 import StlStrdata2

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 260)
        Dialog.move(1000, 0)

#形式
        self.label = QtGui.QLabel('Type',Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(140, 10, 69, 22))
        self.comboBox.setObjectName("comboBox")        
#形鋼
        self.label_3 = QtGui.QLabel('Shaped steel',Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 36, 81, 21))
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(140, 36, 81, 22))
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName("comboBox_3")        
#形鋼サイズ
        self.label_8 = QtGui.QLabel('Size',Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.label_8.setObjectName("label_8")
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(140, 60, 81, 22))
        self.comboBox_4.setMaxVisibleItems(10)
        self.comboBox_4.setObjectName("comboBox_4")        
#L
        self.lineEdit_L = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(140, 85, 60, 22))
        self.lineEdit_L.setObjectName("lineEdit_L")
        self.label_L = QtGui.QLabel('L[mm]',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 85, 81, 21))
        self.label_L.setObjectName("label_L")
#L1
        self.label_L1 = QtGui.QLabel('L1[mm]',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(10, 110, 81, 20))
        self.label_L1.setObjectName("label_L1")
        self.lineEdit_L1 = QtGui.QLineEdit('70',Dialog)
        self.lineEdit_L1.setGeometry(QtCore.QRect(140, 110, 60, 22))
        self.lineEdit_L1.setObjectName("lineEdit_L1")
#H
        self.label_H = QtGui.QLabel('H[mm]',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 135, 81, 20))
        self.label_H.setObjectName("label_H")        
        self.lineEdit_H = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(140, 135, 60, 22))
        self.lineEdit_H.setObjectName("lineEdit_H")
#W
        self.label_W = QtGui.QLabel('Stairs width W[mm]',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 165, 100, 20))
        self.label_W.setObjectName("label_W")
        self.lineEdit_W = QtGui.QLineEdit('800',Dialog)
        self.lineEdit_W.setGeometry(QtCore.QRect(140, 165, 60, 22))
        self.lineEdit_W.setObjectName("lineEdit_W")        
#image
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(230, 90, 150, 150))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
#ベースプレート       
        self.label_9 = QtGui.QLabel('Base plate',Dialog)
        self.label_9.setGeometry(QtCore.QRect(255, 0, 130, 21))
        self.label_9.setObjectName("label_9")
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
#板厚        
        self.label_10 = QtGui.QLabel('Bord width[mm]',Dialog)
        self.label_10.setGeometry(QtCore.QRect(210, 16, 100, 21))
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
  
        self.comboBox_5 = QtGui.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(320, 16, 69, 22))
        self.comboBox_5.setMaxVisibleItems(10)
        self.comboBox_5.setObjectName("comboBox_5")

#高所  
        self.label_p = QtGui.QLabel('High place',Dialog)
        self.label_p.setGeometry(QtCore.QRect(240, 40, 71, 21))
        self.label_p.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_p.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_p.setObjectName("label_p")
        self.checkbox = QtGui.QCheckBox('HighPlace',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(320, 40, 20, 23))
        self.checkbox.setChecked(False)


#実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 230, 70, 23))
        self.pushButton.setObjectName("pushButton")
#mass
        self.pushButton_2 = QtGui.QPushButton('Mass culculation',Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 230, 100, 23))
        self.pushButton_2.setObjectName("pushButton_2")  

# 手すり位置
        self.label_ichi = QtGui.QLabel('Handrail Position',Dialog)
        self.label_ichi.setGeometry(QtCore.QRect(10, 200, 100, 21))
        self.combo_ichi = QtGui.QComboBox(Dialog)
        self.combo_ichi.setGeometry(QtCore.QRect(140, 200, 61, 23))
        self.combo_ichi.setMaxVisibleItems(10)
        self.combo_ichi.setObjectName("combo_ichi")

        self.comboBox.addItems(StlStrdata2.type)
        self.combo_ichi.addItems(StlStrdata2.ichi)
        self.comboBox_3.addItems(StlStrdata2.katakou)
        self.comboBox_5.addItems(StlStrdata2.ita_t)
        self.comboBox_5.setCurrentIndex(3)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_4.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_4.setCurrentIndex(1)
        self.combo_ichi.currentIndexChanged[int].connect(self.onType)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("pressed()"), self.on_mass)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'for the second floor', None))
    def on_mass(self):
        doc = FreeCAD.ActiveDocument
        object_list = []
        for obj in doc.Objects:
            if hasattr(obj, "mass"):
                object_list.append([obj.Label, 1, obj.mass])
            else:
                try:
                    object_list.append([obj.Label, 1, 0.0])
                except:
                    pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        try:
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write the header row
                writer.writerow(['Object Name', 'Count', 'mass[kg]'])
                for obj in object_list:
                    writer.writerow(obj)
        except:
            pass        

    def onType(self):
        global key
        global key1
        global key2
        global y

        self.comboBox_3.clear()
        key = self.comboBox.currentIndex()
        key1=self.comboBox_3.currentIndex()
        key2=self.combo_ichi.currentText()
        self.comboBox_3.addItems(StlStrdata2.katakou[:2])
        if key==0:
            img='stairs_1'
            pic=img+'.png'
        elif key==1:
            img='手すり_0'
            pic=img+'.jpg'
        elif key==2:
            img='手すり_1'
            pic=img+'.jpg'
        elif key==3:
            img='手すり_2'
            pic=img+'.jpg'    
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "StlStr_data2",pic)
        self.label_7.setPixmap(QtGui.QPixmap(joined_path))

    def onKatakou(self):
        global key1
        global katakou_size
        key1=self.comboBox_3.currentIndex()
        if key<=1:
            katakou_size=StlStrdata2.channel_ss_size
        self.comboBox_4.clear()
        self.comboBox_4.addItems(katakou_size)

    def onSize(self):
        global size
        global sa
        global sa2
        global size2
        size=self.comboBox_4.currentText()
        try:
            sa=StlStrdata2.channel_ss[size]
        except:
            pass
    def create(self):
        L=float(self.lineEdit_L.text())
        L1=float(self.lineEdit_L1.text())
        H=float(self.lineEdit_H.text())
        w=float(self.lineEdit_W.text())
        H0=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        r1=float(sa[4])
        r2=float(sa[5])
        Cy=float(sa[8])*10
        t2=float(sa[3])
        t=float(self.comboBox_5.currentText())

        JPN='鋼製階段'

        label = 'SteelStair'
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

        obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  
        #obj.addProperty("App::PropertyInteger", "key1",'Type').key1=key1
        obj.addProperty("App::PropertyEnumeration", "Position",'Type')
        obj.Position = StlStrdata2.ichi
        obj.Position = StlStrdata2.ichi[1]
        obj.Position = StlStrdata2.ichi[2]

        obj.addProperty("App::PropertyEnumeration", "type",'Type')
        obj.type=StlStrdata2.type
        i=self.comboBox.currentIndex()
        obj.type=StlStrdata2.type[i] 

        if self.checkbox.isChecked():
            obj.addProperty("App::PropertyBool",'HighPlace','Type').HighPlace = True
        else:
            obj.addProperty("App::PropertyBool",'HighPlace','Type').HighPlace = False
        
        obj.addProperty("App::PropertyFloat", "L",'Dimension').L=L
        obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
        obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
        obj.addProperty("App::PropertyFloat", "w",'Dimension').w=w
        obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

        obj.addProperty("App::PropertyEnumeration", "size",'ShapedSteel')
        obj.size=StlStrdata2.channel_ss_size
        i=self.comboBox_4.currentIndex()
        obj.size=StlStrdata2.channel_ss_size[i]

        try:        
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            Standard='H='+str(obj.H)+'  W='+str(obj.w)
            obj.Standard=Standard
        except:
            pass 

        ParamStair2.ParamStaire20(obj)
        obj.ViewObject.Proxy=0
        FreeCAD.ActiveDocument.recompute() 
        Gui.SendMsgToActiveView("ViewFit") 

        Gui.ActiveDocument.ActiveView.fitAll() 
        Gui.activateWorkbench("DraftWorkbench")
        Gui.Selection.addSelection(obj)
        Gui.runCommand('Draft_Move',0)   

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
        


