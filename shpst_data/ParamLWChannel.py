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
class LWChannel:
    def __init__(self, obj):
        self.Type = 'LW_channel'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.LW_channel_ss[size]
        elif standard=='SUS':
            sa=ShpstData.LW_channel_sus[size]
        H=float(sa[0])
        B=float(sa[1])
        t=float(sa[2])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        r2=2*t
        x1=t/math.sqrt(2)
        x2=t-x1
        x3=r2/math.sqrt(2)
        x4=r2-x3

        p1=(0,0,r2)
        p2=(0,0,H-r2)
        p3=(x4,0,H-x4)
        p4=(r2,0,H)
        p5=(B,0,H)
        p6=(B,0,H-t)
        p7=(r2,0,H-t)
        p8=(t+x2,0,H-(t+x2))
        p9=(t,0,H-r2)
        p10=(t,0,r2)
        p11=(t+x2,0,t+x2)
        p12=(r2,0,t)
        p13=(B,0,t)
        p14=(B,0,0)
        p15=(r2,0,0)
        p16=(x4,0,x4)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.makeLine(p5,p6)
        edge5=Part.makeLine(p6,p7)
        edge6=Part.Arc(Base.Vector(p7),Base.Vector(p8),Base.Vector(p9)).toShape()
        edge7=Part.makeLine(p9,p10)
        edge8=Part.Arc(Base.Vector(p10),Base.Vector(p11),Base.Vector(p12)).toShape()
        edge9=Part.makeLine(p12,p13)
        edge10=Part.makeLine(p13,p14)
        edge11=Part.makeLine(p14,p15)
        edge12=Part.Arc(Base.Vector(p15),Base.Vector(p16),Base.Vector(p1)).toShape()
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
        pface=Part.Face(awire)
        if Solid==True:
            #L=App.ActiveDocument.getObject(label).L
            c00=pface.extrude(Base.Vector(0,L,0))
            obj.Shape=c00
        else:    
            c00=pface
        obj.size=size
        obj.H=H
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