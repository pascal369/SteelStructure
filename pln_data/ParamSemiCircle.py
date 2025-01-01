from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part

class SemiCircle:
    def __init__(self, obj):
        self.Type = 'SemiCircle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        p1=(-D/2,0,0)
        p2=(0,D/2,0)
        p3=(D/2,0,0)
        edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
        edge2=Part.makeLine(p1,p3)
        awire=Part.Wire([edge1,edge2])
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