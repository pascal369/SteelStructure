from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ScrData
class ShBlt:#六角穴付きボルト
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        def hex_cutter(self):#六角穴カッター
            global c001
            global t3
            sa1=ScrData.sh_dia[dia]
            t=float(sa1[2])
            k=float(sa1[1])
            e0=s1/math.cos(math.pi/6)
            x1=(e0/2)*math.cos(math.pi/6)
            y1=(e0/2)*math.sin(math.pi/6)
            t1=e0/2*math.tan(math.pi/6)
            t2=t+t1
            t3=k-t2
            p1=(x1,y1,0)
            p2=(0,e0/2,0)
            p3=(-x1,y1,0)
            p4=(-x1,-y1,0)
            p5=(0,-e0/2,0)
            p6=(x1,-y1,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c001=wface.extrude(Base.Vector(0,0,t2))
            #下部カット
            p1=(-e0/2,0,0)
            p2=(-e0/2,0,t1)
            p3=(0,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c002=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)
            c001=c001.cut(c002)
        label=obj.Name
        Thread=App.ActiveDocument.getObject(label).Thread
        dia=App.ActiveDocument.getObject(label).dia
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        st=App.ActiveDocument.getObject(label).st
        sa=ScrData.sh_dia[dia]
        dk1=float(sa[0])
        k=float(sa[1])
        t=float(sa[2])
        v=float(sa[3])
        if st=='Section1':
            s1=float(sa[4])
        elif st=='Section2':
            s1=float(sa[5])
        sa=ScrData.regular[dia]
        p=sa[0]
        H1=sa[1]
        m=sa[6]
        m1=sa[7]
        s0=sa[8]
        e0=sa[9]
        D0=sa[2]
        D2=sa[3]
        D1=sa[4]
        dk=sa[5]
        z=sa[10]
        H0=0.86625*p
        x=H1+H0/8
        y=x*math.tan(math.pi/6)
        r0=D0/2+H0/8
        a=p/2-y
        #ボルト部
        cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)#首下長さ
        c00=cb
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0.0,0.0,1.0),360)#軸先端カット
        #ソケットヘッド
        c1= Part.makeCylinder(dk1/2,k,Base.Vector(0,0,L1),Base.Vector(0,0,1),360)
        c00=c00.fuse(c1)
        #外側_上
        p1=(dk1/2,0,k-v)
        p2=(dk1/2,0,k)
        p3=(dk1/2-v,0,k)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c1=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c1.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
        c00=c00.cut(c1)
        hex_cutter(self)
        c01=c001
        c01.Placement=App.Placement(App.Vector(-L1-t3,0,0),App.Rotation(App.Vector(0,1,0),-90))
        c00=c00.cut(c01)
        #ねじ断面
        if Thread==True:
            p1=(D1/2,0,-a)
            p2=(D1/2,0,a)
            p3=(r0,0,p/2)
            p4=(r0,0,-p/2)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p1)
            #らせん_sweep
            L3=L1-L2
            if  L3>0:
                helix=Part.makeHelix(p,p+L2,D0/2,0,False)
            else:
                helix=Part.makeHelix(p,L2,D0/2,0,False)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.cut(pipe)
            #if key=='02':
            L3=L1-L2
            if L3>0:
                cb1= Part.makeCylinder(D0/2,L3,Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
                c00=c00.cut(cb1)
                c00=c00.fuse(cb1)
        else:
            c1= Part.makeCylinder(D0/2,L2,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=c00.cut(c1)
            c00=c00.fuse(c1)
        L3=L1-L2
        if L3<=0:
            L3=0.1
            c2= Part.makeCylinder(D0/2,L3,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L2),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
        if z!=0:
            c00=c00.cut(c0)
        c00.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
        c00=c00.cut(c01)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0) 
        obj.Shape=c00