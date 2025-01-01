from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import FreeCADGui as Gui
class Circle:
    def __init__(self, obj):
        self.Type = 'Circle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        c1=Part.makeCircle(D/2,Base.Vector(0,0,0))
        if sface=='XZ':
            c1=Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(0,1,0))
        if sface=='YZ':
            c1=Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(1,0,0))

        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)      
        obj.Shape=c1    


        