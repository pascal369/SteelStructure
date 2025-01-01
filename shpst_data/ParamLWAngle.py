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
class LWAngle:
    def __init__(self, obj):
        self.Type = 'LW_angle'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.LW_angle_ss[size]
        elif standard=='SUS':
            sa=ShpstData.LW_angle_sus[size]
        A=float(sa[0])
        B=float(sa[1])
        t=float(sa[2])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        r1=t
        r2=2*t
        x1=r1/math.sqrt(2)
        x2=r1-x1
        x3=r2/math.sqrt(2)
        x4=r2-x3
        p1=(0,0,r2)
        p2=(0,0,A)
        p3=(t,0,A)
        p4=(t,0,r2)
        p5=(t+x2,0,t+x2)
        p6=(r2,0,t)
        p7=(B,0,t)
        p8=(B,0,0)
        p9=(r2,0,0)
        p10=(x4,0,x4)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.makeLine(p2,p3)
        edge3=Part.makeLine(p3,p4)
        edge4=Part.Arc(Base.Vector(p4),Base.Vector(p5),Base.Vector(p6)).toShape()
        edge5=Part.makeLine(p6,p7)
        edge6=Part.makeLine(p7,p8)
        edge7=Part.makeLine(p8,p9)
        edge8=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p1)).toShape()
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
        pface=Part.Face(awire)
        if Solid==True:
            c00=pface.extrude(Base.Vector(0,L,0))
            obj.Shape=c00
        else:    
            c00=pface
        obj.size=size
        obj.A=A
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