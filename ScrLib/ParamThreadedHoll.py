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
class ThreadedHoll:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        st=App.ActiveDocument.getObject(label).st
        Thread=App.ActiveDocument.getObject(label).Thread
        L2=App.ActiveDocument.getObject(label).L2
        L1=L2
        
        #global c00
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
        n=sa[11]
        z=p/2
        H0=0.86625*p
        x=H1+H0/8
        y=x*math.tan(math.pi/6)
        r0=D0/2+H0/8
        a=p/2-y
        #ボルト部
        cb= Part.makeCylinder(D0/2,2*p+L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト部
        cb1= Part.makeCylinder(D0/2,2*p,Base.Vector(0,0,L1),Base.Vector(0,0,1),360)#ボルト部
        #Part.show(cb1)
        c00=cb
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        #c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)#ボルト先端カット
        c01=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト先端カット
        #print(D0)
        #print(st)
        #Part.show(c01)
        #ねじ断面
        if Thread==True:
            p1=(D1/2,0,-a)
            p2=(D1/2-a/2,0,0)
            p3=(D1/2,0,a)
            p4=(r0,0,p/2)
            p5=(r0,0,-p/2)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2 = Part.makeLine(p3,p4)
            edge3 = Part.makeLine(p4,p5)
            edge4 = Part.makeLine(p5,p1)
            #らせん_sweep
            helix=Part.makeHelix(p,p+L1,D0/2,0,False)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            #Part.show(pipe)
            #Part.show(c00)
            c00=c00.cut(pipe)
 
        c1=c00
        sa1=ScrData.set_screw[dia]
        dk=float(dia[1:])
        e0=float(sa1[1])
        dp=float(sa1[2])
        dt=float(sa1[3])
        t01=float(sa1[5])
        t02=float(sa1[6])
        #六角穴部
        if st=='Flat_head_1' or st=='Point_ahead_1':
            t=t01
        else:
            t=t02
        x1=(e0/2)*math.cos(math.pi/6)
        y1=(e0/2)*math.sin(math.pi/6)
        t1=e0/2*math.tan(math.pi/6)
        t2=t+t1
        z=L2-t2
        p1=(x1,y1,z)
        p2=(0,e0/2,z)
        p3=(-x1,y1,z)
        p4=(-x1,-y1,z)
        p5=(0,-e0/2,z)
        p6=(x1,-y1,z)
        plist=[p1,p2,p3,p4,p5,p6,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        c001=wface.extrude(Base.Vector(0,0,t2))
        c1=c1.cut(c001)
        #下部カット
        p1=(-e0/2,0,0)
        p2=(-e0/2,0,t1)
        p3=(0,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        c002=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)
        c001=c001.cut(c002)
        c001.Placement=App.Placement(App.Vector(0,0,L1-t2),App.Rotation(App.Vector(0,0,1),0))
        c001=c001.cut(c002)
        c001.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
        c1=c1.cut(c001)
        #下部カット
        d0p=dt
        x=(dk-d0p)/2
        p1=(d0p/2,0,0)
        p2=(dk/2,0,x)
        p3=(dk/2,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),0))
        c1=c1.cut(c2)
        c1=c1.cut(cb1)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1