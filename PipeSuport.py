# -*- coding: utf-8 -*-
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
import FreeCAD as App
import FreeCADGui as Gui
from pspt_data import ParamS01
from pspt_data import ParamS02
from pspt_data import ParamS04
from pspt_data import ParamS05
from pspt_data import ParamS06
from pspt_data import ParamS08
from pspt_data import ParamS10
from pspt_data import psuport_data
DEBUG = True


class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        return

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 280)
        Dialog.move(1000, 0)
        #形式
        self.label = QtGui.QLabel('type',Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(100, 10, 100, 22))
        self.comboBox.setObjectName("comboBox")
        #形鋼
        self.label_3 = QtGui.QLabel('shapedSteel',Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 36, 81, 21))
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 36, 100, 22))
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName("comboBox_3")
        #形鋼サイズ
        self.label_8 = QtGui.QLabel('size',Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.label_8.setObjectName("label_8")
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(100, 60, 100, 22))
        self.comboBox_4.setMaxVisibleItems(10)
        self.comboBox_4.setObjectName("comboBox_4")
        #スパンL
        self.label_2 = QtGui.QLabel('spanL[mm]',Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 85, 81, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_L = QtGui.QLineEdit('300',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(100, 85, 69, 22))
        self.lineEdit_L.setObjectName("lineEdit")
        #垂直材
        #H(mm)
        self.label_5 = QtGui.QLabel('H[mm]',Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 132, 81, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtGui.QLineEdit('300',Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 129, 71, 20))
        self.lineEdit.setObjectName("lineEdit")
        #H1(mm)
        self.label_6 = QtGui.QLabel('H1[mm]',Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 152, 81, 20))
        self.label_6.setObjectName("label_6")
        self.lineEdit_2 = QtGui.QLineEdit('300',Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 150, 71, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        #斜材角度
        self.label_k = QtGui.QLabel('degree[deg]',Dialog)
        self.label_k.setGeometry(QtCore.QRect(10, 180, 81, 20))
        self.label_k.setObjectName("label_k")
        self.comboBox_k = QtGui.QComboBox(Dialog)
        self.comboBox_k.setGeometry(QtCore.QRect(100, 180, 71, 20))
        self.comboBox_k.setObjectName("comboBox_k")
        #ベースプレート
        #checkbox
        self.checkbox = QtGui.QCheckBox('basePlate',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(210, 0, 130, 21))
        self.checkbox.setObjectName("checkbox")
        self.checkbox.setChecked(True)

        #板厚
        self.label_10 = QtGui.QLabel('thickness',Dialog)
        self.label_10.setGeometry(QtCore.QRect(210, 20, 71, 21))
        self.label_10.setObjectName("label_10")
        self.comboBox_5 = QtGui.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(280, 20, 69, 22))
        self.comboBox_5.setMaxVisibleItems(10)
        self.comboBox_5.setObjectName("comboBox_5")
        #横幅
        self.label_x = QtGui.QLabel('X[mm]',Dialog)
        self.label_x.setGeometry(QtCore.QRect(210, 44, 71, 21))
        self.lineEdit_x = QtGui.QLineEdit('',Dialog)
        self.lineEdit_x.setGeometry(QtCore.QRect(280, 44, 71, 20))
        #縦長
        self.label_x = QtGui.QLabel('Y[mm]',Dialog)
        self.label_x.setGeometry(QtCore.QRect(210, 66, 71, 21))
        self.lineEdit_y = QtGui.QLineEdit('',Dialog)
        self.lineEdit_y.setGeometry(QtCore.QRect(280, 66, 71, 20))
        #img
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(220, 130, 131, 111))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        #実行      
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(250, 250, 75, 23))
        self.pushButton.setObjectName("pushButton")
        
        self.comboBox.addItems(psuport_data.type)
        self.comboBox_k.addItems(psuport_data.kaku)
        self.comboBox_3.addItems(psuport_data.katakou)
        self.comboBox_5.addItems(psuport_data.ita_t)
        self.comboBox_5.setCurrentIndex(3)
        #self.comboBox_6.addItems(psuport_data.bolt_d)
        #self.comboBox_6.setCurrentIndex(3)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(1)
        self.comboBox_4.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_4.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        #self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "pipeSupport", None))
            
    def onA(self):
        return

    def onType(self):
        global key
        global key1
        self.comboBox_3.clear()
        key = self.comboBox.currentIndex()
        key1=self.comboBox_3.currentIndex()

        if key==0:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_01_a'
            self.lineEdit_2.setText('')
            self.lineEdit_2.setEnabled(False)
            self.label_6.setText('')

        elif key==1:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_02_a'

            if key1==0:
                self.lineEdit_2.setText('')
                self.lineEdit_2.setEnabled(False)
                self.label_6.setText('')
            elif key1==10:
                self.lineEdit_2.setEnabled(True)
                self.lineEdit_2.setText('150')
        elif key==2:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_03_a'
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_2.setText('150')
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==3:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_04_a'
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('')
            self.label_6.setText('')
        elif key==4:
            self.comboBox_3.addItems(psuport_data.katakou[2:3])
            img='s_05_a'
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.label_5.setText('')
            self.label_6.setText('')
            self.label_2.setText('H[mm]')
        elif key==5:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_06_a'
            self.lineEdit.setText('500')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setText('L[mm}')
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
        elif key==6:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_07_a'
            self.lineEdit.setText('500')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setText('200')
            self.lineEdit_2.setEnabled(True)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==7:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_08_a'
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
        elif key==8:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_09_a'
            self.lineEdit_2.setText('200')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==9:
            self.comboBox_3.addItems(psuport_data.sichu)
            img='s_10_a'
            self.lineEdit.setText('1000')
            self.lineEdit_2.setText('')
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
        if key==9:
            self.comboBox_5.setCurrentIndex(3)

        pic=img + '.jpg'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "pspt_data",pic)
        self.label_7.setPixmap(QtGui.QPixmap(joined_path))
    def onKatakou(self):
        global key1
        global katakou_size
        key1=self.comboBox_3.currentIndex()
        if key<=8:
            if key==4:
                katakou_size=psuport_data.RB_ss_size
            else:
                if key1==0:
                    katakou_size=psuport_data.angle_ss_size
                elif key1==1:
                    katakou_size=psuport_data.channel_ss_size
        elif key==9:
            if key1==0:#支柱
                katakou_size=psuport_data.SGP_size
            elif key1==1:#笠木
                katakou_size=psuport_data.channel_ss_size

        self.comboBox_4.clear()
        self.comboBox_4.addItems(katakou_size)

    def onSize(self):
        global size
        global sa
        global sa2
        global size1
        global size2
        #global W
        #global B
        size=self.comboBox_4.currentText()
        if key<=8:
            katakou=self.comboBox_3.currentText()
            if key1==0:
                try:
                    sa=psuport_data.angle_ss_equal[size]
                except:
                    pass

                A=sa[0]
                W=A+50
                B=A+20
                self.lineEdit_x.setText(str(W))
                self.lineEdit_y.setText(str(B))
            elif key1==1:
                
                try:
                    sa=psuport_data.channel_ss[size]
                except:
                    pass   
                W=sa[0]+50
                B=sa[1] +20
                self.lineEdit_x.setText(str(W))
                self.lineEdit_y.setText(str(B))
            elif key1==2:
                sa=psuport_data.STK_ss[size]
                W=sa[0]
                B=sa[1]     
            else:
                pass

            if key1==0:
                try:
                    sa=psuport_data.angle_ss_equal[size]
                except KeyError:
                    pass
            elif key1==1:
                try:
                    sa=psuport_data.channel_ss[size]
                except KeyError:
                    pass
        elif key==9:
            
            try:
                if key1==0:
                    #size1=size
                    sa=psuport_data.SGP[size]
                elif key1==1:
                    #size2=size
                    sa=psuport_data.channel_ss[size]
                self.lineEdit_x.setText('200')
                self.lineEdit_y.setText('')    
            except:
                pass
    def create(self):
        global L
        global x0
        global c1
        global vx
        global vy
        global vz
        global A
        global t
        global w0
        global h0
        global pface_c
        global D
        global t0
        global sa

        x0=1
        vz=1
        key = self.comboBox.currentIndex()
        key1=self.comboBox_3.currentIndex()
        Type=self.comboBox.currentText()
        label=Type
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyString", "Type",'Type').Type=Type
        #print(Type)
        if key==0:#S01
            katakou=self.comboBox_3.currentText()
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "BasePlate",'BasePlate').BasePlate = True 
            else:    
                obj.addProperty("App::PropertyBool", "BasePlate",'BasePlate').BasePlate = False  
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou

            if key1==0:#アングル
                L1=float(self.lineEdit_L.text())
                H=float(self.lineEdit.text())
                t0=float(self.comboBox_5.currentText())
                #d=float(self.comboBox_6.currentText())
                W=float(self.lineEdit_x.text())
                B=float(self.lineEdit_y.text())
                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
                obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
                obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B

                obj.size=psuport_data.angle_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.angle_ss_size[i] 
                ParamS01.S01(obj) 
                obj.ViewObject.Proxy=0
            elif key1==1:#チャンネル
                #label='C' + size  
                L1=float(self.lineEdit_L.text())
                t0=float(self.comboBox_5.currentText())
                #d=float(self.comboBox_6.currentText())
                H=float(self.lineEdit.text())
                W=float(self.lineEdit_x.text())
                B=float(self.lineEdit_y.text())
                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
                obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
                obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B

                obj.size=psuport_data.channel_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.channel_ss_size[i] 
                ParamS01.S01(obj) 
                obj.ViewObject.Proxy=0
                    
        elif key==1 or key==2:#S02 S03
            katakou=self.comboBox_3.currentText()
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
            if key1==0:#アングル
                
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
                else:    
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  

                L1=float(self.lineEdit_L.text())
                H=float(self.lineEdit.text())
                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
                if key==2:
                    H1=float(self.lineEdit_2.text())
                    obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1

                W=float(self.lineEdit_x.text())
                B=float(self.lineEdit_y.text())    
                obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
                obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B    
                #d=float(self.comboBox_6.currentText())
                t0=float(self.comboBox_5.currentText())
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                obj.addProperty("App::PropertyFloat", "t0","BasePlate").t0=t0
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')

                obj.size=psuport_data.angle_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.angle_ss_size[i] 
                ParamS02.S02(obj) 
                obj.ViewObject.Proxy=0
                
            elif key1==1:#チャンネル
                #katakou=self.comboBox_3.currentText()
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
                else:    
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  

                L1=float(self.lineEdit_L.text())
                H=float(self.lineEdit.text())
                t0=float(self.comboBox_5.currentText())
                #d=float(self.comboBox_6.currentText())
                W=float(self.lineEdit_x.text())
                B=float(self.lineEdit_y.text())    
                obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
                obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B  
                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
                obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                
                if key==2:
                    H1=float(self.lineEdit_2.text())
                    obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
                
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.channel_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.channel_ss_size[i] 
                ParamS02.S02(obj) 
                obj.ViewObject.Proxy=0
                
        elif key==3:#S04
            L1=float(self.lineEdit_L.text())
            t0=float(self.comboBox_5.currentText())
            #d=float(self.comboBox_6.currentText())
            k=float(self.comboBox_k.currentText())
            katakou=self.comboBox_3.currentText()
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
            if key1==0: #アングル

                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
                else:    
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
                
                #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou

                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                #obj.addProperty("App::PropertyFloat", "t0",label).t0=t0
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                obj.addProperty("App::PropertyFloat", "k",'Dimension').k=k
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.angle_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.angle_ss_size[i] 
                ParamS04.S04(obj) 
                obj.ViewObject.Proxy=0
                
            elif key1==1:
                katakou=self.comboBox_3.currentText()
                #label='S04_C'+size
                L1=float(self.lineEdit_L.text())
                t0=float(self.comboBox_5.currentText())
                #d=float(self.comboBox_6.currentText())
                #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
                else:    
                    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  

                #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
                #obj.addProperty("App::PropertyInteger", "key",label).key=key
                #obj.addProperty("App::PropertyInteger", "key1",label).key1=key1
                obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
                #obj.addProperty("App::PropertyFloat", "d",label).d=d
                obj.addProperty("App::PropertyFloat", "k",'Dimension').k=k
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.channel_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.channel_ss_size[i] 
                ParamS04.S04(obj) 
                obj.ViewObject.Proxy=0
            
        elif key==4:#05
            #b='s05'
            H1=float(self.lineEdit_L.text())
            t=float(self.comboBox_5.currentText())
            d1=float(self.comboBox_4.currentText())
            #d=float(self.comboBox_6.currentText())
            #label=b
            #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            #obj.addProperty("App::PropertyInteger", "key",label).key=key
            obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t
            obj.addProperty("App::PropertyFloat", "d1",'Dimension').d1=d1
            #obj.addProperty("App::PropertyFloat", "d",label).d=d
            ParamS05.S05(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key==5 or key==6:#s06 s07

            if key==5:
                #b='s06'
                pass
            elif key==6:
                #b='s07'
                H1=float(self.lineEdit_2.text())
            L1=float(self.lineEdit_L.text())
            H=float(self.lineEdit.text())
            t0=float(self.comboBox_5.currentText())
            #d=float(self.comboBox_6.currentText())
            katakou=self.comboBox_3.currentText()
            '''
            if key1==0:
                label=b
            elif key1==1:
                label=b
            '''
            #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            else:    
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou

            #obj.addProperty("App::PropertyInteger", "key",label).key=key
            #obj.addProperty("App::PropertyInteger", "key1",label).key1=key1
            obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            W=float(self.lineEdit_x.text())
            B=float(self.lineEdit_y.text())    
            obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B  
            if key==6:
                obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
            obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            #obj.addProperty("App::PropertyFloat", "d",label).d=d
            if key1==0:#アングル
                label='s07'
                #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.angle_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.angle_ss_size[i] 
                ParamS06.S06(obj) 
                obj.ViewObject.Proxy=0
            elif key1==1:
                label='s07_C'+size
                H0=float(sa[0])
                B=float(sa[1])
                t1=float(sa[2])
                r1=float(sa[4])
                r2=float(sa[5])
                Cy=float(sa[8])*10
                t2=float(sa[3])
                obj.addProperty("App::PropertyEnumeration", "size",label)
                obj.size=psuport_data.channel_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.channel_ss_size[i] 
                ParamS06.S06(obj) 
                obj.ViewObject.Proxy=0
            
        elif key==7 or key==8:#s08 s09
            '''
            if key==7:
                #b='s08'
                pass
            elif key==8:
                #b='s09'
            '''
            L1=float(self.lineEdit_L.text())
            H=float(self.lineEdit.text())
            if key==8:
                H1=float(self.lineEdit_2.text())

            t0=float(self.comboBox_5.currentText())
            #d=float(self.comboBox_6.currentText())
            katakou=self.comboBox_3.currentText()
            '''
            if key1==0:
                label=b+'L'+size
            elif key1==1:  
                label=b+'C'+size  

            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            '''

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            else:    
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
            #obj.addProperty("App::PropertyInteger", "key",label).key=key
            #obj.addProperty("App::PropertyInteger", "key1",label).key1=key1
            obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            if key==8:
                obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1

            obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            W=float(self.lineEdit_x.text())
            B=float(self.lineEdit_y.text())    
            obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B    
            #obj.addProperty("App::PropertyFloat", "d",label).d=d
            if key1==0:#アングル
                #label=b+'_L'+size
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.angle_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.angle_ss_size[i] 
                ParamS08.S08(obj) 
                obj.ViewObject.Proxy=0
            elif key1==1:
                #label=b+'_C'+size
                obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                obj.size=psuport_data.channel_ss_size
                i=self.comboBox_4.currentIndex()
                obj.size=psuport_data.channel_ss_size[i] 
                ParamS08.S08(obj) 
                obj.ViewObject.Proxy=0

        elif key==9:
            #b='s10'
            L1=float(self.lineEdit_L.text())
            H=float(self.lineEdit.text())
            t=float(self.comboBox_5.currentText())
            katakou=self.comboBox_3.currentText()
            #label=b+size
            #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            '''
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            else:    
                obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
            '''
            #obj.addProperty("App::PropertyInteger", "key",label).key=key
            obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou

            obj.addProperty("App::PropertyEnumeration", "Post",'Post')
            obj.Post=psuport_data.SGP_size
            i=self.comboBox_4.currentIndex()
            obj.Post=psuport_data.SGP_size[i]

            obj.addProperty("App::PropertyEnumeration", "TopBeam",'TopBeam')
            obj.TopBeam=psuport_data.channel_ss_size
            i=self.comboBox_4.currentIndex()
            obj.TopBeam=psuport_data.channel_ss_size[i]
            
            obj.addProperty("App::PropertyFloat", "L1",'TopBeam').L1=L1
            obj.addProperty("App::PropertyFloat", "H",'Post').H=H
            obj.addProperty("App::PropertyFloat", "t",'BasePlate').t=t
            W=float(self.lineEdit_x.text())
            obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            
            ParamS10.S10(obj) 
            obj.ViewObject.Proxy=0    

class Main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)





