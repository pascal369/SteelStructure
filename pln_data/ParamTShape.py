from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class TShape:
    def __init__(self, obj):
        self.Type = 'TShape'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H
        B=App.ActiveDocument.getObject(label).B
        b1=App.ActiveDocument.getObject(label).b1
        h1=App.ActiveDocument.getObject(label).h1
        p1=(-b1/2,0,0)
        p2=(-b1/2,H-h1,0)
        p3=(-B/2,H-h1,0)
        p4=(-B/2,H,0)
        p5=(B/2,H,0)
        p6=(B/2,H-h1,0)
        p7=(b1/2,H-h1,0)
        p8=(b1/2,0,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p5,p6,p7,p8,p1])
        if sface=='XZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        pface=Part.Face(polygon)
        c00=pface
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)    
        obj.Shape=c00
    