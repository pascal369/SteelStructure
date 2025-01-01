from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import psuport_data
class S05:
    def __init__(self, obj):
        self.Type = 'S05'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        #key=App.ActiveDocument.getObject(label).key
        H1=App.ActiveDocument.getObject(label).H1
        t=App.ActiveDocument.getObject(label).t
        d1=App.ActiveDocument.getObject(label).d1
        #BasePlate=App.ActiveDocument.getObject(label).BasePlate
        w=40
        h=120
        c01=Part.makeBox(w,h,t)
        c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),-90))
        c02=Part.makeBox(w,h,t)
        c02.Placement=App.Placement(App.Vector(0,0,H1-120),App.Rotation(App.Vector(1,0,0),-90))

        c01=c01.fuse(c02)
        c02=Part.makeCylinder(d1/2,H1-160,Base.Vector(w/2,-d1/2,-40),Base.Vector(0,0,1),360)
        c01=c01.fuse(c02)
        c1=c01
        #print(c1.Volume)
        g=-c1.Volume*7850/10**9 
        label='mass[kg]'
        try:
            #obj.addProperty("App::PropertyFloat", "body",label)
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass    
        obj.Shape=c1 