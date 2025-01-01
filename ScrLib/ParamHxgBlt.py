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
        cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c00=cb
        z=p/2
        p1=(-D0/2,0,0)
        p2=(-D0/2,0,z)
        p3=(-D0/2+z,0,0)
        plist=[p1,p2,p3,p1]
        w10=Part.makePolygon(plist)
        wface=Part.Face(w10)
        c01=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0.0,0.0,1.0),360)
        if key=='01':
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
                helix=Part.makeHelix(p,-p+L2,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            cutProfile.Placement=App.Placement(App.Vector(0,0,-0.5*p),App.Rotation(App.Vector(0,0,1),0))
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.cut(pipe)
            if key=='01' :
                L3=L1-L2
                if L3>0:
                    cb1= Part.makeCylinder(D0/2,L3,Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
                    c00=c00.cut(cb1)
                    c00=c00.fuse(cb1)
            elif key=='05' :
                if L3<0:
                    cb1= Part.makeCylinder(D0/2,2*p,Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
                    c00=c00.cut(cb1)
        else:
            c1= Part.makeCylinder(D0/2,L2,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c1=c1.cut(c01)
            L3=L1-L2
        c00=c00.cut(c01) 
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)    
        obj.Shape=c00