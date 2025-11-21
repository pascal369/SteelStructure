# -*- coding: utf-8 -*-
#copyright katsuichi yamashita
import os
import sys
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCADGui as Gui
import FreeCAD as App
from StlStr_data import ParamStStairs
from StlStr_data import stlstrdata

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 335)
        Dialog.move(1000, 0)
#形式
        self.label = QtGui.QLabel('Type',Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setStyleSheet("color: black;")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(100, 10, 111, 22))
        self.comboBox.setObjectName("comboBox")        
#形鋼
        self.label_3 = QtGui.QLabel('ShapedSteel',Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 36, 81, 21))
        self.label_3.setStyleSheet("color: black;")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 36, 111, 22))
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName("comboBox_3")        
#形鋼サイズ
        self.label_8 = QtGui.QLabel('Size',Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.label_8.setStyleSheet("color: black;")
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(100, 60, 111, 22))
        self.comboBox_4.setMaxVisibleItems(10)
        self.comboBox_4.setObjectName("comboBox_4")        
#L
        self.lineEdit_L = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(100, 85, 60, 22))
        self.lineEdit_L.setObjectName("lineEdit_L")
        self.label_L = QtGui.QLabel('L[mm]',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 85, 81, 21))
        self.label_L.setStyleSheet("color: black;")
#L1
        self.label_L1 = QtGui.QLabel('L1[mm]',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(10, 110, 81, 20))
        self.label_L1.setStyleSheet("color: black;")
        self.lineEdit_L1 = QtGui.QLineEdit('1500',Dialog)
        self.lineEdit_L1.setGeometry(QtCore.QRect(100, 110, 60, 22))
        self.lineEdit_L1.setObjectName("lineEdit_L1")
#H
        self.label_H = QtGui.QLabel('H[mm]',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 135, 81, 20))
        self.label_H.setStyleSheet("color: black;")    
        self.lineEdit_H = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(100, 135, 60, 22))
        self.lineEdit_H.setObjectName("lineEdit_H")
#階段内幅w0
        self.label_w = QtGui.QLabel('StairWith_w0[mm]',Dialog)
        self.label_w.setGeometry(QtCore.QRect(10, 160, 81, 20))
        self.label_w.setStyleSheet("color: black;")
        self.lineEdit_w0 = QtGui.QLineEdit('800',Dialog)
        self.lineEdit_w0.setGeometry(QtCore.QRect(100, 160, 60, 22))
        self.lineEdit_w0.setObjectName("lineEdit_w0") 
#階段外幅w1
        self.label_w1 = QtGui.QLabel('StairWith_w1[mm]=',Dialog)
        self.label_w1.setGeometry(QtCore.QRect(10, 185, 150, 20))
        self.label_w1.setStyleSheet("color: black;")
#階段渡り幅w2
        self.label_w2 = QtGui.QLabel('w2[mm]',Dialog)
        self.label_w2.setGeometry(QtCore.QRect(10, 205, 81, 20))
        self.label_w2.setStyleSheet("color: black;")
        self.lineEdit_w2 = QtGui.QLineEdit('200',Dialog)
        self.lineEdit_w2.setGeometry(QtCore.QRect(100, 205, 60, 22))
        self.lineEdit_w2.setObjectName("lineEdit_W2")         
#階段間隔w3
        self.label_w3 = QtGui.QLabel('StairSpacing_w3[mm]',Dialog)
        self.label_w3.setGeometry(QtCore.QRect(10, 230, 81, 20))
        self.label_w3.setStyleSheet("color: black;")
        self.lineEdit_w3 = QtGui.QLineEdit('0',Dialog)
        self.lineEdit_w3.setGeometry(QtCore.QRect(100, 230, 60, 22))
        self.lineEdit_w3.setObjectName("lineEdit_W3")    
# 手すり位置
        self.label_ichi = QtGui.QLabel('RailingPosition',Dialog)
        self.label_ichi.setGeometry(QtCore.QRect(10, 255, 100, 21))
        self.label_ichi.setStyleSheet("color: black;")
        self.combo_ichi = QtGui.QComboBox(Dialog)
        self.combo_ichi.setGeometry(QtCore.QRect(100, 255, 61, 23))
        self.combo_ichi.setMaxVisibleItems(10)
        self.combo_ichi.setObjectName("combo_ichi")
# 階数
        self.label_Stry = QtGui.QLabel('Story',Dialog)
        self.label_Stry.setGeometry(QtCore.QRect(10, 280, 100, 21))
        self.label_Stry.setStyleSheet("color: black;")
        self.lineEdit_str = QtGui.QLineEdit('2',Dialog)
        self.lineEdit_str.setGeometry(QtCore.QRect(100, 280, 61, 23))
        self.lineEdit_str.setObjectName("lineEdit_str")    
#image
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(190, 90, 150, 150))
        self.label_7.setStyleSheet("color: black;")
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
#ベースプレート       
        self.label_9 = QtGui.QLabel('BasePlate',Dialog)
        self.label_9.setGeometry(QtCore.QRect(215, 0, 130, 21))
        self.label_9.setStyleSheet("color: black;")

        self.label_10 = QtGui.QLabel('Thickness[mm]',Dialog)
        self.label_10.setGeometry(QtCore.QRect(215, 16, 85, 21))
        self.label_10.setStyleSheet("color: black;")

        self.comboBox_5 = QtGui.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(310, 16, 40, 21))
        self.comboBox_5.setMaxVisibleItems(10)
        self.comboBox_5.setObjectName("comboBox_5")

#チェッカープレート       
        self.label_9c = QtGui.QLabel('CheckeredPlate',Dialog)
        self.label_9c.setGeometry(QtCore.QRect(215, 40, 130, 21))
        self.label_9c.setStyleSheet("color: black;")
        #self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        
        self.label_10c = QtGui.QLabel('Thickness[mm]',Dialog)
        self.label_10c.setGeometry(QtCore.QRect(215, 56, 85, 21))
        self.label_10c.setStyleSheet("color: black;")
        #self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10c.setObjectName("label_10")

        self.comboBox_5c = QtGui.QComboBox(Dialog)
        self.comboBox_5c.setGeometry(QtCore.QRect(310, 56, 40, 22))
        self.comboBox_5c.setMaxVisibleItems(10)
        self.comboBox_5c.setObjectName("comboBox_5c")


#廻り方向checkbox
        self.checkbox = QtGui.QCheckBox('ClockWise',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(180, 260, 120, 23))
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet("color: black;")
#中間階checkbox3
        self.checkbox3= QtGui.QCheckBox('MiddleFloor',Dialog)
        self.checkbox3.setGeometry(QtCore.QRect(280, 260, 120, 23))
        self.checkbox3.setChecked(False)
        self.checkbox3.setStyleSheet("color: black;")
#実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 305, 155, 23))
        self.pushButton.setObjectName("pushButton")

        self.comboBox.addItems(stlstrdata.type)
        self.combo_ichi.addItems(stlstrdata.ichi)

        self.comboBox_3.addItems(stlstrdata.katakou)
        
        self.comboBox_5c.addItems(stlstrdata.ch_t)


        self.comboBox_5.addItems(stlstrdata.ita_t)
        self.comboBox_5.setCurrentIndex(3)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_4.currentIndexChanged[int].connect(self.onSize)
        self.comboBox.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_4.setCurrentIndex(1)
        self.lineEdit_w0.textChanged.connect(self.onSize)
        self.combo_ichi.currentIndexChanged[int].connect(self.onType)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'steelStair', None))
    def onType(self):
        global key
        #global key1
        global Rail
        global y
        key = self.comboBox.currentIndex()
        Rail=self.combo_ichi.currentText()
        self.comboBox_3.addItems(stlstrdata.katakou[:2])
        if key==0:
            img='stairs_2'
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
        joined_path = os.path.join(base, "StlStr_data",pic)
        self.label_7.setPixmap(QtGui.QPixmap(joined_path))
    def onKatakou(self):
        global key1
        global katakou_size
        key1=self.comboBox_3.currentIndex()
        if key<=1:
            katakou_size=stlstrdata.channel_ss_size
        self.comboBox_4.clear()
        self.comboBox_4.addItems(katakou_size)

    def onSize(self):
        global size
        global sa
        global sa2
        global size2
        global w1
        size=self.comboBox_4.currentText()
        w0=float(self.lineEdit_w0.text())
        w2=float(self.lineEdit_w2.text())
        try:
            sa=stlstrdata.channel_ss[size]
        except:
            pass   
        B=float(sa[1])
        w1=w0+2*B
        label2='StairWith_w1=' + str(w1) + '[mm]'
        self.label_w1.setText(QtGui.QApplication.translate("Dialog", str(label2), None))

    def create(self):
        stry=int(self.lineEdit_str.text())    
        L=float(self.lineEdit_L.text())
        L1=float(self.lineEdit_L1.text())
        H=float(self.lineEdit_H.text())
        w0=float(self.lineEdit_w0.text())
        w2=float(self.lineEdit_w2.text())
        w3=float(self.lineEdit_w3.text())
        H0=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        r1=float(sa[4])
        r2=float(sa[5])
        Cy=float(sa[8])*10
        t2=float(sa[3])
        t=float(self.comboBox_5.currentText())
        t0=float(self.comboBox_5.currentText())

        JPN='鋼製階段'

        label = 'stair'
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyEnumeration", "Rail",label)
        obj.Rail = stlstrdata.ichi
        i=self.combo_ichi.currentIndex()
        obj.Rail = stlstrdata.ichi[i]
        obj.addProperty("App::PropertyFloat", "L",'Dimension').L=L
        obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
        obj.addProperty("App::PropertyFloat", "H0",'Dimension').H0=H
        obj.addProperty("App::PropertyFloat", "w0",'Dimension').w0=w0
        obj.addProperty("App::PropertyFloat", "w1",'Dimension').w1=w1
        obj.addProperty("App::PropertyFloat", "w2",'Dimension').w2=w2
        obj.addProperty("App::PropertyFloat", "w3",'Dimension').w3=w3
        obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t
        obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

        obj.addProperty("App::PropertyEnumeration", "size",'shape')
        obj.size=stlstrdata.channel_ss_size
        i=self.comboBox_4.currentIndex()
        obj.size=stlstrdata.channel_ss_size[i]

        obj.addProperty("App::PropertyEnumeration", "type",label)
        obj.type=stlstrdata.type
        i=self.comboBox.currentIndex()
        obj.type=stlstrdata.type[i] 

        if self.checkbox.isChecked():
            obj.addProperty("App::PropertyBool",'ClockWise',label).ClockWise = True
        else:
            obj.addProperty("App::PropertyBool",'ClockWise',label).ClockWise = False
        if self.checkbox3.isChecked():
            obj.addProperty("App::PropertyBool",'MdlFloor',label).MdlFloor = True
        else:
            obj.addProperty("App::PropertyBool",'MdlFloor',label).MdlFloor = False

        obj.addProperty("App::PropertyEnumeration", "t0",'Dimension')
        obj.t0=stlstrdata.ch_t
        i=self.comboBox_5c.currentIndex()
        obj.t0=stlstrdata.ch_t[i]
        
        obj.addProperty("App::PropertyInteger", "story",label).story=stry

        try:        
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            N=obj.story-1
            Standard='H='+str(obj.H)+'  W='+str(obj.w0)+'  n='+str(N)
            obj.Standard=Standard
        except:
            pass 
        
        ParamStStairs.Staires(obj)
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
    script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
    # 閉じるボタンを無効にする
    script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        

       

