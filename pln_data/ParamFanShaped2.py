from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class FanShaped2:
    def __init__(self, obj):
        self.Type = 'FanShaped2'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D  
        d=App.ActiveDocument.getObject(label).d
        st=App.ActiveDocument.getObject(label).st
        a=(180-st)/2
        a0=math.radians(a)
        x1=d/2*math.cos(a0)
        x2=D/2*math.cos(a0)
        y1=d/2*math.sin(a0)
        y2=D/2*math.sin(a0)
        p1=(-x1,y1,0)
        p2=(-x2,y2,0)
        p3=(0,D/2,0)
        p4=(x2,y2,0)
        p5=(x1,y1,0)
        p6=(0,d/2,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p1)).toShape()
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
      