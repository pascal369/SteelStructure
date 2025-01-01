import FreeCAD
import FreeCADGui as Gui
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import FreeCAD as App
#import SplStairCase
class SplCase:
    def __init__(self, obj):
        self.Type = 'S01'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
        #return
    def execute(self, obj):
        label=obj.Name
        H=App.ActiveDocument.getObject(label).H
        a=App.ActiveDocument.getObject(label).a
        d=App.ActiveDocument.getObject(label).d
        D=App.ActiveDocument.getObject(label).D
        n=App.ActiveDocument.getObject(label).n
        w=App.ActiveDocument.getObject(label).w
        w1=App.ActiveDocument.getObject(label).w1
        t=App.ActiveDocument.getObject(label).t
        ra=math.radians(a/n)
        rd=float(a/n)
        s=math.asin(w1/D)
        #print(s)
        l=D/2*math.cos(s)
        hs=round(H/n,2)
        p=H*360/a
        def prop(self):
            global c00
            c00=Part.makeCylinder(d/2,H)
        def step(self):
            global c00
            p1=(0,w/2,0) 
            p2=(0,-w/2,0)
            p3=(l,-w1/2,0)
            p4=(l,w1/2,0)  
            p5=(D/2,0,0) 
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p5),Base.Vector(p4)).toShape()
            edge4=Part.makeLine(p4,p1)
            wire=Part.Wire([edge1,edge2,edge3,edge4])
            face=Part.Face(wire)
            c00=face.extrude(Base.Vector(0,0,-t))
        def handrail1(self):
            global c00
            c00=Part.makeCylinder(34/2,1100,Base.Vector(l-34/2,0,hs),Base.Vector(0,0,1))
        def handrail2(self):
            global c00
            #p=p*1600/D
            helix=Part.makeHelix(p,H,l-34/2,s,False)
            #Part.show(helix)
            helix.Placement=App.Placement(App.Vector(0,0,1100),App.Rotation(App.Vector(0,0,1),0))
            r=21.5
            p1=(0,0,r)
            p2=(-r,0,0)
            p3=(0,0,-r)
            p4=(r,0,0)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2])
            awire.Placement=App.Placement(App.Vector(l-17,0,1100),App.Rotation(App.Vector(0,0,1),0))
            #awire.Placement=App.Placement(App.Vector(l-17,0,0),App.Rotation(App.Vector(0,0,1),0))
            #Part.show(awire)
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(helix).makePipeShell([awire],makeSolid,isFrenet)
            #Part.show(c00)
        #支柱
        prop(self)
        c1=c00
        #ステップ
        for i in range(n):
            step(self)
            c2=c00
            #Part.show(c2)
            c2.Placement=App.Placement(App.Vector(0,0,i*hs+hs),App.Rotation(App.Vector(0,0,1),i*rd+rd))
            c1=c1.fuse(c2)
            handrail1(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(0,0,i*hs),App.Rotation(App.Vector(0,0,1),i*rd+rd))
            c1=c1.fuse(c2)
        handrail2(self)
        c2=c00
        #h1=(rd/(360))*(l-17)+21.5*1.5
        #c2.Placement=App.Placement(App.Vector(0,0,h1),App.Rotation(App.Vector(0,0,1),rd/2))
        #h1=math.tan(a/(57.3*n))*w1/2*(a/(n*57.3))
        h1=hs/2
        c2.Placement=App.Placement(App.Vector(0,0,h1),App.Rotation(App.Vector(0,0,1),rd/2))
        c1=c1.fuse(c2)
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)  
        obj.Shape=c1
        