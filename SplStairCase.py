# -*- coding: utf-8 -*-
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore
import FreeCAD
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import FreeCAD as App

from SplLib import ParamSplCase
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 390)
        Dialog.move(1000, 0)
        #高さ H
        self.label_H = QtGui.QLabel('Height H[mm]',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 10, 120, 21))
        self.lineEdit_H = QtGui.QLineEdit('2500',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(140, 10, 50, 22))
        #回転角度 a
        self.label_a = QtGui.QLabel('Rotation angle a[deg]',Dialog)
        self.label_a.setGeometry(QtCore.QRect(10, 35, 120, 21))
        self.lineEdit_a = QtGui.QLineEdit('360',Dialog)
        self.lineEdit_a.setGeometry(QtCore.QRect(140, 35, 50, 22))        
        #支柱径 d
        self.label_d = QtGui.QLabel('Prop diameter d[mm]',Dialog)
        self.label_d.setGeometry(QtCore.QRect(10, 60, 120, 21))
        self.lineEdit_d = QtGui.QLineEdit('165',Dialog)
        self.lineEdit_d.setGeometry(QtCore.QRect(140, 60, 50, 22))
        #外径 D
        self.label_D = QtGui.QLabel('Outer diameter D[mm]',Dialog)
        self.label_D.setGeometry(QtCore.QRect(10, 85, 120, 21))
        self.lineEdit_D = QtGui.QLineEdit('1600',Dialog)
        self.lineEdit_D.setGeometry(QtCore.QRect(140, 85, 50, 22))
        #ステップ高 hs
        self.label_hs = QtGui.QLabel('Step height hs',Dialog)
        self.label_hs.setGeometry(QtCore.QRect(10, 110, 200, 21))
        #ステップ厚 t
        self.label_t = QtGui.QLabel('Step thickness t',Dialog)
        self.label_t.setGeometry(QtCore.QRect(10, 135, 200, 21))
        self.lineEdit_t = QtGui.QLineEdit('50',Dialog)
        self.lineEdit_t.setGeometry(QtCore.QRect(140, 135, 50, 22))
        #段数 n
        self.label_n = QtGui.QLabel('No of step n',Dialog)
        self.label_n.setGeometry(QtCore.QRect(10, 160, 200, 21))
        self.lineEdit_n = QtGui.QLineEdit('12',Dialog)
        self.lineEdit_n.setGeometry(QtCore.QRect(140, 160, 50, 22))
        #w
        self.label_w = QtGui.QLabel('Inside step width w[mm]',Dialog)
        self.label_w.setGeometry(QtCore.QRect(10, 185, 130, 21))
        self.lineEdit_w = QtGui.QLineEdit('200',Dialog)
        self.lineEdit_w.setGeometry(QtCore.QRect(140, 185, 50, 22))
        #w1
        self.label_w1 = QtGui.QLabel('Outside step width w1[mm]',Dialog)
        self.label_w1.setGeometry(QtCore.QRect(10, 205, 130, 21))
        self.lineEdit_w1 = QtGui.QLineEdit('400',Dialog)
        self.lineEdit_w1.setGeometry(QtCore.QRect(140, 205, 50, 22))
        #create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 350, 100, 25))
        self.label_create = QtGui.QLabel('It will take some time',Dialog)
        self.label_create.setGeometry(QtCore.QRect(150, 350, 150, 21))
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(200, 0, 200, 300))
        self.lineEdit_d.setText('')
        self.lineEdit_d.textChanged.connect(self.on_dim)
        self.lineEdit_d.setText('165')
        self.lineEdit_D.textChanged.connect(self.on_dim)
        self.lineEdit_w.textChanged.connect(self.on_dim)
        self.lineEdit_H.textChanged.connect(self.on_dim)
        self.lineEdit_n.textChanged.connect(self.on_dim)
        self.lineEdit_w1.textChanged.connect(self.on_dim)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        pic='スパイラル3.jpg'
        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "SplLib",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))
        except:
            return
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'spiralStairCase', None))
    def on_dim(self):
        global H
        global d
        global D
        global n
        global w
        global w1
        global hs
        global l
        global rd
        global t
        global p
        global ra
        global H
        global a
        global D
        global d
        global n
        H=float(self.lineEdit_H.text())
        a=float(self.lineEdit_a.text())
        d=float(self.lineEdit_d.text()) 
        D=float(self.lineEdit_D.text()) 
        n=int(self.lineEdit_n.text()) 
        ra=math.radians(a/n)
        rd=float(a/n)
        w=float(self.lineEdit_w.text())
        w1=float(self.lineEdit_w1.text()) 
        t=float(self.lineEdit_t.text()) 
        s=math.asin(w1/D)
        l=D/2*math.cos(s)
        hs=round(H/n,2)
        p=H*360/a
        label='Step hight hs = '+str(hs)
        self.label_hs.setText(QtGui.QApplication.translate("Dialog", str(label), None))
    def create(self):
        label='SplStairCase'
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyFloat", "H",label).H=H
        obj.addProperty("App::PropertyFloat", "a",label).a=a
        obj.addProperty("App::PropertyFloat", "d",label).d=d
        obj.addProperty("App::PropertyFloat", "D",label).D=D
        obj.addProperty("App::PropertyInteger", "n",label).n=n
        obj.addProperty("App::PropertyFloat", "w",label).w=w
        obj.addProperty("App::PropertyFloat", "w1",label).w1=w1
        obj.addProperty("App::PropertyFloat", "t",label).t=t
        ParamSplCase.SplCase(obj) 
        obj.ViewObject.Proxy=0
        Gui.SendMsgToActiveView("ViewFit")
        #FreeCAD.ActiveDocument.recompute()  
        return

class Main_P():
        w = QtGui.QWidget()
        w.ui = Ui_Dialog()
        w.ui.setupUi(w)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        w.show()
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

