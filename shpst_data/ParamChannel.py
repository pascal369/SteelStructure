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
class Channel:
    def __init__(self, obj):
        self.Type = 'Channel'
        obj.Proxy = self
        return
    def execute(self,obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        #H=App.ActiveDocument.getObject(label).H
        #B=App.ActiveDocument.getObject(label).B
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS':
            sa=ShpstData.channel_ss[size]
            s0=5
            t2=float(sa[3])
        elif standard=='SUS':
            sa=ShpstData.channel_sus[size]
            s0=0
            t2=float(sa[2])
        H=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        #t2=float(sa[3])
        r1=float(sa[4])
        r2=float(sa[5])
        Cy=float(sa[8])*10
        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        Solid=App.ActiveDocument.getObject(label).Solid
        s5=math.radians(s0)
        s45=math.radians(45)
        y1=r2*math.cos(s45)
        y2=r2*math.cos(s5)
        y3=r1*math.cos(s5)
        x1=r2*(1-math.cos(s45))
        x2=r2*math.sin(s5)
        x30=r2-x2
        x3=r1*math.sin(s5)
        x4=r1*math.cos(s45)
        x5=r1-x4
        x40=r1+x3
        x6=B-(x30+x40+t1)
        y6=x6*math.tan(s5)
        x7=Cy-(t1+x40)
        x8=x6-x7
        y7=x8*math.tan(s5)
        y8=t2-y7
        y4=y8-y2
        y10=y4+y2+y6
        y11=y4+y2+y6+x5
        y12=y4+y2+y6+x5+x4
        p1=(0,0,0)
        p2=(0,0,H)
        p3=(B,0,H)
        p4=(B,0,H-y4)
        p5=(B-x1,0,H-(y4+y1))
        p6=(B-x30,0,H-(y4+y2))
        p7=(t1+x40,0,H-y10)
        p8=(t1+x5,0,H-y11)
        p9=(t1,0,H-y12)
        p10=(t1,0,y12)
        p11=(t1+x5,0,y11)
        p12=(t1+x40,0,y10)
        p13=(B-x30,0,y4+y2)
        p14=(B-x1,0,y4+y1)
        p15=(B,0,y4)
        p16=(B,0,0)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.makeLine(p2,p3)
        edge3=Part.makeLine(p3,p4)
        edge4=Part.Arc(Base.Vector(p4),Base.Vector(p5),Base.Vector(p6)).toShape()
        edge5=Part.makeLine(p6,p7)
        edge6=Part.Arc(Base.Vector(p7),Base.Vector(p8),Base.Vector(p9)).toShape()
        edge7=Part.makeLine(p9,p10)
        edge8=Part.Arc(Base.Vector(p10),Base.Vector(p11),Base.Vector(p12)).toShape()
        edge9=Part.makeLine(p12,p13)
        edge10=Part.Arc(Base.Vector(p13),Base.Vector(p14),Base.Vector(p15)).toShape()
        edge11=Part.makeLine(p15,p16)
        edge12=Part.makeLine(p16,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
        pface=Part.Face(awire)
        #Part.show(pface)
        if Solid==True:
            pface.translate(Base.Vector(-B/2,0,-H/2))
            c00=pface.extrude(Base.Vector(0,L,0))
            g=c00.Volume*g0/10**9 
            label='mass[kg]'
            obj.Shape=c00
        else:  
            pface.translate(Base.Vector(-B/2,0,-H/2)) 
            c00=pface
            obj.Shape=c00
            
        
        obj.size=size
        obj.H=H
        obj.B=B
        
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            #obj.mass=g
            #obj.ViewObject.Proxy=0
            pass    
        #obj.Shape=c00
       
   