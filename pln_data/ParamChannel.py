from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App

class Channel:
    def __init__(self, obj):
        self.Type = 'Channel'
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
        p3=(b2,H,0)
        p4=(b2,H-h1,0)
        p5=(b1,H-h1,0)
        p6=(b1,h2,0)
        p7=(B,h2,0)
        p8=(B,0,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p5,p6,p7,p8,p1])
        if sface=='XZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)

        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)    

        pface=Part.Face(polygon)
        c00=pface
        obj.Shape=c00
   