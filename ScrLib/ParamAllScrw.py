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
class AllScrw:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        Thread=App.ActiveDocument.getObject(label).Thread
        dia=App.ActiveDocument.getObject(label).dia
        L1=App.ActiveDocument.getObject(label).L1
        L2=L1
        #ボルトねじ部
        def bolt_screw(self):
            global c00
            global c0
            global c01
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
            cb= Part.makeCylinder(D0/2,L2,Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト部
            c00=cb
            z=p
            p1=(-D0/2,0,0)
            p2=(-D0/2,0,z)
            p3=(-D0/2+z,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)#ボルト先端カット
            c01=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト先端カット
            c01.Placement=App.Placement(App.Vector(0,0,L2),App.Rotation(App.Vector(0,1,0),180))#ボルト先端カット
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
                helix=Part.makeHelix(p,L2,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                cutProfile.Placement=App.Placement(App.Vector(0,0,-0.5*p),App.Rotation(App.Vector(0,0,1),0))
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)

            c00=c00.cut(c01)
            c00=c00.cut(c0)    
        bolt_screw(self)
        c1=c00
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1
        