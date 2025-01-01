from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part

class Quadrant:
    def __init__(self, obj):
        self.Type = 'Quadrant'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        p1=(0,0,0)
        p2=(0,D/2,0)
        p3=(D/2,0,0)
        p4=(D/(2*math.sqrt(2)),D/(2*math.sqrt(2)),0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p4),Base.Vector(p3)).toShape()
        edge3=Part.makeLine(p1,p3)
        awire=Part.Wire([edge1,edge2,edge3])

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
      