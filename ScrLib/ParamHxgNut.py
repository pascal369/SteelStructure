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
import FreeCADGui as Gui

class HxgNut:#00六角ナット
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        st=App.ActiveDocument.getObject(label).st
        dia=App.ActiveDocument.getObject(label).dia
        Thread=App.ActiveDocument.getObject(label).Thread
        sa=ScrData.regular[dia]
        p=sa[0]
        H1=sa[1]
        m=sa[6]
        m1=sa[7]
        s0=sa[8]
        e0=sa[9]
        D0=sa[2]/2
        D2=sa[3]/2
        D1=sa[4]/2
        dk=sa[5]/2
        H0=0.866025*p
        x=H1+H0/4
        y=x*math.tan(math.pi/6)
        a=p/2-y
        #六角面
        x1=e0/2*math.cos(math.pi/6)
        y1=e0/2*math.sin(math.pi/6)
        p1=(x1,y1,0)
        p2=(0,e0/2,0)
        p3=(-x1,y1,0)
        p4=(-x1,-y1,0)
        p5=(0,-e0/2,0)
        p6=(x1,-y1,0)
        plist=[p1,p2,p3,p4,p5,p6,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        if st=='Type3':
            H=m1
        else:
            H=m
        c1=wface.extrude(Base.Vector(0,0,H))
        c2=Part.makeCylinder(D1,H)
        c00=c1.cut(c2)
        #1,2,3種
        #面取り上
        p1=(dk,0,H)
        p2=(e0/2,0,H)
        p3=(e0/2,0,H-(e0/2-dk)*math.tan(math.pi/6))
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
        c00=c00.cut(c2)
        #面取り 内側下
        p1=(D0+0.1,0,0)
        p2=(0,0,0)
        p3=(0,0,(D0+0.1)*math.tan(math.radians(30)))
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c20=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c00=c00.cut(c20)
        #2,3種
        if st=='Type2' or st=='Type3':
            p1=(dk,0,0)
            p2=(e0/2,0,0)
            p3=(e0/2,0,(e0/2-dk)*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c23=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
            c00=c00.cut(c23)
            #面取り 内側上
            p1=(D0+0.1,0,H)
            p2=(0,0,H)
            p3=(0,0,H-(D0+0.1)*math.tan(math.radians(30)))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
            c00=c00.cut(c2)
        if Thread==True:
            #ねじ断面
            p1=(-(D0-x),0,-p/2)
            p2=(-(D0-x),0,p/2)
            p3=(-D0,0,a)
            p4=(-D0,0,-a)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p1)
            #らせん_sweep
            helix=Part.makeHelix(p,2*p+H,D0,0,False)
            helix.Placement=App.Placement(App.Vector(0,0,-p),App.Rotation(App.Vector(0,0,1),0))
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c2= Part.makeCylinder(D1,4*p+H,Base.Vector(0,0,-2*p),Base.Vector(0,0,1),360)
            pipe=pipe.fuse(c2)
            c00=c00.cut(pipe)
        else:
            c2=Part.makeCylinder(D0,H)
            c00=c00.cut(c2)
        c00=c00.cut(c20)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0) 
        obj.Shape=c00
        
      