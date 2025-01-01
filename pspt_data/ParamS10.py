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

class S10:
    def __init__(self, obj):
        self.Type = 'S10'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        global L1
        label=obj.Name
        #key=App.ActiveDocument.getObject(label).key
        #size_s=App.ActiveDocument.getObject(label).size1
        #size_c=App.ActiveDocument.getObject(label).size2

        Type=App.ActiveDocument.getObject(label).Type
        ShapedSteel=App.ActiveDocument.getObject(label).ShapedSteel

        L1=App.ActiveDocument.getObject(label).L1
        t=App.ActiveDocument.getObject(label).t
        H=App.ActiveDocument.getObject(label).H
        x=App.ActiveDocument.getObject(label).W
        Post=App.ActiveDocument.getObject(label).Post
        TopBeam=App.ActiveDocument.getObject(label).TopBeam
        #BasePlate=App.ActiveDocument.getObject(label).BasePlate
        #size2=App.ActiveDocument.getObject(label).size2
        def rib(self):
            global c00
            #w=float(sa[11])
            w=x
            #x0=float(sa[12])
            D=float(sa[0])
            w0=(w-D)/2
            #h=x0
            h=150
            p1=(0,0,0)
            p2=(0,0,20)
            p3=(w0-20,0,h)
            p4=(w0,0,h)
            p5=(w0,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p4,p5)
            edge5=Part.makeLine(p1,p5)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            pface=Part.Face(aWire)
            c00=pface.extrude(Base.Vector(0,6,0))
        def channel_10(self):
            global c00
            s0=5
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
            p2=(0,vy*H0,0)
            p3=(vx*B,vy*H0,0)
            p4=(vx*B,vy*(H0-y4),0)
            p5=(vx*(B-x1),vy*(H0-(y4+y1)),0)
            p6=(vx*(B-x30),vy*(H0-(y4+y2)),0)
            p7=(vx*(t1+x40),vy*(H0-y10),0)
            p8=(vx*(t1+x5),vy*(H0-y11),0)
            p9=(vx*t1,vy*(H0-y12),0)
            p10=(vx*t1,vy*y12,0)
            p11=(vx*(t1+x5),vy*y11,0)
            p12=(vx*(t1+x40),vy*y10,0)
            p13=(vx*(B-x30),vy*(y4+y2),0)
            p14=(vx*(B-x1),vy*(y4+y1),0)
            p15=(vx*B,vy*y4,0)
            p16=(vx*B,0,0)
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
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
            pface_c=Part.Face(aWire)
            c00=pface_c.extrude(Base.Vector(0,0,L))  
        L=L1
        vz=-1
        vx=1
        vy=1
        #print(size)
        sa=psuport_data.SGP[Post]
        D=sa[0]
        #print(D)
        t0=sa[1]
        #size2=sa[10]
        sa=psuport_data.channel_ss[TopBeam]  
        H0=sa[0]
        B=sa[1]
        t1=sa[2]
        t2=sa[3]
        r1=sa[4]
        r2=sa[5]
        Cy=sa[8]*10   
        channel_10(self)
        c01=c00
        c01.Placement=App.Placement(App.Vector(-B/2,L/2,H-H0-t),App.Rotation(App.Vector(1,0,0),90))
        H=H-H0-t
        c02=Part.makeCylinder(D/2,H,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c03=Part.makeCylinder((D-2*t0)/2,H,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c04=Part.makeCylinder((D)/2,6,Base.Vector(0,0,H-6),Base.Vector(0,0,1),360) 
        #Part.show(c04)
        c02=c02.cut(c03)
        #c02=c02.cut(c01)
        c1=c01
        c1=c1.fuse(c02)
        c1=c1.fuse(c04)
        obj.Shape=c1
        sa=psuport_data.SGP[Post]
        #w=sa[11]
        w=x
        pface=Part.makePlane(x,x)
        c01=pface.extrude(Base.Vector(0,0,t))
        c01.Placement=App.Placement(App.Vector(-x/2,-x/2,-t),App.Rotation(App.Vector(0,0,1),0))
        c1=c1.fuse(c01)
       
        for i in range(4):
            rib(self)
            c01=c00
            if i==0:
                x0=-w/2
                y0=-3
                k=0
            elif i==1:
                x0=-3
                y0=w/2
                k=-90
            elif i==2:
                x0=w/2
                y0=3
                k=180
            elif i==3:
                x0=3
                y0=-w/2
                k=90

            c01.Placement=App.Placement(App.Vector(x0,y0,0),App.Rotation(App.Vector(0,0,1),k))
            c1=c1.fuse(c01)
            c1=c1.removeSplitter()
            
            g=c1.Volume*7850/10**9 
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
        
            