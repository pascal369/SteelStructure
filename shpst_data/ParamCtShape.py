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
class CtShape:
    def __init__(self, obj):
        self.Type = 'Ct_shape'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        sa=ShpstData.CT_ss[size]
        A=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        t2=float(sa[3])
        r=float(sa[4])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        s45=math.radians(45)
        x1=r*math.cos(s45)
        x2=r-x1
        x3=t2+r
        x4=A-x3
        x5=(B-t1)/2
        p1=(0,0,0)
        p2=(0,0,A-x3)
        p3=(-x2,0,A-x3+x1)
        p4=(-r,0,A-t2)
        p5=(-x5,0,A-t2)
        p6=(-x5,0,A)
        p7=(t1+x5,0,A)
        p8=(t1+x5,0,A-t2)
        p9=(t1+r,0,A-t2)
        p10=(t1+x2,0,A-(t2+x2))
        p11=(t1,0,A-x3)
        p12=(t1,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.makeLine(p5,p6)
        edge5=Part.makeLine(p6,p7)
        edge6=Part.makeLine(p7,p8)
        edge7=Part.makeLine(p8,p9)
        edge8=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
        edge9=Part.makeLine(p11,p12)
        edge10=Part.makeLine(p12,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10])
        pface=Part.Face(awire)
        if Solid==True:
            #L=App.ActiveDocument.getObject(label).L
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