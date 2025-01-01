from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class D_Cut2:
    def __init__(self, obj):
        self.Type = 'D_Cut'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        H=App.ActiveDocument.getObject(label).H 
        B=App.ActiveDocument.getObject(label).B
        
        p1=(0,0,0)
        p2=(0,H,0)
        p3=(B/2,0.8*H,0)
        p4=(B,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p1,p4)
        awire=Part.Wire([edge1,edge2,edge3]) 
        if sface=='XZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
        elif sface=='YZ':
            awire.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)  
         
        pface=Part.Face(awire)
        c00=pface
        obj.Shape=c00
       