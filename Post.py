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

Ptype=['Pst_H','Pst_L','Pst_C','Pst_SQ','Pst_Pipe',]
H_st=['SS_Wide',]
Angle_st=['SS_Equal','SUS_Equal',]
Channel_st=['SS','SUS',]
Square_pipe_st=['SS','SUS',]
Pipe_st=['STK',]
H_ss_w_size=[
'100x100x6/8','125x125x6.5/9','150x150x7/10','175x175x7.5/11','200x200x8/12','250x250x9/14',
'300x300x10/15','300x305x15/15','350x350x12/19','400x400x13/21',
]
H_ss_m_size=[
'148x100x6/9','194x150x6/9','244x175x7/11','294x200x8/12','340x250x9/14','390x300x10/16',
'440x300x11/18','482x300x11/15','488x300x11/18','582x300x12/17','588x300x12/20','692x300x13/20',
'700x300x13/24','800x300x14/26','900x300x16/28',
]
H_ss_t_size=[
'100x50x5/7','125x60x6/8','150x75x5/7','175x90x5/8','198x99x4.5/7','200x100x5.5/8','248x124x5/8',
'250x125x6/9','298x149x5.5/8','300x150x6.5/9','346x174x6/9','350x175x7/11','396x199x7/11',
'400x200x8/13','446x199x8/12','450x200x9/14','496x199x9/14','500x200x10/16','546x199x9/14',
'550x200x10/16','596x199x10/15','600x200x11/17'
]
H_sus_size=[
'100x100x6/8','125x125x6.5/8','148x100x6/8','150x150x7/8','200x100x5.5/8','200x200x8/12','250x250x9/14',
]
angle_ss_size=[
'20x20x3','25x25x3','30x30x3','30x30x5','40x40x3','40x40x5','50x50x4','50x50x6','65x65x6',
'65x65x8','75x75x6','75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7',
'100x100x10','100x100x13','130x130x9','130x130x12','130x130x15','150x150x12','130x130x15',
'150x150x12','150x150x15','150x150x19','200x200x15','200x200x20','200x200x25'
]
angle_ssun_size=[
'90x75x9','100x75x7','100x75x10','125x75x7','125x75x10','125x75x13','125x90x10','125x90x13','150x90x9',
'150x90x12','150x100x9','150x100x12','150x100x15',
]
angle_sus_size=[
'20x20x3','25x25x3','30x30x3','40x40x3','35x35x4','40x40x4','50x50x4','40x40x5','45x45x5',
'50x50x5','30x30x6','35x35x6','40x40x6','50x50x6','60x60x6','65x65x6','75x75x6','100x100x6',
'70x70x7','65x65x8','80x80x8','100x100x8','50x50x9','65x65x9','75x75x9','90x90x9','125x125x9',
'75x75x12','100x100x10','100x100x12','125x125x12','90x90x13','100x100x13','130x130x12','125x125x15',
'150x150x15'
]
channel_ss_size=[
'75x40x5','100x50x5','125x65x6','150x75x6','150x75x9','180x75x7','200x80x7.5','200x90x8',
'250x90x9','250x90x11','300x90x9','300x90x10','300x90x12','380x100x10.5','380x100x13/16.5',
'380x100x13/20',
]

channel_sus_size=[
'40x20x3','50x25x3','100x50x4','80x40x5','100x50x5','100x50x6','120x60x6','130x65x6',
'150x75x6','150x75x9','200x100x10','220x65x6','230x65x6','250x75x6','250x75x9',
'250x90x9','300x90x9','300x100x9','250x100x10','300x90x10','300x100x10',
]
Square_pipe_ss_size=[
'9x9x1.0','10x10x1.0','11.5x11.5x1.6','15x15x0.8','15x15x1.2','15x15x2.0','20x20x1.6','20x20x2.3','21x21x2.3','25x25x2.0',
'30x30x2.3','30x30x3.2','30x30x4.5','31x31x2.3','31x31x3.2','31x31x4.5','32x32x2.3','35x35x3.2','35x35x3.5','35x35x4.5',
'38x38x2.3','39.4x39.4x3.5','39.6x39.6x4.5','40x40x1.6','40x40x2.3',
'50x50x1.6','50x50x2.3','50x50x3.2','60x60x1.6','60x60x2.3','60x60x3.2','75x75x2.3','75x75x3.2','100x100x2.3','100x100x3.2',
'100x100x4,100','100x100x4.5','125x125x3.2','125x125x4.5','125x125x5','125x125x6','150x150x4.5','150x150x5','150x150x6',
'200x200x6','200x200x8','200x200x9','200x200x12','25x250x5','250x250x6','250x250x8','250x250x9','250x250x12','300x300x4.5',
'300x300x6','300x300x9','300x300x12','350x350x9','350x350x12',
]

Square_pipe_sus_size=[
'30x30x3','40x40x3','40x40x4','40x40x5','50x50x3','50x50x4','50x50x5','60x60x3','60x60x4','60x60x5','75x75x3','75x75x4',
'75x75x5','75x75x6','80x80x3','80x80x4','80x80x5','80x80x6','90x90x3','90x90x4','90x90x5','90x90x6','100x100x3','100x100x4',
'100x100x4','100x100x5','100x100x6','100x100x9','100x100x12','120x120x3','120x120x4','120x120x5','120x120x6','120x120x9',
'125x125x3','125x125x4','125x125x5','125x125x6','125x125x9','125x125x12','150x150x3','150x150x4','150x150x5','150x150x6',
'150x150x9','150x150x12','175x175x3','175x175x4','175x175x5','175x175x6','175x175x9','175x175x12','200x200x3','200x200x4',
'200x200x5','200x200x6','200x200x8','200x200x9','200x200x12','250x250x4','250x250x5','250x250x6','250x250x9','250x250x12',
'300x300x4','300x300x6','300x300x9','300x300x12','350x350x9','350x350x12','400x400x6','400x400x9','400x400x12',
]
STK_ss_size=[
'21.7x2.0','27.2x2.0','27.2x2.3','34.0x2.3','42.7x2.3','42.7x2.8','48.6x2.3','48.6x2.8','48.6x3.2','60.5x2.3',
'60.5x3.2','60.5x4.0','7635x2.8','76.3x3.2','76.3x4.0','89.1x2.8','89.1x3.2','89.1x4.0','101.6x3.2','101.6x4.0',
'101.6x5.0','114.3x3.2','114.3x3.6','114.3x4.5','114.3x5.6','139.8x3.6','139.8x4.0','139.8x4.5','139.8x6.0',
'165.2x4.5','165.2x5.0','165.2x6.0','165.2x7.0','190.7x4.5','190.7x5.0','190.7x6.0','190.7x7.0','216.3x4.5',
'216.3x6.0','216.3x7.0','216.3x8.0',
]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 410)
        Dialog.move(1500, 0)
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
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
        self.pushButton.setGeometry(QtCore.QRect(167, 107, 50, 22))
        self.pushButton.setObjectName("pushButton")
        #更新upDate
        self.pushButton2 = QtGui.QPushButton("upDate",Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(222, 107, 50, 22))
        self.pushButton2.setObjectName("pushButton")
        
        #import
        self.pushButton3 = QtGui.QPushButton("import",Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(167, 132, 110, 22))

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
        self.label_step = QtGui.QLabel('ステップ',Dialog)
        self.label_step.setGeometry(QtCore.QRect(180, 85, 50, 16))
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(220, 85, 40, 16))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        
        #checkboxソリッド
        self.checkbox = QtGui.QCheckBox("Solid",Dialog)
        self.checkbox.setGeometry(QtCore.QRect(100, 130, 61, 23))
        self.checkbox.setObjectName("checkbox")
        self.checkbox.setChecked(True)
        
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(0, 150, 300, 300))
        self.img.setText("")
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        
        self.retranslateUi(Dialog)
        self.comboBox_type.addItems(Ptype)
        #self.comboBox_st.addItems(Post_data)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)

        self.comboBox_st.setCurrentIndex(1)
        self.comboBox_st.currentIndexChanged[int].connect(self.onSt)
        self.comboBox_st.setCurrentIndex(0)

        self.spinBoxL.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Post", None))
        
    def upDate(self):
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 print('aaaaaaaaaaaa')
                 parts_group = selected_object
                 for obj in selection:
                     try:
                         size=self.comboBox_size.currentText()
                         #L=self.spinBoxL.value()
                         label='Standard'
                         obj.addProperty("App::PropertyFloat", "Standard",label)
                         obj.Standard=size
                     except:
                         obj.Standard=size
                 App.ActiveDocument.recompute()         

    def read_data(self):
        global HShape
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 print('aaaaaaaaaaaa')
                 parts_group = selected_object
                 for obj in parts_group.Group:
                      print(obj.Label)  
                      if obj.Label=='HShape':
                          HShape=obj
                      elif obj.Label=='LShape':
                          return    

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
        global sa
        global key
        key = self.comboBox_type.currentText()

        if key=='Pst_H':
             sa=H_st
             pic='03_Pst_H.png'
        elif key=='Pst_L':
             sa=Angle_st
             pic='03_Pst_L.png'
        elif key=='Pst_C':
            sa=Channel_st
            pic='03_Pst_C.png'
        elif key=='Pst_SQ':
            sa=Square_pipe_st
            pic='03_Pst_SQ.png'
        elif key=='Pst_Pipe':
            sa=Pipe_st
            pic='03_Pst_Pip.png'  
        self.comboBox_st.clear()
        self.comboBox_st.addItems(sa)

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "StlStu_data",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))  

    def onSt(self):
        global ta
        global key2
        key2=self.comboBox_st.currentText()
        if key=='Pst_H':
            if key2=='SS_Wide':
                ta=H_ss_w_size
        elif key=='Pst_L':
            if key2=='SS_Equal':
                ta=angle_ss_size
        elif key=='Pst_C':
            if key2=='SS':
                ta=channel_ss_size  
            elif key2=='SUS':
                ta=channel_sus_size  
        elif key=='Pst_SQ':
            if key2=='SS':
                ta=Square_pipe_ss_size       
            elif key2=='SUS':
                ta=Square_pipe_sus_size 
        elif key=='Pst_Pipe':
            if key2=='SS':
                ta=STK_ss_size
        self.comboBox_size.clear()
        self.comboBox_size.addItems(ta)  

    def create(self):
        
        Gui.activateWorkbench("DraftWorkbench")
        key=self.comboBox_type.currentText()
        if key=='Pst_H':
            fname='03_Pst_H.FCStd'  
        elif key=='Pst_L':
            fname='03_Pst_L.FCStd'  
        elif key=='Pst_C':
            fname='03_Pst_C.FCStd' 
        elif key=='Pst_SQ':
            fname='03_Pst_SQ.FCStd'  
        elif key=='Pst_Pipe':
            fname='03_Pst_Pip.FCStd'  

        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "StlStu_data",fname)
        Gui.ActiveDocument.mergeProject(joined_path)


class main():
    d = QtGui.QWidget()
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    d.show()
    script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
    script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)  

    
    
    







