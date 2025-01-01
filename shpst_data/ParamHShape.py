import FreeCAD, Part, math
import FreeCADGui as Gui
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD, FreeCADGui
import FreeCAD as App
from FreeCAD import Base
from . import ShpstData
class HShape:
    def __init__(self, obj):
        self.Type = 'H_shape'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS_Wide':
            sa=ShpstData.H_ss_w[size]
        elif standard=='SS_Medium':
            sa=ShpstData.H_ss_m[size]
        elif standard=='SS_Thin':
            sa=ShpstData.H_ss_t[size]
        elif standard=='SUS':
            sa=ShpstData.H_sus[size]    

        H=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        t2=float(sa[3])
        r=float(sa[4])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        Solid=App.ActiveDocument.getObject(label).Solid
        
        x2=t1+2*r
        x1=(B-x2)/2
        y1=t2+r
        y2=(H-2*y1)
        x4=r/math.sqrt(2)
        x5=r*(1-1/math.sqrt(2))
        p1=(0,0,0)
        p2=(0,0,t2)
        p3=(x1,0,t2)
        p4=(x1+x4,0,t2+x5)
        p5=(x1+r,0,y1)
        p6=(x1+r,0,H-y1)
        p7=(x1+x4,0,H-(t2+x5))
        p8=(x1,0,H-t2)
        p9=(0,0,H-t2)
        p10=(0,0,H)
        p11=(B,0,H)
        p12=(B,0,H-t2)
        p13=(B-x1,0,H-t2)
        p14=(B-(x1+x4),0,H-(t2+x5))
        p15=(B-(x1+r),0,H-y1)
        p16=(B-(x1+r),0,y1)
        p17=(B-(x1+x4),0,y1-x4)
        p18=(B-x1,0,t2)
        p19=(B,0,t2)
        p20=(B,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.makeLine(p2,p3)
        edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge4=Part.makeLine(p5,p6)
        edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
        edge6=Part.makeLine(p8,p9)
        edge7=Part.makeLine(p9,p10)
        edge8=Part.makeLine(p10,p11)
        edge9=Part.makeLine(p11,p12)
        edge10=Part.makeLine(p12,p13)
        edge11=Part.Arc(Base.Vector(p13),Base.Vector(p14),Base.Vector(p15)).toShape()
        edge12=Part.makeLine(p15,p16)

        edge13=Part.Arc(Base.Vector(p16),Base.Vector(p17),Base.Vector(p18)).toShape()
        edge14=Part.makeLine(p18,p19)
        edge15=Part.makeLine(p19,p20)
        edge16=Part.makeLine(p20,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12,edge13,edge14,edge15,edge16])
        pface=Part.Face(awire)
        pface.translate(Base.Vector(-B/2,H/2,0))
        pface.rotate(Base.Vector(-B/2,H/2,0),Base.Vector(1,0,0),90)
        if Solid==True:
            #L=App.ActiveDocument.getObject(label).L
            c00=pface.extrude(Base.Vector(0,0,L))
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