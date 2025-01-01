from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class Frame:
    def __init__(self, obj):
        self.Type = 'Frame'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H 
        B=App.ActiveDocument.getObject(label).B
        b1=App.ActiveDocument.getObject(label).b1
        b2=App.ActiveDocument.getObject(label).b2
        h1=App.ActiveDocument.getObject(label).h1
        h2=App.ActiveDocument.getObject(label).h2
        p1=(0,0,0)
        p2=(0,H,0)
        p3=(B,H,0)
        p4=(B,0,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p1])
        if sface=='XZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        pface=Part.Face(polygon)
        c01=pface

        p1=(b1,h2,0)
        p2=(b1,H-h1,0)
        p3=(B-b2,H-h1,0)
        p4=(B-b2,h2,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p1])
        if sface=='XZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        pface=Part.Face(polygon)
        c02=pface
        c00=c01.cut(c02)
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)  
        obj.Shape=c00
 