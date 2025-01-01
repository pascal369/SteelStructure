from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
import Part
class BasePlate:
    def __init__(self, obj):
        self.Type = 'BasePlate'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        sface=App.ActiveDocument.getObject(label).sface
        D=App.ActiveDocument.getObject(label).D
        H=App.ActiveDocument.getObject(label).H
        B=App.ActiveDocument.getObject(label).B 
        b1=App.ActiveDocument.getObject(label).b1
        h1=App.ActiveDocument.getObject(label).h1 
        p1=(-B/2,-H/2,0)
        p2=(-B/2,H/2,0)
        p3=(B/2,H/2,0)
        p4=(B/2,-H/2,0)
        #p5=(b1,h1,0)
        polygon=Part.makePolygon([p1,p2,p3,p4,p1])
        c00=polygon

        if sface=='XY':
            c00.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
        elif sface=='YZ':
            c00.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)

        for i in range(4):
            if i==0:
                x=b1
                y=h1
            elif i==1:
                x=b1
                y=H-h1
            elif i==2: 
                x=B-b1
                y=H-h1
            elif i==3:
                x=B-b1
                y=h1          
            try:
                if sface=='XY':
                    c02=Part.makeCircle(D/2,Base.Vector(x-B/2,y-H/2,0),Base.Vector(0,0,1))
                    c00=c00.fuse(c02)
                elif sface=='XZ':
                    c02=Part.makeCircle(D/2,Base.Vector(x-B/2,0,y-H/2),Base.Vector(0,1,0))
                    c00=c00.fuse(c02)
                elif sface=='YZ':
                    c02=Part.makeCircle(D/2,Base.Vector(0-B/2,x-H/2,y),Base.Vector(1,0,0))
                    c00=c00.fuse(c02)
            except:
                pass

        obj.Shape=c00
     