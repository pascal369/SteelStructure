from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class Trapezoid:
    def __init__(self, obj):
        self.Type = 'Trapezoid'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H 
        B=App.ActiveDocument.getObject(label).B
        b1=App.ActiveDocument.getObject(label).b1
        x=(B-b1)/2
        p1=(0,0,0)
        p2=(x,H,0)  
        p3=((x+b1),H,0)
        p4=(B,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.makeLine(p2,p3)
        edge3=Part.makeLine(p3,p4)
        edge4=Part.makeLine(p4,p1)
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
     