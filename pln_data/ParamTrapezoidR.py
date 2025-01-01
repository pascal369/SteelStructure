from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class TrapezoidR:
    def __init__(self, obj):
        self.Type = 'TrapezoidR'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H 
        B=App.ActiveDocument.getObject(label).B
        b1=App.ActiveDocument.getObject(label).b1
        h1=App.ActiveDocument.getObject(label).h1
        h2=App.ActiveDocument.getObject(label).h2
        p1=(0,0,0)
        p2=(-B/2,h2,0)  
        p3=(-b1/2,H-h1,0)
        p4=(0,H,0)
        p5=(b1/2,H-h1,0)
        p6=(B/2,h2,0)
        edge1=Part.makeLine(p2,p3)
        edge2=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge3=Part.makeLine(p5,p6)
        edge4=Part.Arc(Base.Vector(p6),Base.Vector(p1),Base.Vector(p2)).toShape()
        awire=Part.Wire([edge1,edge2,edge3,edge4])
        if sface=='XZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        pface=Part.Face(awire)
        c00=pface
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)    
        obj.Shape=c00
        