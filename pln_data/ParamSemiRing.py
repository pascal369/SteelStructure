from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part

class SemiRing:
    def __init__(self, obj):
        self.Type = 'Ring'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        d=App.ActiveDocument.getObject(label).d
        p1=(-D/2,0,0)
        p2=(0,D/2,0)
        p3=(D/2,0,0)
        p4=(d/2,0,0)
        p5=(-d/2,0,0)
        p6=(0,d/2,0)
        edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
        edge2=Part.makeLine(p3,p4)
        edge3=Part.Arc(Base.Vector(p4),Base.Vector(p6),Base.Vector(p5)).toShape()
        edge4=Part.makeLine(p5,p1)
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