# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtCore
from PySide import QtGui
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import FreeCADGui as Gui
from pivy import coin
from PySide2 import QtCore
from pln_data import plndata
from pln_data import ParamCircle
from pln_data import ParamSemiCircle
from pln_data import ParamQuadrant
from pln_data import ParamRing
from pln_data import ParamSemiRing
from pln_data import ParamOval
from pln_data import ParamOvalRing
from pln_data import ParamRectang
from pln_data import ParamLShape
from pln_data import ParamChannel
from pln_data import ParamTShape
from pln_data import ParamHShape
from pln_data import ParamFrame
from pln_data import ParamD_Cut
from pln_data import ParamD_Cut2
from pln_data import ParamRightTriangle
from pln_data import ParamTrapezoid
from pln_data import ParamTrapezoidR
from pln_data import ParamFanShaped
from pln_data import ParamFanShaped2
from pln_data import ParamBracket
from pln_data import ParamDharma
from pln_data import ParamBasePlate
from pln_data import ParamUShape
from pln_data import ParamChainCover
DEBUG = True # set to True to show debug messages
class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        return
        
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 500)
        Dialog.move(1000, 0)
        #shape
        self.shape = QtGui.QLabel('shapes',Dialog)
        self.shape.setGeometry(QtCore.QRect(50, 15, 50, 12))
        self.shape.setStyleSheet("color: black;")
        self.combo_shape = QtGui.QComboBox(Dialog)
        self.combo_shape.setGeometry(QtCore.QRect(105, 10, 159, 22))
        
        #D
        self.lbl_D = QtGui.QLabel('D[mm]',Dialog)
        self.lbl_D.setGeometry(QtCore.QRect(50, 65, 50, 12))
        self.lbl_D.setStyleSheet("color: black;")
        self.le_D = QtGui.QLineEdit(Dialog)
        self.le_D.setGeometry(QtCore.QRect(105, 65, 50, 20))
        self.le_D.setAlignment(QtCore.Qt.AlignCenter)

        #d
        self.lbl_d = QtGui.QLabel('d[mm]',Dialog)
        self.lbl_d.setGeometry(QtCore.QRect(170, 65, 50, 12))
        self.lbl_d.setStyleSheet("color: black;")
        self.le_d = QtGui.QLineEdit(Dialog)
        self.le_d.setGeometry(QtCore.QRect(220, 65, 50, 20))
        self.le_d.setAlignment(QtCore.Qt.AlignCenter)

        #B
        self.lbl_B = QtGui.QLabel('B[mm]',Dialog)
        self.lbl_B.setGeometry(QtCore.QRect(50, 95, 50, 12))
        self.lbl_B.setStyleSheet("color: black;")
        self.le_B = QtGui.QLineEdit(Dialog)
        self.le_B.setGeometry(QtCore.QRect(105, 95, 50, 20))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)       

        #H
        self.lbl_H = QtGui.QLabel('H[mm]',Dialog)
        self.lbl_H.setGeometry(QtCore.QRect(170, 95, 50, 12))
        self.lbl_H.setStyleSheet("color: black;")
        self.le_H = QtGui.QLineEdit(Dialog)
        self.le_H.setGeometry(QtCore.QRect(220, 95, 50, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)  

        #b1
        self.lbl_b1 = QtGui.QLabel('b1[mm]',Dialog)
        self.lbl_b1.setGeometry(QtCore.QRect(50, 125, 50, 12))
        self.lbl_b1.setStyleSheet("color: black;")
        self.le_b1 = QtGui.QLineEdit(Dialog)
        self.le_b1.setGeometry(QtCore.QRect(105, 125, 50, 20))
        self.le_b1.setAlignment(QtCore.Qt.AlignCenter) 

        #h1
        self.lbl_h1 = QtGui.QLabel('h1[mm]',Dialog)
        self.lbl_h1.setGeometry(QtCore.QRect(170, 125, 50, 12))
        self.lbl_h1.setStyleSheet("color: black;")
        self.le_h1 = QtGui.QLineEdit(Dialog)
        self.le_h1.setGeometry(QtCore.QRect(220, 125, 50, 20))
        self.le_h1.setAlignment(QtCore.Qt.AlignCenter)  

        #b2
        self.lbl_b2 = QtGui.QLabel('b2[mm]',Dialog)
        self.lbl_b2.setGeometry(QtCore.QRect(50, 155, 50, 12))
        self.lbl_b2.setStyleSheet("color: black;")
        self.le_b2 = QtGui.QLineEdit(Dialog)
        self.le_b2.setGeometry(QtCore.QRect(105, 155, 50, 20))
        self.le_b2.setAlignment(QtCore.Qt.AlignCenter)   

        #h2
        self.lbl_h2 = QtGui.QLabel('h2[mm]',Dialog)
        self.lbl_h2.setGeometry(QtCore.QRect(170, 155, 50, 12))
        self.lbl_h2.setStyleSheet("color: black;")
        self.le_h2 = QtGui.QLineEdit(Dialog)
        self.le_h2.setGeometry(QtCore.QRect(220, 155, 50, 20))
        self.le_h2.setAlignment(QtCore.Qt.AlignCenter)  

        #b3
        self.lbl_b3 = QtGui.QLabel('b3[mm]',Dialog)
        self.lbl_b3.setGeometry(QtCore.QRect(50, 185, 50, 12))
        self.lbl_b3.setStyleSheet("color: black;")
        self.le_b3 = QtGui.QLineEdit(Dialog)
        self.le_b3.setGeometry(QtCore.QRect(105, 185, 50, 20))
        self.le_b3.setAlignment(QtCore.Qt.AlignCenter)   

        #h3
        self.lbl_h3 = QtGui.QLabel('h3[mm]',Dialog)
        self.lbl_h3.setGeometry(QtCore.QRect(170, 185, 50, 12))
        self.lbl_h3.setStyleSheet("color: black;")
        self.le_h3 = QtGui.QLineEdit(Dialog)
        self.le_h3.setGeometry(QtCore.QRect(220, 185, 50, 20))
        self.le_h3.setAlignment(QtCore.Qt.AlignCenter)   

        #st
        self.lbl_st = QtGui.QLabel('θ[deg]',Dialog)
        self.lbl_st.setGeometry(QtCore.QRect(50, 215, 70, 12))
        self.lbl_st.setStyleSheet("color: black;")
        self.le_st = QtGui.QLineEdit(Dialog)
        self.le_st.setGeometry(QtCore.QRect(105, 215, 50, 20))
        self.le_st.setAlignment(QtCore.Qt.AlignCenter)     

        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 245, 90, 23))
        self.pushButton.setObjectName("pushButton")  

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(150, 245, 90, 23))
        self.pushButton_m.setObjectName("pushButton")  

        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(90, 283, 100, 12))
        self.lbl_gr.setStyleSheet("color: black;")
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(170, 280, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        
        self.le_D.setText('50')
        self.le_d.setText('40')
        self.le_B.setText('50')
        self.le_H.setText('50')
        self.le_b1.setText('10')
        
        self.le_b2.setText('20')
        self.le_b3.setText('10')
        self.le_h1.setText('10')
        self.le_h2.setText('10')
        self.le_h3.setText('10')
        self.le_st.setText('90')

        self.le_gr.setText('7.85')

        #img
        self.img = QtGui.QLabel(Dialog)
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 305, 250, 140))
        self.img.setText("")
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        #作業面
        self.sface = QtGui.QLabel('Work surface',Dialog)
        self.sface.setGeometry(QtCore.QRect(90, 458, 100, 15))
        self.sface.setStyleSheet("color: black;")
        self.combo_sface = QtGui.QComboBox(Dialog)
        self.combo_sface.setGeometry(QtCore.QRect(170, 455, 50, 22))
        self.combo_sface.addItems(plndata.sface)

        self.retranslateUi(Dialog)
        self.combo_shape.addItems(plndata.shape_type)
        self.combo_shape.setCurrentIndex(1)
        self.combo_shape.currentIndexChanged[int].connect(self.on_shape)
        self.combo_shape.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def massCulc(self):
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]

        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.g0=g0
        except:
            obj.mass=g
            obj.g0=g0 
            
    def on_shape(self):
        global key
        key=self.combo_shape.currentIndex()
        #print(key)            
        if key==0:
            pic='0_circle.png'
            print(pic) 
        elif key==1:
            pic='1_semi_circle.png'  
        elif key==2:
            pic='2_ring.png'  
        elif key==3:
            pic='3_semi_ring.png'  
        elif key==4:
            pic='4_oval.png'  
        elif key==5:
            pic='5_oval_ring.png'  
        elif key==6:
            pic='6_rectang.png'  
        elif key==7:
            pic='7_L.png'  
        elif key==8:
            pic='8_channel.png' 
            self.le_b2.setText('50')
        elif key==9:
            pic='9_T.png' 
        elif key==10:
            pic='10_H.png'  
          
        elif key==11:
            pic='11_frame.png' 
            self.le_b2.setText('10')   
        elif key==12:
            pic='12_D_Cut.png' 
        elif key==13:
            pic='13_right_triangle.png'  
        elif key==14:
            pic='14_trapezoid.png' 
            self.le_b1.setText('30')      
        elif key==15:
            pic='15_trapezoid_r.png' 
            self.le_b1.setText('30')                           
        elif key==16:
            pic='16_fan_shaped.png' 
        elif key==17:
            pic='17_fan_shaped2.png'   
        elif key==18:
            pic='18_bracket.png' 
        elif key==19:
            pic='19_dharma.png' 
        elif key==20:
            pic='20_base_p.png'  
            self.le_b1.setText('30') 
            self.le_b2.setText('20') 
            self.le_h1.setText('30')  
            self.le_D.setText('20')    
            self.le_B.setText('100')  
            self.le_H.setText('100')  
        elif key==21:
            pic='21_quadrant.png'      
        elif key==22:
            pic='22_D_Cut2.png'  
            self.le_B.setText('1000')  
            self.le_H.setText('120') 
        elif key==23:
            pic='23_UShape.png'  
            self.le_D.setText('480')  
            self.le_d.setText('468')  
            self.le_H.setText('250')  
        elif key==24:
            pic='24_ChainCover.png'  
            self.le_D.setText('600')  
            self.le_d.setText('300')    
            self.le_B.setText('600')
            self.le_h1.setText('200')
            self.le_h2.setText('100')


        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "pln_data",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))  
         
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "planar shapes ", None))

    def create(self):
        global D
        global D0
        global d
        global d0
        global B
        global B0
        global H
        global H0
        global b1
        global b2
        global b3
        global h1
        global h2
        global h3
        global st
        global n

        D=float(self.le_D.text())
        d=float(self.le_d.text())
        B=float(self.le_B.text())
        H=float(self.le_H.text())
        b1=float(self.le_b1.text())
        b2=float(self.le_b2.text())
        b3=float(self.le_b3.text())
        h1=float(self.le_h1.text())
        h2=float(self.le_h2.text())
        h3=float(self.le_h3.text())
        st=float(self.le_st.text())

        if key==0 or key==1 or key==21:
            if key==0:
                label='Circle'
            elif key==1:
                label='SemiCircle'
            elif key==21:
                label='Quadrant'    
            
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==2 or key==3:
            if key==2:
                label='Ring'
            else:
                label='SemiRing'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "d",label).d=d

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==4:
            label='Oval'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "B",label).B=B

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==5:
            label='OvalRing'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "d",label).d=d
            obj.addProperty("App::PropertyFloat", "B",label).B=B

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==6:
            label='Rectang'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==7:
            label='LShape'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==8:
            label='Channel'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "b2",label).b2=b2
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==9:
            label='TShape'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==10:
            label='HShape'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "b2",label).b2=b2
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==11:
            label='Frame'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "b2",label).b2=b2
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==12:
            label='D_Cut'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==13:
            label='RightTriangle'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==14:
            label='Trapezoid'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==15:
            label='TrapezoidR'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]
        
        elif key==16:
            label='FanShaped'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "st",label).st=st

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==17:
            label='FanShaped2'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "d",label).d=d
            obj.addProperty("App::PropertyFloat", "st",label).st=st  

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==18:
            label='Bracket'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "b2",label).b2=b2
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]
        
        elif key==19:
            label='Dharma'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "d",label).d=d
            obj.addProperty("App::PropertyFloat", "B",label).B=B

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==20:
            label='BasePlate'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "b1",label).b1=b1
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==21:
            label='Quadrant'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]

        elif key==22:
            label='D_Cut2'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "H",label).H=H
            obj.addProperty("App::PropertyFloat", "B",label).B=B 

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]
        elif key==23:
            label='UShape'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "H",label).H=H

            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]    
        elif key==24:
            label='ChainCover'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",label).D=D
            obj.addProperty("App::PropertyFloat", "d",label).d=d
            obj.addProperty("App::PropertyFloat", "B",label).B=B
            obj.addProperty("App::PropertyFloat", "h1",label).h1=h1
            obj.addProperty("App::PropertyFloat", "h2",label).h2=h2
           
            obj.addProperty("App::PropertyEnumeration", "sface",label)
            obj.sface=plndata.sface              
            i=self.combo_sface.currentIndex()
            obj.sface=plndata.sface[i]      
       
        if key==0:
            ParamCircle.Circle(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==1:
            ParamSemiCircle.SemiCircle(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==2:
            ParamRing.Ring(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==3:
            ParamSemiRing.SemiRing(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==4:
            ParamOval.Oval(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==5:
            ParamOvalRing.OvalRing(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==6: 
            ParamRectang.Rectang(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==7:
            ParamLShape.LShape(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==8:
            ParamChannel.Channel(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==9:
            ParamTShape.TShape(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==10:
            ParamHShape.HShape(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==11:
            ParamFrame.Frame(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==12:
            ParamD_Cut.D_Cut(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==13:
            ParamRightTriangle.RightTriangle(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==14:
            ParamTrapezoid.Trapezoid(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==15:
            ParamTrapezoidR.TrapezoidR(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==16:
            ParamFanShaped.FanShaped(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==17:
            ParamFanShaped2.FanShaped2(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==18:
            ParamBracket.Bracket(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==19:
            ParamDharma.Dharma(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==20:
            ParamBasePlate.BasePlate(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()  
        elif key==21:
            ParamQuadrant.Quadrant(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()     
        elif key==22:
            ParamD_Cut2.D_Cut2(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
        elif key==23:
            ParamUShape.UShape(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()      
        elif key==24:
            ParamChainCover.ChainCover(obj)
            obj.ViewObject.Proxy=0
            

        doc = App.ActiveDocument
        new_obj = doc.ActiveObject 

        #'Assembly' オブジェクトを探して追加する
        target_folder = doc.getObject('Assembly')
        if target_folder:
            target_folder.addObject(new_obj)
            doc.recompute()

        view = Gui.ActiveDocument.ActiveView
        obj.ViewObject.Visibility = True
        sep = coin.SoSeparator()
        trans = coin.SoTranslation()
        sep.addChild(trans)
        view.getSceneGraph().addChild(sep)
        callbacks = {}
        
        # -----------------------------
        def move_cb(info):
            pos = info["Position"]
            p = view.getPoint(pos)
            trans.translation.setValue(p)
            obj.Placement.Base = p
        
        # -----------------------------
        def click_cb(info):
            if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                # ★ 直接 finish() を呼ばない
                QtCore.QTimer.singleShot(0, finish)
        
        # -----------------------------
        def key_cb(info):
            if info.get("Key") == "ESCAPE":
                QtCore.QTimer.singleShot(0, cancel)
        
        # -----------------------------
        def finish():
            try:
                view.removeEventCallback("SoLocation2Event", callbacks["move"])
                view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                view.removeEventCallback("SoKeyboardEvent", callbacks["key"])
            except:
                pass
        
            obj.ViewObject.Visibility = True
        
            try:
                view.getSceneGraph().removeChild(sep)
            except:
                pass
        
            App.ActiveDocument.recompute()
        
        # -----------------------------
        def cancel():
            finish()
            try:
                App.ActiveDocument.removeObject(obj.Name)
            except:
                pass
        
        # -----------------------------
        callbacks["move"]  = view.addEventCallback("SoLocation2Event", move_cb)
        callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)
        callbacks["key"]   = view.addEventCallback("SoKeyboardEvent", key_cb)         
        
class Main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
       