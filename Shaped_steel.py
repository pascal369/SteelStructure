# -*- coding: utf-8 -*-
import os
import sys
import Import
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCADGui as Gui
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD, FreeCADGui
import FreeCAD as App

from shpst_data import ShpstData
from shpst_data import ShpstData
from shpst_data import ParamAngle
from shpst_data import ParamChannel
from shpst_data import ParamHShape
from shpst_data import ParamIShape
from shpst_data import ParamCtShape
from shpst_data import ParamPipeShape
from shpst_data import ParamFlatShape
from shpst_data import ParamLWAngle
from shpst_data import ParamLWChannel
from shpst_data import ParamRipChannel
from shpst_data import ParamSquarePipe

#JIS G 3192
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 320)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel('Shaped Steel',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 10, 70, 12))
        self.label_type.setObjectName("label_type")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(100, 10, 160, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        #規格
        self.label_st = QtGui.QLabel("Standard",Dialog)
        self.label_st.setGeometry(QtCore.QRect(10, 35, 50, 12))
        self.label_st.setObjectName("label_st")
        self.comboBox_st = QtGui.QComboBox(Dialog)
        self.comboBox_st.setGeometry(QtCore.QRect(100, 35, 160, 22))
        self.comboBox_st.setObjectName("comboBox_st")
        #サイズ
        self.label_size = QtGui.QLabel("Size",Dialog)
        self.label_size.setGeometry(QtCore.QRect(10, 60, 50, 12))
        self.label_size.setObjectName("label_size")
        self.comboBox_size = QtGui.QComboBox(Dialog)
        self.comboBox_size.setGeometry(QtCore.QRect(100, 60, 160, 22))
        self.comboBox_size.setObjectName("comboBox_size")
        self.comboBox_size.Editable=True
        #実行Create
        self.pushButton = QtGui.QPushButton("Create",Dialog)
        self.pushButton.setGeometry(QtCore.QRect(167, 160, 80, 22))
        self.pushButton.setObjectName("pushButton")
        #更新upDate
        self.pushButton2 = QtGui.QPushButton("upDate",Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(167, 185, 80, 22))
        self.pushButton2.setObjectName("pushButton")
        #import
        self.pushButton3 = QtGui.QPushButton("import",Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(167, 210, 80, 22))


        #比重
        self.mtrl = QtGui.QLabel('Specific gravity of material',Dialog)
        self.mtrl.setGeometry(QtCore.QRect(30, 268, 150, 12))
        self.le_mtrl = QtGui.QLineEdit(Dialog)
        self.le_mtrl.setGeometry(QtCore.QRect(180, 265, 50, 20))
        self.le_mtrl.setAlignment(QtCore.Qt.AlignCenter)

        #長さ
        self.label_l = QtGui.QLabel("Length[mm]",Dialog)
        self.label_l.setGeometry(QtCore.QRect(10, 85, 81, 20))
 
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(100, 85, 60, 32)
        self.spinBoxL.setMinimum(1)  # 最小値
        self.spinBoxL.setMaximum(5500)  # 最大値
        self.spinBoxL.setValue(5500)  # 
        self.spinBoxL.setSingleStep(100) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)
        #lengthStep
        self.label_step = QtGui.QLabel('step',Dialog)
        self.label_step.setGeometry(QtCore.QRect(180, 85, 50, 16))
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(220, 85, 40, 16))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        
        #checkboxソリッド
        self.checkbox = QtGui.QCheckBox("Solid",Dialog)
        self.checkbox.setGeometry(QtCore.QRect(30, 130, 61, 23))
        self.checkbox.setObjectName("checkbox")
        self.checkbox.setChecked(True)
        
        #img
        self.label_img = QtGui.QLabel(Dialog)
        self.label_img.setGeometry(QtCore.QRect(30, 155, 100, 100))
        self.label_img.setText("")
        
        
        self.retranslateUi(Dialog)
        self.comboBox_type.addItems(ShpstData.type)
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)

        self.comboBox_type.setCurrentIndex(0)
        self.comboBox_st.setCurrentIndex(1)
        self.comboBox_st.currentIndexChanged[int].connect(self.onStandard)
        self.comboBox_st.setCurrentIndex(0)

        self.spinBoxL.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "JIS G 3192 Shaped Steel", None))
        
    def upDate(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                size=self.comboBox_size.currentText()
                myShape.size=size
                L=self.spinBoxL.value()
                myShape.L=str(L)
            except:
                myShape=None 
        App.ActiveDocument.recompute()         

    def read_data(self):#管長
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                L=int(myShape.L)
                size=myShape.size
                self.spinBoxL.setValue(int(L))
                self.comboBox_size.setCurrentText(size)
                self.comboBox_type.setCurrentText(myShape.type)
            except:
                myShape=None        
        App.ActiveDocument.recompute()   
        
    def spinMove(self):
        step=self.le_step.text()
        self.spinBoxL.setSingleStep(int(step)) 
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                myShape=obj
                L=self.spinBoxL.value()
                myShape.L=str(L)
            except:
                myShape=None  
        App.ActiveDocument.recompute()         

    def onType(self):
        global ta
        
        global key
        
        key = self.comboBox_type.currentText()[:2]
        if key=='00':
            ta=ShpstData.Angle_st
        elif key=='01':
            ta=ShpstData.Channel_st
        elif key=='02':
            ta=ShpstData.H_st
        elif key=='03':
            ta=ShpstData.I_st
        elif key=='04':
            ta=ShpstData.CT_st
        elif key=='05':
            ta=ShpstData.Pipe_st
        elif key=='06':
            ta=ShpstData.Flat_Bar_st
        elif key=='07':
            ta=ShpstData.LW_angle_st
        elif key=='08':
            ta=ShpstData.LW_channel_st
        elif key=='09':
            ta=ShpstData.Rip_channel_st
        elif key=='10':
            ta=ShpstData.Square_pipe_st

        self.comboBox_st.clear()
        self.comboBox_st.addItems(ta)

    def onStandard(self):
        global size
        global pic
        key = self.comboBox_type.currentText()[:2]
        
        st=self.comboBox_st.currentText()
        #print(st)
        if key=='00':#Angle
            
            pic='angle'
            if st=='SS_Equal':
                size=ShpstData.angle_ss_size
            elif st=='SS_Unequal':
                size=ShpstData.angle_ssun_size
            elif st=='SUS_Equal':
                size=ShpstData.angle_sus_size

        elif key=='01':
            pic='channel'
            if st=='SS':
                size=ShpstData.channel_ss_size
            elif st=='SUS':
                size=ShpstData.channel_sus_size
        elif key=='02':
            pic='h1_shape'
            if st=='SS_Wide':
                size=ShpstData.H_ss_w_size
                pic='h1_shape'
            elif st=='SS_Medium':
                pic='h2_shape'
                size=ShpstData.H_ss_m_size
            elif st=='SS_Thin':
                pic='h3_shape'
                size=ShpstData.H_ss_t_size
            elif st=='SUS':
                pic='h3_shape'
                size=ShpstData.H_sus_size
        elif key=='03':
            pic='i_shape'
            if st=='SS':
                size=ShpstData.I_ss_size
        elif key=='04':
            pic='ct_shape'
            if st=='SS':
                size=ShpstData.CT_ss_size
        elif key=='05':
            pic='pipe'
            if st=='STK':
                size=ShpstData.STK_ss_size
            elif st=='SUS_Sch20S':
                size=ShpstData.tube_d
            elif st=='SUS_Sch40':
                size=ShpstData.tube_d
            elif st=='SGP':
                size=ShpstData.tube_d    
        elif key=='06':
            pic='flat_bar'
            if st=='SS':
                size=ShpstData.Flat_bar_ss_size
            elif st=='SUS':
                size=ShpstData.Flat_bar_sus_size
        elif key=='07':
            pic='lw_angle'
            if st=='SS':
                size=ShpstData.LW_angle_ss_size
            elif st=='SUS':
                size=ShpstData.LW_angle_sus_size
        elif key=='08':
            pic='lw_channel'
            if st=='SS':
                size=ShpstData.LW_channel_ss_size
            elif st=='SUS':
                size=ShpstData.LW_channel_sus_size
        elif key=='09':
            pic='rip_channel'
            if st=='SS':
                size=ShpstData.Rip_channel_ss_size
            elif st=='SUS':
                size=ShpstData.Rip_channel_sus_size
        elif key=='10':
            pic='square_pipe'
            if st=='SS':
                size=ShpstData.Square_pipe_ss_size
            elif st=='SUS':
                size=ShpstData.Square_pipe_sus_size

        pic0='img_' + pic + '.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "shpst_data",pic0)
        self.label_img.setPixmap(QtGui.QPixmap(joined_path))
        self.comboBox_size.clear()
        self.comboBox_size.addItems(size)
        self.le_mtrl.setText('7.85')

    def create(self):
        key = self.comboBox_type.currentText()[:2]
        L=self.spinBoxL.value()
        g0=float(self.le_mtrl.text())
        
        if key=='00':#Angle
            label='AngleSteel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()
            
            try:
                if st=='SS_Equal' or st==['SS_Equal']:
                    sa=ShpstData.angle_ss_equal[dia]
                    JPN='等辺山形鋼'
                elif st=='SS_Unequal':
                    sa=ShpstData.angle_ss_unequal[dia]
                    JPN='不等辺山形鋼'
                elif st=='SUS_Equal':
                    JPN='ステンレス等辺山形鋼'
                    sa=ShpstData.angle_sus_equal[dia]
            except:
                pass
            A=sa[0]
            B=sa[1]
            t=sa[2]
            
            obj.addProperty("App::PropertyFloat", "A",'Dimension').A=A
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt
 
            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  
            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='L'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass    

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
            
            ParamAngle.Angle(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='01':#Channel
            label='ChannelSteel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()
            b='C'
            if st=='SS':
                sa=ShpstData.channel_ss[dia]
                JPN='溝形鋼'
            elif st=='SUS':
                PN='ステンレス溝形鋼'
                sa=ShpstData.channel_sus[dia]
            H=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]

            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t1",'Dimension').t1=t1
            obj.addProperty("App::PropertyFloat", "t2",'Dimension').t2=t2

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='C'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   

            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
            ParamChannel.Channel(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='02':#H
            label='HShapeSteel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='H'+st
            if st=='SS_Wide':
                sa=ShpstData.H_ss_w[dia]
                JPN='広幅H形鋼'
            elif st=='SS_Medium':
                sa=ShpstData.H_ss_m[dia]
                JPN='中幅H形鋼'
            elif st=='SS_Thin':
                sa=ShpstData.H_ss_t[dia]
                JPN='細幅H形鋼'
            elif st=='SUS':
                sa=ShpstData.H_sus[dia]
                JPN='ステンレスH形鋼'
            H=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]

            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t1",'Dimension').t1=t1
            obj.addProperty("App::PropertyFloat", "t2",'Dimension').t2=t2

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt
            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='H'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   


            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
            ParamHShape.HShape(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='03':#I
            label='IShapSteel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='I'
            if st=='SS':
                sa=ShpstData.I_ss[dia]
                JPN='ステンレスH形鋼'
            H=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]

            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t1",'Dimension').t1=t1
            obj.addProperty("App::PropertyFloat", "t2",'Dimension').t2=t2

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='I'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass  

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 

            ParamIShape.IShape(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='04':#CT
            label='CTShapeSteel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='CT'
            if st=='SS':
                sa=ShpstData.CT_ss[dia]
                JPN='CT形鋼'
            A=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]

            obj.addProperty("App::PropertyFloat", "A",'Dimension').A=A
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t1",'Dimension').t1=t1
            obj.addProperty("App::PropertyFloat", "t2",'Dimension').t2=t2

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='CT'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
            
            ParamCtShape.CtShape(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='05':#Pipe
            label='Pipe'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='Pipe'#Pipe
            if st=='STK':
                sa=ShpstData.STK_ss[dia]
                JPN='一般構造用炭素鋼鋼管'
            elif st=='SUS_Sch20S':
                sa=ShpstData.tubes[dia]
                JPN='ステンレス鋼管'
            elif st=='SUS_Sch40':
                sa=ShpstData.tubes[dia]
                JPN='ステンレス鋼管'
            elif st=='SGP':
                sa=ShpstData.tubes[dia]  
                JPN='配管用鋼管'  
            D=sa[0]
            t=sa[1]

            obj.addProperty("App::PropertyFloat", "D",'Dimension').D=D
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='Φ'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 

            ParamPipeShape.PipeShape(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='06':#FlatBar
            label='FlatBar'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()
            JPN='平鋼'
            b='FB'
            if st=='SS':
                sa=ShpstData.flat_ss[dia]
                JPN='平鋼'
            elif st=='SUS':
                sa=ShpstData.flat_sus[dia]
                JPN='ステンレス平鋼'
            B=sa[1]
            t=sa[0]

            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='FB'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
           
            ParamFlatShape.FlatShape(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='07':#LightWeightAngle
            label='LightWeightAngle'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='L'
            if st=='SS':
                sa=ShpstData.LW_angle_ss[dia]
                JPN='軽量山形鋼'
            elif st=='SUS':
                sa=ShpstData.LW_angle_sus[dia]
                JPN='ステンレス軽量山形鋼'
            A=sa[0]
            B=sa[1]
            t=sa[2]

            obj.addProperty("App::PropertyFloat", "A",'Dimension').A=A
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='L'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 
            
            ParamLWAngle.LWAngle(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 
        elif key=='08':#LightWeightChannel
            label='LightWeightChannel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()

            b='C'
            if st=='SS':
                sa=ShpstData.LW_channel_ss[dia]
                JPN='軽量溝形鋼'
            elif st=='SUS':
                sa=ShpstData.LW_channel_sus[dia]
                JPN='ステンレス軽量溝形鋼'
            H=sa[0]
            B=sa[1]
            t=sa[2]

            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='C'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 

            ParamLWChannel.LWChannel(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='09':#RipChannel
            label='RipChannel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()
            b='C'
            if st=='SS':
                sa=ShpstData.Rip_channel_ss[dia]
                JPN='リップ溝形鋼'
            elif st=='SUS':
                sa=ShpstData.Rip_channel_sus[dia]
                JPN='ステンレスリップ溝形鋼'

            H=sa[0]
            A=sa[1]
            C=sa[2]
            t=sa[3]

            obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            obj.addProperty("App::PropertyFloat", "A",'Dimension').A=A
            obj.addProperty("App::PropertyFloat", "C",'Dimension').C=C
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt

            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='C'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 

            ParamRipChannel.RipChannel(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        elif key=='10':#SquarePipe
            label='SquarePipe'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyString", "L",'Dimension').L=str(L)
            dia=self.comboBox_size.currentText()
            st=self.comboBox_st.currentText()
            b='Square_Pipe'
            if st=='SS':
                sa=ShpstData.square_pipe_ss[dia]
                JPN='角形鋼管'
            elif st=='SUS':
                sa=ShpstData.square_pipe_sus[dia]
                JPN='ステンレス角形鋼管'
            A=sa[0]
            B=sa[1]
            t=sa[2]

            obj.addProperty("App::PropertyFloat", "A",'Dimension').A=A
            obj.addProperty("App::PropertyFloat", "B",'Dimension').B=B
            obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t

            tt=self.comboBox_type.currentText()
            obj.addProperty("App::PropertyString", "type",label).type=tt
            obj.addProperty("App::PropertyEnumeration", "size",label)
            obj.size=size
            i=self.comboBox_size.currentIndex()
            obj.size=size[i]
            st=self.comboBox_st.currentText()
            obj.addProperty("App::PropertyString", "standard",label).standard=st
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  

            try:        
                obj.addProperty("App::PropertyString", "Standard",'Standard')
                Standard='□'+obj.size+'  L='+obj.L
                obj.Standard=Standard
            except:
                pass   
            
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = True 
            else:    
                obj.addProperty("App::PropertyBool", "Solid",label).Solid = False 

            ParamSquarePipe.SquarePipe(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

        
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

    

    
    
    







