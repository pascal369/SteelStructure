from FreeCAD import Base
import FreeCADGui as Gui
#import pyautogui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ShpstData
class Angle:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        #App.activeDocument().recompute(None,True,True)
        return
    def execute(self, obj):
        label=obj.Name
        size=App.ActiveDocument.getObject(label).size
        standard=App.ActiveDocument.getObject(label).standard
        Solid=App.ActiveDocument.getObject(label).Solid
        g0=App.ActiveDocument.getObject(label).g0*1000
        if standard=='SS_Equal':
            sa=ShpstData.angle_ss_equal[size]
        elif standard=='SS_Unequal':
            sa=ShpstData.angle_ss_unequal[size]
        elif standard=='SUS_Equal':
            sa=ShpstData.angle_sus_equal[size]    
               
        A=float(sa[0])
        B=float(sa[1])
        t=float(sa[2])
        r1=float(sa[3])
        r2=float(sa[4])
        cx=float(sa[7])*10
        cy=float(sa[8])*10

        L=App.ActiveDocument.getObject(label).L
        L=float(L)
        x1=r2*(1-1/math.sqrt(2))
        x2=r2-x1
        y1=r1*(1-1/math.sqrt(2))
        y2=r1-y1
        y3=A-(r2+r1+t)
        x=t-r2
        p1=(0,0,0)
        p2=(0,0,A)
        p3=(x,0,A)
        p4=(t-x1,0,A-x1)
        p5=(t,0,A-r2)
        p6=(t,0,A-(r2+y3))
        p7=(t+y1,0,t+y1)
        p8=(t+r1,0,t)
        p9=(B-r2,0,t)
        p10=(B-x1,0,t-x1)
        p11=(B,0,t-r2)
        p12=(B,0,0)

        edge1=Part.makeLine(p1,p2)
        edge2=Part.makeLine(p2,p3)
        edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge4=Part.makeLine(p5,p6)
        edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
        edge6=Part.makeLine(p8,p9)
        edge7=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
        edge8=Part.makeLine(p11,p12)
        edge9=Part.makeLine(p12,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9])
        pface=Part.Face(awire)

        pface.translate(Base.Vector(-A/2,A/2,0))
        pface.rotate(Base.Vector(-A/2,A/2,0),Base.Vector(1,0,0),90)
        if Solid==True:
            c00=pface.extrude(Base.Vector(0,0,L))
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
       
