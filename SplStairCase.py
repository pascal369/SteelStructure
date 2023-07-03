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
        Dialog.move(800, 0)
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

        def prop(self):
            global c00
            c00=Part.makeCylinder(d/2,H)
        def step(self):
            global c00
            p1=(0,w/2,0) 
            p2=(0,-w/2,0)
            p3=(l,-w1/2,0)
            p4=(l,w1/2,0)  
            p5=(D/2,0,0) 
            edge1=Part.makeLine(p1,p2)
            #Part.show(edge1)
            edge2=Part.makeLine(p2,p3)
            #Part.show(edge2)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p5),Base.Vector(p4)).toShape()
            #Part.show(edge3)
            edge4=Part.makeLine(p4,p1)
            wire=Part.Wire([edge1,edge2,edge3,edge4])
            face=Part.Face(wire)
            c00=face.extrude(Base.Vector(0,0,-t))
            #Part.show(c00)
        def handrail1(self):
            global c00
            c00=Part.makeCylinder(34/2,1100,Base.Vector(l-34/2,0,hs),Base.Vector(0,0,1))
        def handrail2(self):
            global c00
            helix=Part.makeHelix(p,H,l-34/2,0,False)
            #awire=helix
            helix.Placement=App.Placement(App.Vector(0,0,1100),App.Rotation(App.Vector(0,0,1),0))
            #Part.show(helix)
            #profile=Part.makeCircle(43/2,Base.Vector(l-34/2,0,1100),Base.Vector(0,1,0))
            r=21.5
            p1=(0,0,r)
            p2=(-r,0,0)
            p3=(0,0,-r)
            p4=(r,0,0)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2])
            
            #pface=Part.Face(awire)
            awire.Placement=App.Placement(App.Vector(l-17,0,1100),App.Rotation(App.Vector(0,0,1),0))
            #Part.show(pface)
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(helix).makePipeShell([awire],makeSolid,isFrenet)
            #Part.show(c00)
            #return    
        #支柱
        prop(self)
        c1=c00
        #ステップ
        #self.label_H.setText(QtGui.QApplication.translate("Dialog", str(p), None))
        for i in range(n):
            step(self)
            c2=c00
            #Part.show(c2)
            c2.Placement=App.Placement(App.Vector(0,0,i*hs+hs),App.Rotation(App.Vector(0,0,1),i*rd+rd))
            c1=c1.fuse(c2)
            handrail1(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(0,0,i*hs),App.Rotation(App.Vector(0,0,1),i*rd+rd))
            c1=c1.fuse(c2)
        #Part.show(c1)    
        handrail2(self)
        c2=c00
        h1=(rd/(360))*(l-17)+21.5*1.5
        c2.Placement=App.Placement(App.Vector(0,0,h1),App.Rotation(App.Vector(0,0,1),rd/2))
        c1=c1.fuse(c2)


            
        '''    
        label= 'Spiral staircase'
        doc=App.ActiveDocument
        F_Obj = doc.addObject("Part::Feature",label)
        F_Obj.Shape=c1
        Gui.SendMsgToActiveView("ViewFit")
        '''
        
class Main_P():
        w = QtGui.QWidget()
        w.ui = Ui_Dialog()
        w.ui.setupUi(w)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        w.show()

#if __name__=='__main__':
#   Main_P()        