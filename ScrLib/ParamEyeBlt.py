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
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        Thread=App.ActiveDocument.getObject(label).Thread
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2

        sa1=ScrData.eye_bolt[dia]
        a=float(sa1[0])
        b=float(sa1[1])
        c=float(sa1[2])
        D=float(sa1[3])
        t=float(sa1[4])
        h=float(sa1[5])
        l=float(sa1[7])
        H=float(sa1[6])
        e=float(sa1[8])

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
        cb= Part.makeCylinder(D0/2,l,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c00=cb
        z=2*p
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c01=wface.revolve(Base.Vector(0,0,0),Base.Vector(0.0,0.0,1.0),360)
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
            L3=L1-L2
            if  L3>0:
                helix=Part.makeHelix(p,p+L2,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            else:
                return

            cutProfile.Placement=App.Placement(App.Vector(0,0,l),App.Rotation(App.Vector(0,0,1),0))
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)

            c00=c00.cut(pipe)

        c1=c00

        #neck cut
        p1=((D1-0.9*p)/2,0,0)
        p2=((D1-0.9*p)/2,0,e)
        p3=(D0/2,0,e)
        p4=(D0/2,0,0)
        plist=[p1,p2,p3,p4,p1]
        w0=Part.makePolygon(plist)
        wface=Part.Face(w0)
        c02=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c02.Placement=App.Placement(App.Vector(0,0,l-e),App.Rotation(App.Vector(0,0,1),0))
        c1=c1.cut(c02)
        
        #eye
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
        c2.Placement=App.Placement(App.Vector(0,0,l),App.Rotation(App.Vector(0,0,1),0))
        c1=c1.fuse(c2)
        c2=Part.makeTorus((b+c)/2,c/2,Base.Vector(0,0,l+h+p),Base.Vector(0,1,0))

        c1=c1.cut(c2)
        c1=c1.fuse(c2)
        
        c1=c1.cut(c01)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1
  