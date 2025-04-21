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
class HxgBlt:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        key=App.ActiveDocument.getObject(label).key
        Thread=App.ActiveDocument.getObject(label).Thread
        dia=App.ActiveDocument.getObject(label).dia
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        sa=ScrData.regular[dia]
        p=sa[0]
        H1=sa[1]
        m=sa[13]
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
        #先端カット
        z=2*p
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c01=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        
        if key=='01':
            #print(key,L1,L2)     
            #六角面
            x1=(e0/2)*math.cos(math.pi/6)
            y1=(e0/2)*math.sin(math.pi/6)
            p1=(x1,y1,L1)
            p2=(0,e0/2,L1)
            p3=(-x1,y1,L1)
            p4=(-x1,-y1,L1)
            p5=(0,-e0/2,L1)
            p6=(x1,-y1,L1)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.extrude(Base.Vector(0,0,m))
            c00=c1.fuse(cb)
            #外側_上
            y2=m+L1
            p1=(dk/2,0,y2)
            p2=(e0/2,0,y2)
            p3=(e0/2,0,y2-(e0-dk)/2*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c22=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0.0,0.0,1.0),360)
            c00=c00.cut(c22)
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

            cutProfile.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
            helix.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),180))
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            
            helix2=Part.makeHelix(p,p,D0/2,45,False)
            cutProfile2=cutProfile
            pipe2 = Part.Wire(helix2).makePipeShell([cutProfile2],makeSolid,isFrenet)

            pipe=pipe.fuse(pipe2)
            pipe.Placement=App.Placement(App.Vector(0,0,p+L2+p),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(pipe)
        
        c00=c00.cut(c01) 
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c00