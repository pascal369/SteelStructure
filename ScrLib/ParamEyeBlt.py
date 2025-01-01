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
class EyeBlt:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        Thread=App.ActiveDocument.getObject(label).Thread
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        def hexagon_bolt(self):
            global c00
            global D0
            global c0
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
            cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=cb
            p1=(-D0/2,0,0)
            p2=(-D0/2,0,z)
            p3=(-D0/2+z,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0.0,0.0,1.0),360)
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
                    cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                else:
                    helix=Part.makeHelix(p,p+L2,D0/2,0,False)
                    cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                cutProfile.Placement=App.Placement(App.Vector(0,0,-0.5*p),App.Rotation(App.Vector(0,0,1),0))
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)
            else:
                c00= Part.makeCylinder(D0/2,L2,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            L3=L1-L2
            if L3<=0:
                L3=0.1
            c2= Part.makeCylinder(D0/2,L3,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        hexagon_bolt(self)
        c1=c00
        if L1>L2:
            c2= Part.makeCylinder(D0/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c1=c1.cut(c2)
            c1=c1.fuse(c2)
            c1=c1.cut(c0)
        sa=ScrData.eye_bolt[dia]
        a=float(sa[0])
        b=float(sa[1])
        c=float(sa[2])
        D=float(sa[3])
        t=float(sa[4])
        h=float(sa[5])
        H=float(sa[6])
        e1=H-a
        f=t-e1
        g=h-b/2
        p1=(0,0,0)
        p2=(0,0,g)
        p3=(D/2,0,t)
        p4=(D/2,0,0)
        p5=(0,0,H-a/2)
        plist=[p1,p2,p3,p4,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
        c1=c1.fuse(c2)
        c2=Part.makeTorus((b+c)/2,c/2,Base.Vector(0,0,L1+h),Base.Vector(0,1,0))
        c1=c1.cut(c2)
        c1=c1.fuse(c2)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0) 
        obj.Shape=c1
  