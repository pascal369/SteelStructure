from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ShpstData
class PipeShape:
    def __init__(self, obj):
        self.Type = 'Pipe_shape'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='STK':
            sa=ShpstData.STK_ss[size]
            D=float(sa[0])
            t=float(sa[1])
            #self.label_type.setText(QtGui.QApplication.translate("Dialog", str(D),None ))    
        elif standard=='SUS_Sch20S':
            sa=ShpstData.tubes[size]
            D=float(sa[0])
            t=float(sa[8])
        elif standard=='SUS_Sch40':
            sa=ShpstData.tubes[size]
            D=float(sa[0])
            t=float(sa[9])
        elif standard=='SGP':
            sa=ShpstData.tubes[size]
            D=float(sa[0])
            t=float(sa[11])    

        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        if Solid==True:
            c1 = Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c2 = Part.makeCylinder((D-2*t)/2,L,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c00=c1.cut(c2)
            obj.Shape=c00
        else:
            c1 = Part.makeCircle(D/2,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c2 = Part.makeCircle((D-2*t)/2,Base.Vector(0,0,0),Base.Vector(0,1,0))    
            c00=c1.fuse(c2)
        obj.size=size
        obj.D=D
        obj.t=t
        g=c00.Volume*g0/10**9 
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass    
        obj.Shape=c00