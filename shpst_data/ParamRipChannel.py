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
class RipChannel:
    def __init__(self, obj):
        self.Type = 'Rip_channel'
        obj.Proxy = self
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.Rip_channel_ss[size]
        elif standard=='SUS':
            sa=ShpstData.Rip_channel_sus[size]
        H=float(sa[0])
        A=float(sa[1])
        C=float(sa[2])
        t=float(sa[3])
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
        p5=(A-r2,0,H)
        p6=(A-x4,0,H-x4)
        p7=(A,0,H-r2)
        p8=(A,0,H-C)
        p9=(A-t,0,H-C)
        p10=(A-t,0,H-r2)
        p11=(A-(t+x2),0,H-(t+x2))
        p12=(A-r2,0,H-t)
        p13=(r2,0,H-t)
        p14=(t+x2,0,H-(t+x2))
        p15=(t,0,H-r2)
        p16=(t,0,r2)
        p17=(t+x2,0,t+x2)
        p18=(r2,0,t)
        p19=(A-r2,0,t)
        p20=(A-t,0,r2)
        p21=(A-t,0,C)
        p22=(A,0,C)
        p23=(A,0,r2)
        p24=(A-x4,0,x4)
        p25=(A-r2,0,0)
        p26=(r2,0,0)
        p27=(x4,0,x4)
        p28=(A-(t+x2),0,t+x2)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p7)).toShape()
        edge5=Part.makeLine(p7,p8)
        edge6=Part.makeLine(p8,p9)
        edge7=Part.makeLine(p9,p10)
        edge8=Part.Arc(Base.Vector(p10),Base.Vector(p11),Base.Vector(p12)).toShape()
        edge9=Part.makeLine(p12,p13)
        edge10=Part.Arc(Base.Vector(p13),Base.Vector(p14),Base.Vector(p15)).toShape()
        edge11=Part.makeLine(p15,p16)
        edge12=Part.Arc(Base.Vector(p16),Base.Vector(p17),Base.Vector(p18)).toShape()
        edge13=Part.makeLine(p18,p19)
        edge14=Part.Arc(Base.Vector(p19),Base.Vector(p28),Base.Vector(p20)).toShape()
        edge15=Part.makeLine(p20,p21)
        edge16=Part.makeLine(p21,p22)
        edge17=Part.makeLine(p22,p23)
        edge18=Part.Arc(Base.Vector(p23),Base.Vector(p24),Base.Vector(p25)).toShape()
        edge19=Part.makeLine(p25,p26)
        edge20=Part.Arc(Base.Vector(p26),Base.Vector(p27),Base.Vector(p1)).toShape()
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12,edge13,edge14,edge15,edge16,edge17,edge18,edge19,edge20])
        pface=Part.Face(awire)
        if Solid==True:
            #L=App.ActiveDocument.getObject(label).L
            c00=pface.extrude(Base.Vector(0,L,0))
            obj.Shape=c00
            
        else:    
            c00=pface
        obj.size=size
        obj.A=A
        obj.H=H
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