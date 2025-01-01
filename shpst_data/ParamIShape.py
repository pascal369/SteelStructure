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
class IShape:
    def __init__(self, obj):
        self.Type = 'I_shape'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.I_ss[size]
        H=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        t2=float(sa[3])
        r1=float(sa[4])
        r2=float(sa[5])
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        Solid=App.ActiveDocument.getObject(label).Solid
        x1=(B-t1)/2
        x2=x1/2
        s45=math.radians(45)
        s8=math.radians(8)
        x3=r2*math.cos(s45)
        x31=r1*math.cos(s45)
        x4=r2-x3
        x5=r1*math.cos(s45)
        x6=r1-x31
        y4=r2*math.sin(s8)
        x8=r1*math.sin(s8)
        x30=r2-y4
        x9=x1+t1+r1-x8
        x10=x1+t1+x6
        x7=x2-x31
        y3=x7*math.tan(s8)
        y6=t2-(r2+y3)
        y5=r2*math.cos(s8)
        x11=x1-(x30+r1-x8)
        x12=x11*math.tan(s8)
        y9=r1*math.cos(s8)
        y1=y6+r2+x12+y9
        y2=H-2*y1
        y8=y6+y5+x12
        p1=(0,0,0)
        p2=(0,0,y6)
        p3=(x4,0,y6+x3)
        p4=(x30,0,y6+y5)
        p5=(x1-r1+x8,0,y8)
        p6=(x1-x6,0,y1-x31)
        p7=(x1,0,y1)
        p8=(x1,0,y1+y2)
        p9=(x1-x6,0,y1+y2+x31)
        p10=(x1-r1+x8,0,H-y8)
        p11=(x30,0,H-(y6+y5))
        p12=(x4,0,H-(y6+x3))
        p13=(0,0,H-y6)
        p14=(0,0,H)
        p15=(B,0,H)
        p16=(B,0,H-y6)
        p17=(B-x4,0,H-(y6+x3))
        p18=(B-x30,0,H-(y6+y5))
        p19=(x9,0,H-y8)
        p20=(x10,0,y1+y2+x31)
        p21=(x1+t1,0,y1+y2)
        p22=(x1+t1,0,y1)
        p23=(x10,0,y1-x31)
        p24=(x9,0,y8)
        p25=(B-x30,0,y6+y5)
        p26=(B-x4,0,y6+x3)
        p27=(B,0,y6)
        p28=(B,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p7)).toShape()
        edge5=Part.makeLine(p7,p8)
        edge6=Part.Arc(Base.Vector(p8),Base.Vector(p9),Base.Vector(p10)).toShape()
        edge7=Part.makeLine(p10,p11)
        edge8=Part.Arc(Base.Vector(p11),Base.Vector(p12),Base.Vector(p13)).toShape()
        edge9=Part.makeLine(p13,p14)
        edge10=Part.makeLine(p14,p15)
        edge11=Part.makeLine(p15,p16)
        edge12=Part.Arc(Base.Vector(p16),Base.Vector(p17),Base.Vector(p18)).toShape()
        edge13=Part.makeLine(p18,p19)
        edge14=Part.Arc(Base.Vector(p19),Base.Vector(p20),Base.Vector(p21)).toShape()
        edge15=Part.makeLine(p21,p22)
        edge16=Part.Arc(Base.Vector(p22),Base.Vector(p23),Base.Vector(p24)).toShape()
        edge17=Part.makeLine(p24,p25)
        edge18=Part.Arc(Base.Vector(p25),Base.Vector(p26),Base.Vector(p27)).toShape()
        edge19=Part.makeLine(p27,p28)
        edge20=Part.makeLine(p28,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12,edge13,edge14,edge15,edge16,edge17,edge18,edge19,edge20])
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