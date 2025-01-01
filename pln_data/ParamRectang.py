from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part

class Rectang:
    def __init__(self, obj):
        self.Type = 'Rectang'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        B=App.ActiveDocument.getObject(label).B
        H=App.ActiveDocument.getObject(label).H
        p1=(0,0,0)
        p2=(0,H,0)
        p3=(B,H,0)
        p4=(B,0,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p1])
        if sface=='XZ':
            polygon.Placement=App.Placement(App.Vector(-B/2,0,-H/2),App.Rotation(App.Vector(1,0,0),90))
        elif sface=='YZ':
            polygon.Placement=App.Placement(App.Vector(-H/2,0,-B/2),App.Rotation(App.Vector(0,1,0),90))
        elif sface=='XY':
            polygon.Placement=App.Placement(App.Vector(-B/2,-H/2,0),App.Rotation(App.Vector(0,0,1),0))
        pface=Part.Face(polygon)
        c00=pface
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)    
        obj.Shape=c00