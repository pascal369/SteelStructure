# -*- coding: utf-8 -*-
import os
import sys
import Import
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App

from ScrLib import ScrData
from ScrLib import ParamHxgNut
from ScrLib import ParamEyNut
from ScrLib import ParamSmlScrw
from ScrLib import ParamHxgBlt
from ScrLib import ParamSetScrew
from ScrLib import ParamShBlt
from ScrLib import ParamAllScrw
from ScrLib import ParamAnchBlt
from ScrLib import ParamEyeBlt
from ScrLib import ParamWasher
from ScrLib import ParamBrgNut
from ScrLib import ParamUBlt
from ScrLib import ParamUBnd
from ScrLib import ParamThreadedHoll

DEBUG = True # set to True to show debug messages
#JIS B 1181

class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 280)
        Dialog.move(1000, 0)
        #種類 type
        self.type = QtGui.QLabel('Type',Dialog)
        self.type.setGeometry(QtCore.QRect(10, 13, 50, 12))
        self.type.setObjectName("type")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(100, 10, 180, 22))
       
        #規格
        self.standard = QtGui.QLabel('Standard',Dialog)
        self.standard.setGeometry(QtCore.QRect(10, 38, 60, 22))
        #self.standard.setAlignment(QtCore.Qt.AlignLeft)
        self.comboBox_standard = QtGui.QComboBox(Dialog)
        self.comboBox_standard.setGeometry(QtCore.QRect(100, 35, 180, 22))
        
        #ねじ呼び径
        self.dia = QtGui.QLabel('Nominal',Dialog)
        self.dia.setGeometry(QtCore.QRect(10, 63, 40, 22))
        #self.dia.setObjectName("yobikei")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(100, 60, 80, 22))
        
        #フランジ規格
        self.fdia = QtGui.QLabel('flange',Dialog)
        self.fdia.setGeometry(QtCore.QRect(190, 63, 60, 22))
        #self.fdia.setObjectName("yobikei")
        self.comboBox_fdia = QtGui.QComboBox(Dialog)
        self.comboBox_fdia.setGeometry(QtCore.QRect(230, 60, 50, 22))
        
        #首下長さ
        self.kubisita = QtGui.QLabel('neckLength',Dialog)
        self.kubisita.setGeometry(QtCore.QRect(10, 85, 80, 22))
        #self.kubisita.setAlignment(QtCore.Qt.AlignCenter)
        #self.kubisita.setObjectName("kubisita")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 85, 80, 22))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        #self.lineEdit.setObjectName("lineEdit")
        #ねじ部長さ
        self.nejibu = QtGui.QLabel('threadLength',Dialog)
        self.nejibu.setGeometry(QtCore.QRect(10, 110, 110, 22))
        #self.nejibu.setAlignment(QtCore.Qt.AlignCenter)
        #self.nejibu.setObjectName("nejibu")
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 108, 80, 22))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        #self.lineEdit_2.setObjectName("lineEdit_2")
        #checkboxフランジ部
        self.checkboxf = QtGui.QCheckBox('Flange',Dialog)
        self.checkboxf.setGeometry(QtCore.QRect(190, 85, 65, 23))
        #checkboxねじ表示
        self.checkbox = QtGui.QCheckBox('Thread',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(190, 108, 61, 22))
        self.checkbox.setObjectName("checkbox")
        #creat
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 145, 250, 22))
        self.pushButton.setObjectName("pushButton")
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 175, 250, 100))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.retranslateUi(Dialog)

        self.comboBox_type.addItems(ScrData.b_type)
        self.comboBox_fdia.addItems(ScrData.flange_st)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_type.setCurrentIndex(0)

        self.comboBox_standard.setCurrentIndex(1)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_standard.setCurrentIndex(0)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.on_dia)
        self.comboBox_dia.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create_screw)
        QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL("checked()"), self.create_screw)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Screws", None))

    def on_type(self):
        global key
        key=self.comboBox_type.currentText()[:2]
        if key=='00':
            ta=ScrData.nut_st
        elif key=='01':
            ta=ScrData.bolt_st1
        elif key=='02':
            ta=ScrData.bolt_st2
        elif key=='03':
            ta=ScrData.bolt_st3
        elif key=='04':
            ta=ScrData.bolt_st4
        elif key=='05':
            ta=ScrData.bolt_st5
        elif key=='06' or key=='13':
            ta=ScrData.bolt_st6
        elif key=='07':
            ta=ScrData.bolt_st7
        elif key=='08':
            ta=ScrData.bolt_st8
        elif key=='09':
            ta=ScrData.bolt_st9
        elif key=='10':
            ta=ScrData.brg_nut_st
        elif key=='11':
            ta=ScrData.u_bolt_st
        elif key=='12':
            ta=ScrData.u_band_st 

        self.comboBox_standard.clear()
        try:
            self.comboBox_standard.addItems(ta)
        except:
            return
    def on_dia(self):
        global sa
        global L2
        st=self.comboBox_standard.currentText()
        dia=self.comboBox_dia.currentText()
        if key=='00':
            try:
                sa=ScrData.regular[dia]
            except:
                return  

        elif key=='05'  or key=='01' :
            try:
                sa=ScrData.regular[dia]
            except:
                return    
            p=sa[0]
            D0=sa[2]
            L1=D0*5
            L2=int(L1*0.75)
            self.lineEdit.setText(str(L1))
            self.lineEdit_2.setText(str(L2))
        elif key=='02':
            try:
                sa=ScrData.regular[dia]
            except:
                return    
            p=sa[0]
            D0=sa[2]
            L1=D0*5
            L2=int(L1*0.75)
            self.lineEdit.setText(str(L1))
            self.lineEdit_2.setText(str(L2))    
        elif key=='03':
            try:
                sa=ScrData.regular[dia]
            except:
                return 
            p=sa[0]
            D0=sa[2]
            self.lineEdit.setText(str(''))
            self.lineEdit_2.setText(str(D0*3-p*3))
        elif key=='04':
            if st=='Type_J':
                try:
                    sa=ScrData.anchor_J[dia]
                except:
                    return
            elif st=='Type_L':
                try:
                    sa=ScrData.anchor_L[dia]
                except:    
                    return
            L1=float(sa[2])
            L2=float(sa[5])
            self.lineEdit.setText(str(L1))
            self.lineEdit_2.setText(str(L2))
        elif key=='06' or key=='13':
            try:
                sa=ScrData.set_screw[dia]
            except:
                return
            p=sa[0]
            D0=sa[2]    
            L2=float(sa[4])
            self.lineEdit_2.setText(str(L2))
        elif key=='07':
            try:
                sa=ScrData.eye_bolt[dia]
            except:
                return
            L1=float(sa[7])
            L2=float(sa[7])-float(sa[8])
            self.lineEdit.setText(str(L1))
            self.lineEdit_2.setText(str(L2))
        elif key=='08' or key=='09':
            try:
                sa=ScrData.eye_bolt[dia]
            except:
                return
            self.lineEdit.setText(str(''))
            self.lineEdit_2.setText(str(''))
        elif key=='10':
            if st=='Bearing Nut' or st=='Bearing Washer' or st=='shaft End':
                try:
                    sa=ScrData.fine_screw[dia]
                    sa1=ScrData.brg_nut[dia]
                    D0=sa1[0]
                    p=sa1[1]
                    L=D0+p
                    self.lineEdit.setText(str(2*L))#首下
                    self.lineEdit_2.setText(str(L))#ねじ部
                except:
                    return
        elif key=='11' or key=='12':
            global size1
            global C
            if st=='U_bolt' or st=='U_band':
                try:
                    sa=ScrData.haikan_u[dia]
                except:
                    return
                try:    
                    size1=sa[0]
                except:
                    return    
                C=sa[1]
                L=sa[2]
                l=sa[3]
                self.lineEdit.setText(str(L))#首下
                self.lineEdit_2.setText(str(l))#ねじ部
        
    def on_standard(self):
        #global FC
        global pic
        global label
        dia=self.comboBox_dia.currentText()
        key=self.comboBox_type.currentText()[:2]
        st=self.comboBox_standard.currentText()
        if key=='00':
            dia=ScrData.size[3:]
            pic='img_nut_' + st + '.png'
        elif key=='01':
            dia=ScrData.size[5:]
            pic='img_bolt_' + st + '.png'
            #FC="六角ボルト JIS B 1180"
        elif key=='02':
            dia=ScrData.sh_size
            pic='img_sh_bolt.png' 
            if st=='Section1':
                #FC="六角穴付きボルト_1欄 JIS B 1176"
                return
            elif st=='Section2':
                #FC="六角穴付きボルト_2欄 JIS B 1176"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "六角穴付きボルト_2欄 JIS B 1176", None))
                return
        elif key=='03':
            dia=ScrData.size[5:]
            pic='img_all_screw.png'
            #FC="全ねじボルト JIS B 0205"
        elif key=='04':
            if st=='Type_L':
                dia=ScrData.anch_size
                pic='img_anchor_L.png'
                #FC="アンカーボルト_L形"
            elif st=='Type_J':
                dia=ScrData.anch_size
                pic='img_anchor_J.png'
                #FC="アンカーボルト_J形"
        elif key=='05':
            if st=='Pan_head':
                dia=ScrData.size[2:11]
                pic='img_pan_head.png'
                #FC="なべ小ねじ JIS B 1101"
            elif st=='Flat_head':
                dia=ScrData.size[2:11]
                pic='img_flat_head.png'
                #FC="皿小ねじ JIS B 1101"
            elif st=='Round_flat_head':
                dia=ScrData.size[2:11]
                pic='img_round_flat_head.png'
                #FC="丸皿小ねじ JIS B 1101"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "丸皿小ねじ JIS B 1101", None))
            elif st=='Truss_screw':
                dia=ScrData.size[3:10]
                pic='img_truss_screw.png'
                #FC="トラス小ねじ JIS B 1101"
            elif st=='Binding_head':
                dia=ScrData.size[3:10]
                pic='img_binding_head.png'
                #FC="バインド小ねじ JIS B 1101"
            elif st=='Round_screw':
                dia=ScrData.size[:10]
                pic='img_round_screw.png'
                #FC="丸小ねじ JIS B 1101"
            elif st=='Flat_screw':
                dia=ScrData.size[:10]
                pic='img_flat_screw.png'
                #FC="平小ねじ JIS B 1101"
        elif key=='06' or key=='13':
            dia=ScrData.size[2:14]
            if key=='06':
                if st=='Flat_head_1' :
                    pic='img_flat_s_head.png'
                    #FC="六角穴付き止めねじ_平先_1欄"
                elif st=='Flat_head_2' :
                    pic='img_flat_s_head.png'
                    #FC="六角穴付き止めねじ_平先_2欄"
                elif st=='Point_ahead_1' :
                    pic='img_point_ahead.png'
                    #FC="六角穴付き止めねじ_とがり先_1欄"
                elif st=='Point_ahead_2':
                    pic='img_point_ahead.png'
                    #FC="六角穴付き止めねじ_とがり先_2欄"
            elif key=='13':
                
                pic='img_threadedHoll.png' 
                #FC='ねじ穴'       
        elif key=='07':
            dia=ScrData.size[9:]
            pic='img_eyebolt.png'
            #FC="アイボルト"
        elif key=='08':
            dia=ScrData.size[9:]
            pic='img_eyenut.png'
            #FC="アイナット"
        elif key=='09':
            b='JIS B 1256_'
            if st=='Small circle':
                dia=ScrData.size[:16]
                pic='img_washer.png'
                #FC=b+"小形丸"
            elif st=='Polish circle':
                dia=ScrData.size[3:16]
                pic='img_washer.png'
                #FC=b+"みがき丸"
            elif st=='Common circle':
                dia=ScrData.size[8:16]
                pic='img_washer.png'
                #FC=b+"並丸"
            elif st=='Small corner':
                dia=ScrData.size[8:16]
                pic='img_cwasher.png'
                #FC=b+"小形角"
            elif st=='Large angle':
                dia=ScrData.size[8:16]
                pic='img_cwasher.png'
                #FC=b+"大形角"
            elif st=='Spring_washer_general':
                b='JIS B 1251_'
                dia=ScrData.size[3:16]
                pic='img_swasher.png'
                #FC=b+"ばね一般"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", b+"ばね一般" , None))
            elif st=='Spring_washer_heavy':
                b='JIS B 1251_'
                dia=ScrData.size[8:16]
                pic='img_swasher.png'
                #FC=b+"ばね重荷重"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", b+"ばね重荷重" , None))
            elif st=='Inclined_washer_5degrees':
                dia=ScrData.size[10:]
                pic='img_incwasher.png'
                #FC="傾斜5度"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "傾斜5度" , None))
            elif st=='Inclined_washer_8degrees':
                dia=ScrData.size[10:]
                pic='img_incwasher.png'
                #FC="傾斜8度"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "傾斜8度" , None))
        elif key=='10':
            if st=='Bearing Nut':
                dia=ScrData.brg_size
                pic='img_brg_nut.png'
                #FC="ベアリングナット"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "ベアリングナット" , None))
            elif st=='Bearing Washer':
                dia=ScrData.brg_size
                pic='img_brg_washer.png'
                #FC="ベアリングナット ワッシャー"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "Bearing Washer" , None))
            elif st=='Shaft End':
                dia=ScrData.brg_size
                pic='img_shaft_end.png'
                #FC="軸端"
                #self.type2.setText(QtGui.QApplication.translate("Dialog", "軸端" , None))
        elif key=='11':
            if st=='U_bolt':
                dia=ScrData.U_size
                pic='img_u_bolt.png'
                #FC='Uボルト'
        elif key=='12':
            if st=='U_band':
                dia=ScrData.U_size
                pic='img_u_band.png'
                #FC='Uバンド'

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "ScrLib",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))
        self.comboBox_dia.clear()
        try:
            self.comboBox_dia.addItems(dia)
        except:
            return

    def create_screw(self):
        global c00
        key=self.comboBox_type.currentText()[:2]
        st=self.comboBox_standard.currentText()
        dia=self.comboBox_dia.currentText()
        
        if key!='10':
            if key=='11' or key=='12':
                sa = ScrData.regular[size1]
            else:
                #sa = ScrData.regular[dia]
                pass
            if key=='00' or key=='08':
                size1=dia
                sa = ScrData.regular[size1]
                if key=='00':
                    label='hexagon_nut'
                elif key=='08':
                    label='eynut'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='00':
                    obj.dia=ScrData.size[5:]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+3]
                    obj.addProperty("App::PropertyEnumeration", "st",label)
                    obj.st=ScrData.nut_st
                    if st=='Type1':
                        B=sa[6]
                    else:    
                        B=sa[7]
                        
                    obj.addProperty("App::PropertyFloat", "B",label).B=B
                elif key=='08': 
                    obj.dia=ScrData.size[9:]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+9]   
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                if key=='00':
                    #ParamHxgNut.HxgNut(obj)
                    ParamHxgNut.HxgNut(obj)
                elif key=='08':
                    ParamEyNut.EyNut(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute() 
            elif key=='01':
                L1=float(self.lineEdit.text())#首下長さ
                L2=float(self.lineEdit_2.text())#ねじ部長さ
                label='hexagon_bolt'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyString", "key",label).key=key
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=ScrData.size[5:]
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.size[i+5]  
                obj.addProperty("App::PropertyFloat", "L1",label).L1=L1
                obj.addProperty("App::PropertyFloat", "L2",label).L2=L2
                ParamHxgBlt.HxgBlt(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute() 
            elif key=='02':
                L1=float(self.lineEdit.text())#首下長さ
                L2=float(self.lineEdit_2.text())#ねじ部長さ
                label='Hexagon Socket head'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyString", "key",label).key=key
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=ScrData.sh_size
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.sh_size[i]  
                obj.addProperty("App::PropertyEnumeration", "st",label)
                obj.st=ScrData.bolt_st2
                i=self.comboBox_standard.currentIndex()
                obj.st=ScrData.bolt_st2[i]
                obj.addProperty("App::PropertyFloat", "L1",label).L1=L1
                obj.addProperty("App::PropertyFloat", "L2",label).L2=L2
                ParamShBlt.ShBlt(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute()    
            elif key=='03':
                L1=float(self.lineEdit_2.text())#ねじ部長さ
                label='All screw'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=ScrData.size[5:]
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.size[i+5]  
                obj.addProperty("App::PropertyFloat", "L1",label).L1=L1
                ParamAllScrw.AllScrw(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute()        
            elif key=='04':
                L1=float(self.lineEdit.text())
                L2=float(self.lineEdit_2.text())#ねじ部長さ
                label='Anchor bolt'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=ScrData.anch_size
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.anch_size[i]  
                obj.addProperty("App::PropertyEnumeration", "st",label)
                obj.st=ScrData.bolt_st4
                i=self.comboBox_standard.currentIndex()
                obj.st=ScrData.bolt_st4[i]
                obj.addProperty("App::PropertyFloat", "L1",label).L1=L1
                obj.addProperty("App::PropertyFloat", "L2",label).L2=L2
                ParamAnchBlt.AnchBlt(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute()      
            elif key=='05' or key=='06' or key=='13':
                try:
                    L1=float(self.lineEdit.text())
                except:
                    pass
                L2=float(self.lineEdit_2.text())
                if key=='05':
                    label=st
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                    if self.checkbox.isChecked():
                        obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                    else:
                        obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                    if st=='Pan_head' or st=='Flat_head' or st=='Round_flat_head':
                        obj.addProperty("App::PropertyEnumeration", "dia",label)
                        obj.dia=ScrData.size[2:11]
                        i=self.comboBox_dia.currentIndex()
                        obj.dia=ScrData.size[i+2]   
                        obj.addProperty("App::PropertyEnumeration", "st",label)
                        obj.st=ScrData.bolt_st5
                        i=self.comboBox_standard.currentIndex()
                        obj.st=ScrData.bolt_st5[i]
                    elif st=='Truss_screw' or st=='Binding_head':
                        obj.addProperty("App::PropertyEnumeration", "dia",label)
                        obj.dia=ScrData.size[3:10]
                        i=self.comboBox_dia.currentIndex()
                        obj.dia=ScrData.size[i+3]   
                        obj.addProperty("App::PropertyEnumeration", "st",label)
                        obj.st=ScrData.bolt_st5
                        i=self.comboBox_standard.currentIndex()
                        obj.st=ScrData.bolt_st5[i]
                    elif st=='Round_screw' or st=='Flat_screw':
                        obj.addProperty("App::PropertyEnumeration", "dia",label)
                        obj.dia=ScrData.size[:10]
                        i=self.comboBox_dia.currentIndex()
                        obj.dia=ScrData.size[i]   
                        obj.addProperty("App::PropertyEnumeration", "st",label)
                        obj.st=ScrData.bolt_st5
                        i=self.comboBox_standard.currentIndex()
                        obj.st=ScrData.bolt_st5[i]  
                    obj.addProperty("App::PropertyFloat",'L1',label).L1=L1
                    obj.addProperty("App::PropertyFloat",'L2',label).L2=L2
                    ParamSmlScrw.SmlScrw(obj)
                    obj.ViewObject.Proxy=0
                    #FreeCAD.ActiveDocument.recompute() 
                elif key=='06' or key=='13':
                    #label=st
                    if key=='13':
                        st='ThreadedHoll'
                        #label=st
                    label=st
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                    if self.checkbox.isChecked():
                        obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                    else:
                        obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                    obj.addProperty("App::PropertyEnumeration", "dia",label)
                    obj.dia=ScrData.size[2:14]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+2] 
                    obj.addProperty("App::PropertyEnumeration", "st",label)
                    obj.st=ScrData.bolt_st6
                    i=self.comboBox_standard.currentIndex()
                    obj.st=ScrData.bolt_st6[i]   
                    #if key=='13':
                    #    obj.addProperty("App::PropertyFloat",'L1',label).L1=L1

                    obj.addProperty("App::PropertyFloat",'L2',label).L2=L2
                    if key=='06':
                        ParamSetScrew.SetScrew(obj)
                    elif key=='13':
                        ParamThreadedHoll.ThreadedHoll(obj)
                    obj.ViewObject.Proxy=0
                    #FreeCAD.ActiveDocument.recompute() 
            elif key=='07':
                label=st
                L1=float(self.lineEdit.text())
                L2=float(self.lineEdit_2.text())
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=ScrData.size[9:]
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.size[i+9] 
                obj.addProperty("App::PropertyFloat",'L1',label).L1=L1
                obj.addProperty("App::PropertyFloat",'L2',label).L2=L2
                ParamEyeBlt.EyeBlt(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute() 
            elif key=='09':
                global t0
                label=st
                #print(st)
                

                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                #obj.addProperty("App::PropertyFloat", "t",label)

                if st=='Small circle':
                    obj.dia=ScrData.size[:16]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i] 
                    sa=ScrData.p_washer[dia]
                    t0=sa[2]
                elif st=='Polish circle' or st=='Spring_washer_general':
                    obj.dia=ScrData.size[3:16]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+3]  
                    sa=ScrData.p_washer[dia]
                    if st=='Polish chircle':
                        t0=sa[5]
                    elif st=='Spring_washer_general':
                        t0=sa[17]    
                elif st=='Common circle' or st=='Small corner' or st=='Large angle' or st=='Spring_washer_heavy':
                    obj.dia=ScrData.size[8:16]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+8] 
                    sa=ScrData.p_washer[dia]
                    if st=='Common circle':
                        t0=sa[8]
                    elif st=='Small corner':
                        t0=sa[11] 
                    elif st=='Large angle':
                        t0=sa[14]  
                    elif st=='Spring_washer_heavy':
                        t0=sa[20]         
                elif st=='Inclined_washer_5degrees' or st=='Inclined_washer_8degrees':
                    obj.dia=ScrData.size[10:]
                    i=self.comboBox_dia.currentIndex()
                    obj.dia=ScrData.size[i+10] 
                    sa=ScrData.inc_washer[dia]
                    if st=='Inclined_washer_5degrees':
                        t0=sa[3]
                    elif st=="Inclined_washer_8degrees":
                        t0=sa[7]
                    
                obj.addProperty("App::PropertyEnumeration", "st",label)
                obj.st=ScrData.bolt_st9
                i=self.comboBox_standard.currentIndex()
                obj.st=ScrData.bolt_st9[i]  

                obj.addProperty("App::PropertyFloat", "t0",label).t0=t0
                #obj.t=t
                #print(st,t)
                ParamWasher.Washer(obj)
                #print(obj.t)
                obj.ViewObject.Proxy=0

                #FreeCAD.ActiveDocument.recompute() 
                
            elif key=='11':
                label='U_bolt'
                L1=float(self.lineEdit.text())
                L2=float(self.lineEdit_2.text())
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)   
                obj.dia=ScrData.U_size
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.U_size[i] 

                obj.addProperty("App::PropertyEnumeration", "fdia",label)   
                obj.fdia=ScrData.flange_st
                i=self.comboBox_fdia.currentIndex()
                obj.fdia=ScrData.flange_st[i] 

                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False

                if self.checkboxf.isChecked():
                    obj.addProperty("App::PropertyBool",'flange',label).flange = True
                else:
                    obj.addProperty("App::PropertyBool",'flange',label).flange = False    
                obj.addProperty("App::PropertyFloat", "stem_length",label).stem_length=L1
                obj.addProperty("App::PropertyFloat", "thread_length",label).thread_length=L2    
                ParamUBlt.UBlt(obj)
                obj.ViewObject.Proxy=0
                #FreeCAD.ActiveDocument.recompute()     
            elif key=='12':
                label='U_band'
                L1=float(self.lineEdit.text())
                L2=float(self.lineEdit_2.text())
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

                obj.addProperty("App::PropertyEnumeration", "dia",label)   
                obj.dia=ScrData.U_size
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.U_size[i] 

                obj.addProperty("App::PropertyEnumeration", "fdia",label)   
                obj.fdia=ScrData.flange_st
                i=self.comboBox_fdia.currentIndex()
                obj.fdia=ScrData.flange_st[i] 

                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False

                if self.checkboxf.isChecked():
                    obj.addProperty("App::PropertyBool",'flange',label).flange = True
                else:
                    obj.addProperty("App::PropertyBool",'flange',label).flange = False    
                obj.addProperty("App::PropertyFloat", "stem_length",label).stem_length=L1
                obj.addProperty("App::PropertyFloat", "thread_length",label).thread_length=L2    
                ParamUBnd.UBlt(obj)
                obj.ViewObject.Proxy=0
                FreeCAD.ActiveDocument.recompute()  
        elif key=='10':
                #print(key)
                dia=self.comboBox_dia.currentText()
                sa=ScrData.brg_nut[dia]
                Bn=sa[7]
                t0=sa[11]
                L1=float(self.lineEdit.text())
                L2=float(self.lineEdit_2.text())
                label=st
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)   
                obj.dia=ScrData.brg_size
                i=self.comboBox_dia.currentIndex()
                obj.dia=ScrData.brg_size[i] 
                obj.addProperty("App::PropertyEnumeration", "st",label)
                obj.st=ScrData.brg_nut_st
                i=self.comboBox_standard.currentIndex()
                if i==0:
                    obj.addProperty("App::PropertyFloat", "Bn",label).Bn=Bn
                elif i==1:
                    obj.addProperty("App::PropertyFloat", "t0",label).t0=t0  

                obj.st=ScrData.brg_nut_st[i]  
                if self.checkbox.isChecked():
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
                else:
                    obj.addProperty("App::PropertyBool",'Thread',label).Thread = False
                obj.addProperty("App::PropertyFloat", "L1",label).L1=L1
                obj.addProperty("App::PropertyFloat", "L2",label).L2=L2
                
                ParamBrgNut.BrgNut(obj)
                obj.ViewObject.Proxy=0
                FreeCAD.ActiveDocument.recompute()   

        
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