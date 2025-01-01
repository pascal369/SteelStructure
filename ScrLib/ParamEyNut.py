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
class EyNut:#08アイナット
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
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
        sa=ScrData.eye_nut[dia]
        a=float(sa[0])
        b=float(sa[1])
        c=float(sa[2])
        D=float(sa[3])
        t=float(sa[4])
        h=float(sa[5])
        H=float(sa[6])
        x=1.1*(h-b/2)
        p1=(0,0,0)
        p2=(0,0,x)
        p3=(c/2,0,x)
        p4=(1.7*D0,0,t)
        p5=(2*D0,0,0)
        plist=[p1,p2,p3,p4,p5,p1]
        w10=Part.makePolygon(plist)
        wface = Part.Face(w10)
        c1=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c2=Part.makeTorus((b+c)/2,c/2,Base.Vector(0,0,h),Base.Vector(0,1,0))
        c1=c1.fuse(c2)
        if Thread==True:
            #ねじ断面
            H0=0.866025*p
            x0=H1+H0/4
            y0=x0*math.tan(math.pi/6)
            a0=p/2-y0
            p1=(-(D0-x0),0,-p/2)
            p2=(-(D0-x0),0,p/2)
            p3=(-D0,0,a0)
            p4=(-D0,0,-a0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p1)
            #らせん_sweep
            helix=Part.makeHelix(p,p+x/1.1,D0,0,False)
            helix.Placement=App.Placement(App.Vector(0,0,-0.5*p),App.Rotation(App.Vector(0,0,1),0))
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c2= Part.makeCylinder(D1,4*p+x,Base.Vector(0,0,-p),Base.Vector(0,0,1),360)
            pipe=pipe.fuse(c2)
            c1=c1.cut(pipe)
        else:
            c2=Part.makeCylinder(D0,x)
            c1=c1.cut(c2)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)     
        obj.Shape=c1    