from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class Dharma:
    def __init__(self, obj):
        self.Type = 'Dharma'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        B=App.ActiveDocument.getObject(label).B  
        D=App.ActiveDocument.getObject(label).D
        d=App.ActiveDocument.getObject(label).d

        R=D/2
        r=d/2
        z=R-r
        a=math.atan(z/B)
        x1=R*math.sin(a)
        y1=R*math.cos(a)
        x2=r*math.sin(a)
        y2=r*math.cos(a)
        p1=(-R,0,0)
        p2=(x1,y1,0)
        p3=(B+x2,y2,0)
        p4=(B+r,0,0)
        p5=(B+x2,-y2,0)
        p6=(x1,-y1,0)
        edge1=Part.Arc(Base.Vector(p6),Base.Vector(p1),Base.Vector(p2)).toShape()
        edge2=Part.makeLine(p2,p3)
        edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge4=Part.makeLine(p5,p6)
        awire=Part.Wire([edge1,edge2,edge3,edge4])
        if sface=='XZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)      
        pface=Part.Face(awire)
        c00=pface 
        obj.Shape=c00
     