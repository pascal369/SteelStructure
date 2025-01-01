from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class ChainCover:
    def __init__(self, obj):
        self.Type = 'Chaincover'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        B=App.ActiveDocument.getObject(label).B  
        D=App.ActiveDocument.getObject(label).D
        d=App.ActiveDocument.getObject(label).d
        h1=App.ActiveDocument.getObject(label).h1
        h2=App.ActiveDocument.getObject(label).h2
        H=h1-h2
        R=D/2
        r=d/2
        z=R-r
        c=math.atan(H/B)
        L=B/math.cos(c)
        k=math.asin(z/L)
        
        a=k+c
        b=(pi/2-a)/2
        #print(b*180/pi,k,L)
        
        x1=R*math.sin(a)
        y1=R*math.cos(a)
        x2=r*math.sin(a)
        y2=r*math.cos(a)
        x20=r*math.cos(b)
        y20=r*math.sin(b)
        
        p1=(-R,0,0)
        p2=(0,R,0)
        p3=(x1,y1,0)
        p4=(B+x2,y2-H,0)
        
        p5=(B+x20,y20-H,0)

        p6=(B+r,-H,0)
        p7=(B+r,-H-h2,0)
        p8=(-R,-h1,0)

        edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
        edge2=Part.makeLine(p3,p4)
        edge3=Part.Arc(Base.Vector(p4),Base.Vector(p5),Base.Vector(p6)).toShape()
        edge4=Part.makeLine(p6,p7)
        edge5=Part.makeLine(p7,p8)
        edge6=Part.makeLine(p8,p1)

        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
        if sface=='XZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        
        pface=Part.Face(awire)
        c00=pface 
        obj.Shape=c00
     