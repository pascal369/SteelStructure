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

class S04:
    def __init__(self, obj):
        self.Type = 'S04'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        global t0
        label=obj.Name

        Type=App.ActiveDocument.getObject(label).Type
        ShapedSteel=App.ActiveDocument.getObject(label).ShapedSteel
        #print(ShapedSteel)
        if ShapedSteel=='Angle':
            key1=0
        else:
            key1=1
            t0=App.ActiveDocument.getObject(label).t0

        L1=App.ActiveDocument.getObject(label).L1
        
        BasePlate=App.ActiveDocument.getObject(label).BasePlate
        k=App.ActiveDocument.getObject(label).k
        size=App.ActiveDocument.getObject(label).size

        def angle(self):
            global c00
            global pface_a
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
            c00=pface_a.extrude(Base.Vector(0,0,L+t))
        def angle_bp(self): 
            global c00
            global W
            global B
            B=A+20
            W=x0*A+10+50
            p1=(0,0,0)
            p2=(0,B,0)
            p3=(W,B,0)
            p4=(W,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p4,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c00=pface.extrude(Base.Vector(0,0,t0))
            
        if key1==0:#アングル 
            sa=psuport_data.angle_ss_equal[size]  
            A=sa[0]
            B=sa[1]
            t=sa[2]
            r1=sa[3]
            r2=sa[4]       

            L=L1-t
            vx=-1
            vy=1
            #主材
            angle(self)
            c01=c00
            #A=App.ActiveDocument.getObject(label).A
            c01.Placement=App.Placement(App.Vector(L+t,0,A),App.Rotation(App.Vector(0,1,0),-90))
            c1=c01
            L=math.sqrt(2)*L1
            #斜材
            if k==45:
                L=L1*1.4142
            else:
                L=L1*2.0/1.732  
            angle(self)
            c01=c00
            if k==45:
                c01.Placement=App.Placement(App.Vector(-t,0,-L1),App.Rotation(App.Vector(0,1,0),90-k))
            else:
                c01.Placement=App.Placement(App.Vector(-t,0,-L1/1.732),App.Rotation(App.Vector(0,1,0),90-k))
            pface=Part.makePlane(2.0*A,2.0*A,Base.Vector(L1-t-2.0*A,0,0), Base.Vector(0,1,0))
            c02=pface.extrude(Base.Vector(0,A,0))
            c01=c01.cut(c02)
            if k==45:
                pface=Part.makePlane(3*A,2*A,Base.Vector(-2*A,0,-L1-2*t), Base.Vector(0,1,0))
            else:
                pface=Part.makePlane(3*A,2*A,Base.Vector(-2*A,0,-L1/1.732-2*t), Base.Vector(0,1,0))
            c02=pface.extrude(Base.Vector(0,A,0))
            c01=c01.cut(c02)
            c1=c1.fuse(c01)
            '''
            x0=1
            if BasePlate==True:
                angle_bp(self)#ベースプレート上
                c01=c00
                c01.Placement=App.Placement(App.Vector(0,-10,-(W-A)/2),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.fuse(c01)
                x0=1.5
                angle_bp(self)#ベースプレート下
                c01=c00
                if k==45:
                    c01.Placement=App.Placement(App.Vector(0,-10,-30-L1),App.Rotation(App.Vector(0,1,0),-90))
                else:
                    c01.Placement=App.Placement(App.Vector(0,-10,-30-L1/1.732),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.fuse(c01)

            pface=Part.makePlane(A,A,Base.Vector(L1-t,A,0), Base.Vector(1,0,0))
            c01=pface.extrude(Base.Vector(-t0,0,0))
            c1=c1.fuse(c01)
            c1=c1.removeSplitter()  
            '''
            angle(self)
            pface=pface_a
            pface.Placement=App.Placement(App.Vector(0,0,A),App.Rotation(App.Vector(0,0,1),-90))
            k0=math.radians(k)
            H=L1*math.tan(k0)
            c01=pface.extrude(Base.Vector(0,0,-H))
            c1=c1.fuse(c01)
            c1.Placement=App.Placement(App.Vector(0,0,-A),App.Rotation(App.Vector(0,0,1),0))  
            c1=c1.removeSplitter()  
            obj.Shape=c1 
            c1=c1.removeSplitter()
        elif key1==1:  
            sa=psuport_data.channel_ss[size]  
            H=sa[0]
            B=sa[1]
            t1=sa[2]
            t2=sa[3]
            r1=sa[4]
            r2=sa[5]
            Cy=sa[8]*10   
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
                p2=(vy*H,0,0)
                p3=(vy*H,vx*B,0)
                p4=(vy*(H-y4),vx*B,0)
                p5=(vy*(H-(y4+y1)),vx*(B-x1),0)
                p6=(vy*(H-(y4+y2)),vx*(B-x30),0)
                p7=(vy*(H-y10),vx*(t1+x40),0)
                p8=(vy*(H-y11),vx*(t1+x5),0)
                p9=(vy*(H-y12),vx*t1,0)
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
                W=x0*H+80
                B1=B+20
                pface=Part.makePlane(W,B1)
                c00=pface.extrude(Base.Vector(0,0,t0))

            L=L1-t1-t0
            vx=1
            vy=-1
            #主材
            channel2(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L,0,H),App.Rotation(App.Vector(0,1,0),-90))
            c1=c01
            pface=Part.makePlane(H,B,Base.Vector(L1-t0,B,0), Base.Vector(1,0,0))
            c02=pface.extrude(Base.Vector(-t1,0,0))
            c01=c01.fuse(c02)
            c1=c1.fuse(c01)
            #ベースプレート上
            x0=1.0
            if BasePlate==True:
                channel_bp(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(0,-10,-40),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.fuse(c01)

            #斜材
            if k==45:
                L=L1*1.4142
            else:
                L=L1*2.0/1.732    
            channel2(self)
            c01=c00
            if k==45:
                c01.Placement=App.Placement(App.Vector(-t0,0,-L1),App.Rotation(App.Vector(0,1,0),90-k))
            else:
                c01.Placement=App.Placement(App.Vector(-t0,0,-L1/1.732),App.Rotation(App.Vector(0,1,0),90-k))
            pface=Part.makePlane(2*H,2*H,Base.Vector(L1-2*H,0,0), Base.Vector(0,1,0))
            c02=pface.extrude(Base.Vector(0,2*H,0))
            c01=c01.cut(c02)
            if k==30:
                pface=Part.makePlane(2*H,2*H,Base.Vector(-2*H,0,-L1/1.732), Base.Vector(0,1,0))
            else:
                pface=Part.makePlane(2*H,2*H,Base.Vector(-2*H,0,-L1), Base.Vector(0,1,0))
            c03=pface.extrude(Base.Vector(0,2*H,0))
            c01=c01.cut(c03)
            c1=c1.fuse(c01)
            #ベースプレート下
            x0=1.5
            if BasePlate==True:
                channel_bp(self)
                c01=c00
                if k==45:
                    c01.Placement=App.Placement(App.Vector(0,-10,-40-L1),App.Rotation(App.Vector(0,1,0),-90))
                else:
                    c01.Placement=App.Placement(App.Vector(0,-10,-40-L1/1.732),App.Rotation(App.Vector(0,1,0),-90))
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