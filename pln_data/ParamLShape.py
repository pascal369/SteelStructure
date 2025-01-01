from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class LShape:
    def __init__(self, obj):
        self.Type = 'LShape'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H
        B=App.ActiveDocument.getObject(label).B
        b1=App.ActiveDocument.getObject(label).b1
        h1=App.ActiveDocument.getObject(label).h1
        p1=(0,0,0)
        p2=(0,H,0)
        p3=(b1,H,0)
        p4=(b1,h1,0)
        p5=(B,h1,0)
        p6=(B,0,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p5,p6,p1])
        if sface=='XZ':
            polygon.Placement=App.Placement(App.Vector(-B/2,0,-H/2),App.Rotation(App.Vector(1,0,0),0))
            #polygon.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            polygon.Placement=App.Placement(App.Vector(0,-B/2,-H/2),App.Rotation(App.Vector(0,1,0),0))
            #polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        elif sface=='XY':
            polygon.Placement=App.Placement(App.Vector(-B/2,-H/2,0),App.Rotation(App.Vector(0,0,1),0))
            #polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)  

        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)     
        pface=Part.Face(polygon)
        c00=pface
        obj.Shape=c00
