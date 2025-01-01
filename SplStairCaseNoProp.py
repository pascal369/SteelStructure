# -*- coding: utf-8 -*-
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore
import FreeCAD
import FreeCADGui as Gui
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
from SplLib import ParamSplCaseNP


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 390)
        Dialog.move(1000, 0)
        #高さ
        self.label_H = QtGui.QLabel('Height H[mm]',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 10, 120, 21))
        self.lineEdit_H = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(130, 10, 60, 22))
        #回転角度 st
        self.label_st = QtGui.QLabel('Rotation angle st[deg]',Dialog)
        self.label_st.setGeometry(QtCore.QRect(10, 35, 120, 21))
        self.lineEdit_st = QtGui.QLineEdit('360',Dialog)
        self.lineEdit_st.setGeometry(QtCore.QRect(140, 35, 50, 22))        
        #内径
        self.label_d = QtGui.QLabel('Inner diameter d[mm]',Dialog)
        self.label_d.setGeometry(QtCore.QRect(10, 60, 120, 21))
        self.lineEdit_d = QtGui.QLineEdit('1600',Dialog)
        self.lineEdit_d.setGeometry(QtCore.QRect(130, 60, 60, 22))

        #外径
        self.label_D = QtGui.QLabel('Outer diameter D[mm]',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 85, 120, 21))
        self.lineEdit_D = QtGui.QLineEdit('3200',Dialog)
        self.lineEdit_D.setGeometry(QtCore.QRect(130, 85, 60, 22))
        '''
        #ステップ高
        self.label_hs = QtGui.QLabel('Step height hs',Dialog)
        self.label_hs.setGeometry(QtCore.QRect(10, 110, 120, 21))
        self.lineEdit_hs = QtGui.QLineEdit('150',Dialog)
        self.lineEdit_hs.setGeometry(QtCore.QRect(130, 110, 60, 22))
        '''
        #段数
        self.label_n = QtGui.QLabel(Dialog)
        self.label_n.setGeometry(QtCore.QRect(10, 135, 200, 21))

        #a
        self.label_a = QtGui.QLabel('a[mm]',Dialog)
        self.label_a.setGeometry(QtCore.QRect(10, 155, 120, 21))
        self.lineEdit_a = QtGui.QLineEdit('50',Dialog)
        self.lineEdit_a.setGeometry(QtCore.QRect(130, 155, 60, 22))

        #t1
        self.label_t1 = QtGui.QLabel('t1[mm]',Dialog)
        self.label_t1.setGeometry(QtCore.QRect(10, 180, 120, 21))
        self.lineEdit_t1 = QtGui.QLineEdit('50',Dialog)
        self.lineEdit_t1.setGeometry(QtCore.QRect(130, 180, 60, 22))

        #t2
        self.label_t2 = QtGui.QLabel('t2[mm]',Dialog)
        self.label_t2.setGeometry(QtCore.QRect(10, 205, 120, 21))
        self.lineEdit_t2 = QtGui.QLineEdit('100',Dialog)
        self.lineEdit_t2.setGeometry(QtCore.QRect(130, 205, 60, 22))

        #h
        self.label_h = QtGui.QLabel('h[mm]',Dialog)
        self.label_h.setGeometry(QtCore.QRect(10, 230, 120, 21))
        self.lineEdit_h = QtGui.QLineEdit('400',Dialog)
        self.lineEdit_h.setGeometry(QtCore.QRect(130, 230, 60, 22))
        
        #C
        self.label_C = QtGui.QLabel(Dialog)
        self.label_C.setGeometry(QtCore.QRect(10, 255, 200, 21))
        #b
        self.label_b = QtGui.QLabel('b=(D-d)/2=',Dialog)
        self.label_b.setGeometry(QtCore.QRect(10, 280, 120, 21))
        #f
        self.label_f = QtGui.QLabel('f=b+2*a=',Dialog)
        self.label_f.setGeometry(QtCore.QRect(10, 305, 120, 21))
        
        #create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 355, 100, 25))

        self.label_create = QtGui.QLabel('It will take some time',Dialog)
        self.label_create.setGeometry(QtCore.QRect(150, 355, 150, 21))
        
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(200, 0, 200, 300))

        #H0
        self.label_H0= QtGui.QLabel('H0=',Dialog)
        self.label_H0.setGeometry(QtCore.QRect(200, 305, 120, 21))

        #self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_d.setText('')
        self.lineEdit_d.textChanged.connect(self.on_dim)
        self.lineEdit_d.setText('1600')
        self.lineEdit_D.textChanged.connect(self.on_dim)
        self.lineEdit_a.textChanged.connect(self.on_dim)
        self.lineEdit_H.textChanged.connect(self.on_dim)
        #self.lineEdit_hs.textChanged.connect(self.on_dim)
        self.lineEdit_t1.textChanged.connect(self.on_dim)
        self.lineEdit_t2.textChanged.connect(self.on_dim)
        self.lineEdit_h.textChanged.connect(self.on_dim)
        self.lineEdit_st.textChanged.connect(self.on_dim)
        #self.lineEdit_p.textChanged.connect(self.on_dim)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        pic='スパイラル.jpg'

        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "SplLib",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))
        except:
            return

       
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "spiralStairCase", None))    
    def on_dim(self):
        global H
        global p
        global D
        global d
        global a
        global t1
        global t2
        global h
        global n
        global C
        global b
        global f
        global hs
        global k
        global k1
        global h0
        global m
        global st
        global ra
        global rd
        global H0
        global p
        H=float(self.lineEdit_H.text())
        st=float(self.lineEdit_st.text())
        p=H*360/st
        #m=p/H
        m=1
        D=float(self.lineEdit_D.text())
        d=float(self.lineEdit_d.text())
        a=float(self.lineEdit_a.text())
        t1=float(self.lineEdit_t1.text())
        t2=float(self.lineEdit_t2.text())
        h=float(self.lineEdit_h.text())
        #hs=int(self.lineEdit_hs.text())
        C=d/2+(D-d)/4
        b=(D-d)/2
        f=b+2*a
        D1=(D-d)/2
        #k1=float(math.atan(p/(D)))
        #self.label_H.setText(QtGui.QApplication.translate("Dialog", str(math.degrees(k1)), None))
        label='C=d/2+(D-d)/4=' + str(C) + '[mm]'
        self.label_C.setText(QtGui.QApplication.translate("Dialog", str(label), None))
        label='b=(D-d)/2=' + str(b) + '[mm]'
        self.label_b.setText(QtGui.QApplication.translate("Dialog", str(label), None))
        label='f=b+2*a=' + str(f) + '[mm]'
        self.label_f.setText(QtGui.QApplication.translate("Dialog", str(label), None))
        hs=150.0
        n=int(H/hs)

        #hs=H/n
        ra=math.radians(st/n)
        rd=float(st/n)
        #n=int((H+hs-h-t1)/hs)
        label='Number of steps n=' + str(n) 
        self.label_n.setText(QtGui.QApplication.translate("Dialog", str(label), None))
        h0=h+t1+hs

        k=float(st/360*math.radians(st*p/(H*n)))
        #k=ra
        #self.label_H.setText(QtGui.QApplication.translate("Dialog", str(math.degrees(k)), None))
        H0=(n-1)*hs+h+t1
        label='H0='+str(H0)+'[mm]'
        self.label_H0.setText(QtGui.QApplication.translate("Dialog", str(label), None))
    def create(self):
        label='SplStairCase'
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyFloat", "H",label).H=H
        obj.addProperty("App::PropertyFloat", "st",label).st=st
        obj.addProperty("App::PropertyFloat", "d",label).d=d
        obj.addProperty("App::PropertyFloat", "D",label).D=D
        #obj.addProperty("App::PropertyFloat", "hs",label).hs=hs
        obj.addProperty("App::PropertyFloat", "a",label).a=a
        obj.addProperty("App::PropertyFloat", "t1",label).t1=t1
        obj.addProperty("App::PropertyFloat", "t2",label).t2=t2
        obj.addProperty("App::PropertyFloat", "h",label).h=h
        obj.addProperty("App::PropertyFloat", "C",label).C=C
        obj.addProperty("App::PropertyFloat", "b",label).b=b
        obj.addProperty("App::PropertyFloat", "f",label).f=f
        obj.addProperty("App::PropertyFloat", "H0",label).H0=H0
        #obj.addProperty("App::PropertyFloat", "p",label).p=p
        obj.addProperty("App::PropertyInteger", "n",label).n=n
        obj.addProperty("App::PropertyFloat", "k",label).k=k
        obj.addProperty("App::PropertyFloat", "m",label).m=m
        ParamSplCaseNP.SplCaseNP(obj) 
        obj.ViewObject.Proxy=0
        Gui.SendMsgToActiveView("ViewFit")
        #FreeCAD.ActiveDocument.recompute()    
            
        
class Main_P():
        w = QtGui.QWidget()
        w.ui = Ui_Dialog()
        w.ui.setupUi(w)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        w.show()
        # スクリプトのウィンドウを取得
        script_window = FreeCADGui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

