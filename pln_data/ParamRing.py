from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part

class Ring:
    def __init__(self, obj):
        self.Type = 'Ring'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        d=App.ActiveDocument.getObject(label).d
        if sface=='XZ':
            c01=Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c02=Part.makeCircle(d/2,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c00=c01.fuse(c02)
        elif sface=='YZ':
            c01=Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c02=Part.makeCircle(d/2,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c00=c01.fuse(c02)
        else:
            c01=Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c02=Part.makeCircle(d/2,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c00=c01.fuse(c02)   
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)        
        obj.Shape=c00
