# -*- coding: utf-8 -*-
import os
import sys
import FreeCADGui as Gui
from PySide import QtGui,QtCore
from FreeCAD import Base
import FreeCAD, Part , math
from math import pi
import FreeCAD as App
import FreeCADGui
from hdrl_data import ParamStraight
from hdrl_data import ParamEndLine
from hdrl_data import ParamCircular
from hdrl_data import ParamEdge
#from hdrl_data import ParamChannel
from hdrl_data import HandData
        
class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self
        return
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(260, 450)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 15, 60, 12))
        self.label_type.setObjectName("label_type")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 15, 160, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        #仕様
        self.label_siyo = QtGui.QLabel(Dialog)
        self.label_siyo.setGeometry(QtCore.QRect(10, 40, 60, 12))
        self.label_siyo.setObjectName("label_st")
        self.comboBox_siyo = QtGui.QComboBox(Dialog)
        self.comboBox_siyo.setGeometry(QtCore.QRect(80, 40, 160, 22))
        self.comboBox_siyo.setObjectName("comboBox_st")
        #長さL1
        self.label_l1 = QtGui.QLabel(Dialog)
        self.label_l1.setGeometry(QtCore.QRect(10, 92, 60, 12))
        self.label_l1.setObjectName("label_L1")
        self.lineEdit_l1 = QtGui.QLineEdit('L1',Dialog)
        self.lineEdit_l1.setGeometry(QtCore.QRect(80, 90, 50, 20))
        self.lineEdit_l1.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_l1.setObjectName("lineEdit_L1")
        #長さL2
        self.label_l2 = QtGui.QLabel(Dialog)
        self.label_l2.setGeometry(QtCore.QRect(133, 92, 60, 12))
        self.label_l2.setObjectName("label_L2")
        self.lineEdit_l2 = QtGui.QLineEdit('L2',Dialog)
        self.lineEdit_l2.setGeometry(QtCore.QRect(197, 90, 43, 20))
        self.lineEdit_l2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_l2.setObjectName("lineEdit_L1")
        #コーナー角度
        self.label_cn = QtGui.QLabel(Dialog)
        self.label_cn.setGeometry(QtCore.QRect(133, 117, 60, 12))
        self.label_cn.setObjectName("label_cn")
        self.lineEdit_cn = QtGui.QLineEdit(Dialog)
        self.lineEdit_cn.setGeometry(QtCore.QRect(197, 115, 43, 20))
        self.lineEdit_cn.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_cn.setObjectName("lineEdit_cn")
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 165, 61, 22))
        self.pushButton.setObjectName("pushButton")
        #リバース
        self.checkbox = QtGui.QCheckBox('Reverse',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(80, 165, 60, 23))
        self.checkbox.setChecked(False)
        #手すり高
        self.label_l = QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(10, 117, 115, 20))
        self.label_l.setAlignment(QtCore.Qt.AlignLeft)
        self.label_l.setObjectName("label_l")
        self.lineEdit_l = QtGui.QLineEdit(Dialog)
        self.lineEdit_l.setGeometry(QtCore.QRect(80, 115, 50, 20))
        self.lineEdit_l.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_l.setObjectName("lineEdit_l")
        #手すりピッチ
        self.label_p = QtGui.QLabel(Dialog)
        self.label_p.setGeometry(QtCore.QRect(10, 142, 115, 20))
        self.label_p.setAlignment(QtCore.Qt.AlignLeft)
        self.label_p.setObjectName("label_p")
        self.lineEdit_p = QtGui.QLineEdit(Dialog)
        self.lineEdit_p.setGeometry(QtCore.QRect(80, 142, 50, 20))
        self.lineEdit_p.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_p.setObjectName("lineEdit_p")
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 230, 200, 200))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.retranslateUi(Dialog)
        #比重
        self.mtrl = QtGui.QLabel('Specific gravity of material',Dialog)
        self.mtrl.setGeometry(QtCore.QRect(10, 190, 150, 12))
        self.le_mtrl = QtGui.QLineEdit(Dialog)
        self.le_mtrl.setGeometry(QtCore.QRect(180, 190, 50, 20))
        self.le_mtrl.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(HandData.type)
        self.comboBox_siyo.addItems(HandData.siyo)

        self.comboBox_siyo.setCurrentIndex(1)
        self.comboBox_siyo.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_siyo.setCurrentIndex(0)

        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.lineEdit_l.setText(QtGui.QApplication.translate("Dialog", '1100', None))
        self.lineEdit_l1.setText(QtGui.QApplication.translate("Dialog", '1500', None))
        self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", '1000', None))
        self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", '90', None))
        self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", '1000', None))
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handrail", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None))
        self.label_siyo.setText(QtGui.QApplication.translate("Dialog", "Spec", None))
        self.label_l1.setText(QtGui.QApplication.translate("Dialog", "length L1[m]", None))
        self.label_l2.setText(QtGui.QApplication.translate("Dialog", "length L2[m]", None))
        self.label_cn.setText(QtGui.QApplication.translate("Dialog", "angle k[deg]", None))
        self.label_l.setText(QtGui.QApplication.translate("Dialog", "height h[m]", None))
        self.label_p.setText(QtGui.QApplication.translate("Dialog", "pitch p[m]", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))

    def on_type(self):
        global key
        global spec_siyo
        
        key = self.comboBox_type.currentText()[:2]
        try:
            l=float(self.lineEdit_l.text())
            h=float(self.lineEdit_l.text())
            l1=float(self.lineEdit_l1.text())
            l2=float(self.lineEdit_l2.text())
            k=float(self.lineEdit_cn.text())
            p=float(self.lineEdit_p.text())
            #print(p)

        except:
            pass

        spec_siyo=self.comboBox_siyo.currentIndex()

        if key=='00':
            pic=str(spec_siyo)+'_直線01L.jpg'

            self.label_l1.setText(QtGui.QApplication.translate("Dialog", "length l1[m]", None))
            self.label_l2.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.label_cn.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", "1000", None))
        elif key=='01':
            pic=str(spec_siyo)+'_端部01L.jpg'

            self.label_l1.setText(QtGui.QApplication.translate("Dialog", "length l1[m]", None))
            self.label_l2.setText(QtGui.QApplication.translate("Dialog", "length l2[m]", None))
            self.label_cn.setText(QtGui.QApplication.translate("Dialog", "angle k[deg]", None))
            self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", "1000", None))
            self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", "90", None))

        elif key=='02':
            pic=str(spec_siyo)+'_コーナー01L.jpg'

            self.label_l1.setText(QtGui.QApplication.translate("Dialog", "length l1[m]", None))
            self.label_l2.setText(QtGui.QApplication.translate("Dialog", "length l2[m]", None))
            self.label_cn.setText(QtGui.QApplication.translate("Dialog", "angle k[deg]", None))
            self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", "1000", None))
            self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", "90", None))
            self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", "1000", None))
        elif key=='03':
            pic=str(spec_siyo)+'_arc01.jpg'

            self.label_l1.setText(QtGui.QApplication.translate("Dialog", "radius R[m]", None))
            self.label_l2.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.label_cn.setText(QtGui.QApplication.translate("Dialog", "angle k[deg]", None))
            self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", "90", None))
            #self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", "1000", None))
        elif key=='04':
           pic=str(spec_siyo)+'_edge01R.jpg'   

        elif key=='05':
           pic=str(spec_siyo)+'_edge01L.jpg'   

        elif key=='06':
           pic=str(spec_siyo)+'_channel01.jpg'  

        #'''   
        print (spec_siyo)
        if spec_siyo < 2:
           self.le_mtrl.setText(QtGui.QApplication.translate("Dialog", "7.85", None))  
        else:
           self.le_mtrl.setText(QtGui.QApplication.translate("Dialog", "2.70", None))     
        #'''

        self.label_l1.setText(QtGui.QApplication.translate("Dialog", "length l1[m]", None))
        self.label_l2.setText(QtGui.QApplication.translate("Dialog", "length l2[m]", None))
        self.label_cn.setText(QtGui.QApplication.translate("Dialog", "angle k[deg]", None))
        self.lineEdit_l2.setText(QtGui.QApplication.translate("Dialog", "1000", None))
        self.lineEdit_cn.setText(QtGui.QApplication.translate("Dialog", "90", None))  
        self.lineEdit_p.setText(QtGui.QApplication.translate("Dialog", "1000", None))  

        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "hdrl_data",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))
        except:
            pass    

    def create(self):
        global L0
        global l
        global h
        global l1
        global l2
        global k
        global p
        g0=float(self.le_mtrl.text())
        #Gui.activeDocument().activeView().viewTop()
        if key=='00':
            label='StraightLine'
        elif key=='01':
            label='Corner with end'
        elif key=='02':
            label='Corner' 
        elif key=='03':
            label='Circular_arc'   
        elif key=='04':
            label='Edge_R'   
        elif key=='05':
            label='Edge_L'  
        elif key=='06':
            label='Channel'   
        #print(label)
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyEnumeration", "spec",label)
        obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
        obj.spec=HandData.siyo
        i=self.comboBox_siyo.currentIndex()
        obj.spec=HandData.siyo[i] 

        h=float(self.lineEdit_l.text())
        l1=float(self.lineEdit_l1.text())
        p=float(self.lineEdit_p.text())
        #print(p)
        if key=='03':
            pass
        else:
            l2=self.lineEdit_l2.text()
        k=self.lineEdit_cn.text()
        obj.addProperty("App::PropertyFloat", "h",label).h=h
        obj.addProperty("App::PropertyFloat", "p",label).p=p
        if self.checkbox.isChecked():
            obj.addProperty("App::PropertyBool",'Reverse',label).Reverse = True
        else:
            obj.addProperty("App::PropertyBool",'Reverse',label).Reverse = False
            
        if key=='00' :
            obj.addProperty("App::PropertyFloat", "l1",label).l1=l1
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamStraight.StraightLine(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 
        elif key=='01' or key=='02' or key=='06':  
            
            obj.addProperty("App::PropertyFloat", "l1",label).l1=l1
            obj.addProperty("App::PropertyFloat", "l2",label).l2=float(l2)
            obj.addProperty("App::PropertyFloat", "k",label).k=float(k)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamEndLine.EndLine(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 
        elif key=='03':
            obj.addProperty("App::PropertyFloat", "R",label).R=l1
            obj.addProperty("App::PropertyFloat", "k",label).k=float(k)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamCircular.circular_arc(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()    
        elif key=='04' or key=='05':  
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=HandData.type
            i=self.comboBox_type.currentIndex()
            obj.type=HandData.type[i] 
            ParamEdge.edge(obj) 
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()  
            
        

class Main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        # スクリプトのウィンドウを取得
        script_window = FreeCADGui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)





