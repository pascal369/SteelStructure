from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD, FreeCADGui
import FreeCAD as App
from . import ShpstData
class FlatShape:
    def __init__(self, obj):
        self.Type = 'Flat_shape'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.flat_ss[size]
        elif standard=='SUS':
            sa=ShpstData.flat_sus[size]
        t=float(sa[0])
        B=float(sa[1])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        p1=(0,0,0)
        p2=(0,0,t)
        p3=(B,0,t)
        p4=(B,0,0)
        awire=Part.makePolygon([p1,p2,p3,p4,p1])
        pface=Part.Face(awire)
        if Solid==True:
            #L=App.ActiveDocument.getObject(label).L
            c00=pface.extrude(Base.Vector(0,L,0))
        obj.size=size
        obj.t=t
        obj.B=B     
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