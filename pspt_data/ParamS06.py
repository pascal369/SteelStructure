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
class S06:
    def __init__(self, obj):
        self.Type = 'S06'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        global H1
        label=obj.Name
        #key=App.ActiveDocument.getObject(label).key
        #key1=App.ActiveDocument.getObject(label).key1
        
        Type=App.ActiveDocument.getObject(label).Type
        ShapedSteel=App.ActiveDocument.getObject(label).ShapedSteel
        if ShapedSteel=='Angle':
            key1=0
        else:
            key1=1

        L1=App.ActiveDocument.getObject(label).L1
        t0=App.ActiveDocument.getObject(label).t0
        BasePlate=App.ActiveDocument.getObject(label).BasePlate
        H=App.ActiveDocument.getObject(label).H
        x=App.ActiveDocument.getObject(label).W
        y=App.ActiveDocument.getObject(label).B
        size=App.ActiveDocument.getObject(label).size

        if Type=='s07':
            H1=App.ActiveDocument.getObject(label).H1
        def angle(self):
            global c00
            if Type=='s07':
                H1=App.ActiveDocument.getObject(label).H1
            x1=r2*(1-1/math.sqrt(2))
            x2=r2-x1
            y1=r1*(1-1/math.sqrt(2))
            y2=r1-y1
            y3=A-(r2+r1+t)
            x=t-r2
            p1=(0,0,0)
            p2=(0,vy*A,0)
            p3=(vx*x,vy*A,0)
            p4=(vx*(t-x1),vy*(A-x1),0)
            p5=(vx*t,vy*(A-r2),0)
            p6=(vx*t,vy*(A-(r2+y3)),0)
            p7=(vx*(t+y1),vy*(t+y1),0)
            p8=(vx*(t+r1),vy*t,0)
            p9=(vx*(B-r2),vy*t,0)
            p10=(vx*(B-x1),vy*(t-x1),0)
            p11=(vx*B,vy*(t-r2),0)
            p12=(vx*B,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            edge6=Part.makeLine(p8,p9)
            edge7=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9])
            pface_a=Part.Face(aWire)
            c00=pface_a.extrude(Base.Vector(0,0,L))
        def angle_bp(self): 
            global c00
            #global W
            x=App.ActiveDocument.getObject(label).W
            #global A
            #A=App.ActiveDocument.getObject(label).A
            #B=A+20
            x0=1
            #W=x0*A+10+4*d
            p1=(0,0,0)
            p2=(0,y,0)
            p3=(x,y,0)
            p4=(x,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p4,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c00=pface.extrude(Base.Vector(0,0,t0))
            '''
            cylinder = Part.makeCylinder(d/2,t0,Base.Vector(2*d,B/2,0),Base.Vector(0,0,1))
            c00=c00.cut(cylinder)
            cylinder = Part.makeCylinder(d/2,t0,Base.Vector(W-2*d,B/2,0),Base.Vector(0,0,1))
            c00=c00.cut(cylinder)
            '''
        def cutter(self):
            global c00
            p1=(0,0,0)
            p2=(vx*w0,0,0)
            p3=(vx*w0,0,-vz*h0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p1)
            aWire=Part.Wire([edge1,edge2,edge3])
            pface=Part.Face(aWire)
            c00=pface.extrude(Base.Vector(0,L,0))  
        if key1==0:#アングル   
            sa=psuport_data.angle_ss_equal[size]  
            A=sa[0]
            B=sa[1]
            t=sa[2]
            r1=sa[3]
            r2=sa[4]       
            #柱L
            vx=1
            vy=1
            L=H
            angle(self)
            c1=c00
            vz=1
            L=A
            w0=A
            h0=A
            L=A
            cutter(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,H),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.cut(c01)
            #柱R
            vx=-1
            vy=1
            L=H
            angle(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(1,0,0),0))
            vx=-1
            w0=A
            h0=A
            L=A
            cutter(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(L1,0,H),App.Rotation(App.Vector(0,0,1),0))
            c01=c01.cut(c02)
            c1=c1.fuse(c01)
            #梁
            vx=-1
            vy=1
            L=L1
            angle(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L1,0,H),App.Rotation(App.Vector(0,1,0),-90))
            #カッターL
            vx=-1
            vz=-1
            L=A
            w0=A
            h0=A
            L=A
            cutter(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(w0,0,H-h0),App.Rotation(App.Vector(0,0,1),0))
            c01=c01.cut(c02)
            #カッターR
            vx=1
            vz=-1
            L=A
            w0=A
            h0=A
            L=A
            cutter(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(L1-w0,0,H-h0),App.Rotation(App.Vector(0,0,1),0))
            c01=c01.cut(c02)
            c1=c1.fuse(c01)
            c1=c1.removeSplitter() 
            #ベースプレートL
            if BasePlate==True:
                angle_bp(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(-x+A+10,-(y-A)/2,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                #ベースプレートR
                angle_bp(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(L1-(A+10),-(y-A)/2,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
            c1.Placement=App.Placement(App.Vector(-L1/2,0,0),App.Rotation(App.Vector(0,0,1),0))  
            c1=c1.removeSplitter()  
            obj.Shape=c1#s06
            if Type=='s07':
                vx=-1
                vy=1
                L=L1
                angle(self)#梁
                c01=c00
                H1=App.ActiveDocument.getObject(label).H1
                c01.Placement=App.Placement(App.Vector(L1/2,0,H-H1),App.Rotation(App.Vector(0,1,0),-90))
                
                c1=c1.fuse(c01)
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))  
                c1=c1.removeSplitter()

            obj.Shape=c1
        
        elif key1==1: 
            def channel(self):
                global c00
                global pface_c
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
            def channel2(self):
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
                #print(y4)
                y10=y4+y2+y6
                y11=y4+y2+y6+x5
                y12=y4+y2+y6+x5+x4
                p1=(0,0,0)
                p2=(vy*H0,0,0)
                p3=(vy*H0,vx*B,0)
                p4=(vy*(H0-y4),vx*B,0)
                p5=(vy*(H0-(y4+y1)),vx*(B-x1),0)
                p6=(vy*(H0-(y4+y2)),vx*(B-x30),0)
                p7=(vy*(H0-y10),vx*(t1+x40),0)
                p8=(vy*(H0-y11),vx*(t1+x5),0)
                p9=(vy*(H0-y12),vx*t1,0)
                p10=(vy*y12,vx*t1,0)
                p11=(vy*y11,vx*(t1+x5),0)
                p12=(vy*y10,vx*(t1+x40),0)
                p13=(vy*(y4+y2),vx*(B-x30),0)
                p14=(vy*(y4+y1),vx*(B-x1),0)
                p15=(vy*y4,vx*B,0)
                p16=(0,vx*B,0)
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
                pface=Part.Face(aWire)
                c00=pface.extrude(Base.Vector(0,0,L))
            def channel_bp(self):
                global c00
                global W
                x0=1
                #W=x0*H0+8*d
                #B1=B+20
                pface=Part.makePlane(x,y)
                c00=pface.extrude(Base.Vector(0,0,t1))
                '''
                for i in range(4):
                    if i==0:
                        x=2*d
                        y=1.5*d
                    elif i==1:
                        x=W-2*d
                        y=1.5*d
                    elif i==2:
                        x=2*d
                        y=B1-1.5*d
                    elif i==3:
                        x=W-2*d
                        y=B1-1.5*d
                    c01=Part.makeCylinder(d/2,t0,Base.Vector(x,y,0),Base.Vector(0,0,1),360)
                    c00=c00.cut(c01) 
                '''    
            def rib_channel(self):
                global c00
                global pface_c
                #H=float(PSuport.sa[0])
                #B=float(PSuport.sa[1])
                #t1=float(PSuport.sa[2])
                channel(self)
                pface1=pface_c
                pface2=Part.makePlane(H0,B)
                c01=pface1.extrude(Base.Vector(0,0,t1))
                c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
                c02=pface2.extrude(Base.Vector(0,0,t1))
                c00=c02.cut(c01)  
            sa=psuport_data.channel_ss[size]  
            H0=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]
            r1=sa[4]
            r2=sa[5]
            Cy=sa[8]*10              
            vx=-1
            vy=1
            L=H
            #柱L
            channel(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-90))
            #柱R
            L=H
            channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L1-H0,0,0),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c01)
            #梁
            t=t2
            L=L1-2*H0
            vx=1
            vy=-1
            channel2(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L1-H0,0,H),App.Rotation(App.Vector(0,1,0),-90))
            c1=c1.fuse(c01)
            c1.Placement=App.Placement(App.Vector(-(L+2*H0)/2,0,0),App.Rotation(App.Vector(0,0,1),0))  
            c1=c1.removeSplitter()
            if Type=='s07':#s07
                H1=App.ActiveDocument.getObject(label).H1
                L=L1-2*H0
                vx=1
                vy=-1
                channel2(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(L1-H0-L1/2,0,H+t-H1),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.fuse(c01)
            #ベースプレート
            if BasePlate==True:
                channel_bp(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(-(x-H0)/2-L1/2,-(y-B)/2,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                channel_bp(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(-(x-H0)/2+L1-H0-L1/2,-(y-B)/2,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01) 

            #リブ
            #L上
            rib_channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(H0,0,H-t1),App.Rotation(App.Vector(0,0,1),0))
            #Part.show(c01)
            c1=c1.fuse(c01)
            
            rib_channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(H0,0,H-H0),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            c1=c1.removeSplitter()
            
            #R上
            rib_channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-L1/2,0,H-t1),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            rib_channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-L1/2,0,H-H0),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            c1=c1.removeSplitter()
            if Type=='s07':
                #リブ
                #L上
                rib_channel(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(H0,0,H-H1),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                rib_channel(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(H0,0,H-H1-H0+t1),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                #R上
                rib_channel(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(-L1+H0+H0,0,H-H1),App.Rotation(App.Vector(0,0,1),0))
                #Part.show(c01)
                c1=c1.fuse(c01)
                rib_channel(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(-L1+H0+H0,0,H-H1-H0+t1),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                #Part.show(c01)
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))  
                c1=c1.removeSplitter()
                
        #c1.Placement=App.Placement(App.Vector(-L,0,0),App.Rotation(App.Vector(0,0,1),0))  
        #c1=c1.removeSplitter()          
        obj.Shape=c1
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
        