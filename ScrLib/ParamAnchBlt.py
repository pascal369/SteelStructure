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
class AnchBlt:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        #key=App.ActiveDocument.getObject(label).key
        Thread=App.ActiveDocument.getObject(label).Thread
        st=App.ActiveDocument.getObject(label).st
        dia=App.ActiveDocument.getObject(label).dia
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
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
        H0=0.86625*p
        x=H1+H0/8
        y=x*math.tan(math.pi/6)
        r0=D0/2+H0/8
        a=p/2-y
        #ボルト部
        #らせん_sweep
        z=2*p
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c01=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
        #Part.show(c01)
        if st=='Type_J':
            sa=ScrData.anchor_J[dia]
        elif st=='Type_L':
            sa=ScrData.anchor_L[dia]
        d=float(sa[0])
        L10=float(sa[3])
        A=float(sa[4])
        L1=L1-d/2
        L10=L10-d/2
        A=A-d
        B=(A/2)*(1-1/math.sqrt(2))
        p1=(L2,0,0)
        p2=(L1-A/2,0,0)
        p3=(L1,0,A/2)
        p4=(L1-A/2,0,A)
        p5=(L1-L10,0,A)
        p6=(0,0,0)
        p7=(L1-B,0,B)
        p8=(L1,0,A)
        edge1 = Part.makeLine(p6,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3 = Part.makeLine(p4,p5)
        edge4=Part.Arc(Base.Vector(p2),Base.Vector(p7),Base.Vector(p3)).toShape()
        edge5 = Part.makeLine(p3,p8)
        edge6= Part.makeCircle(d/2, Base.Vector(p1), Base.Vector(1,0,0), 0, 360)
     
        if st=='Type_J':
            aWire = Part.Wire([edge1,edge2,edge3])
            #Part.show(aWire)
        elif st=='Type_L':
            aWire = Part.Wire([edge1,edge4,edge5])
            #Part.show(aWire)
        #Part.show(aWire)    
        profile = Part.Wire([edge6])
        makeSolid=True
        isFrenet=True
        c1 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
        #Part.show(c1)
 
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

            L3=L1-L2
            if  L3>0:
                helix=Part.makeHelix(p,p+L2,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            else:
                return

            cutProfile.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
            helix.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),180))
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            
            helix2=Part.makeHelix(p,p,D0/2,45,False)
            helix2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
            cutProfile2=cutProfile
            cutProfile2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
            pipe2 = Part.Wire(helix2).makePipeShell([cutProfile2],makeSolid,isFrenet)

            pipe=pipe.fuse(pipe2)
            pipe.Placement=App.Placement(App.Vector(p+L2+p,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.cut(pipe)
        c1=c1.cut(c01)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1