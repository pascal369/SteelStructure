from ast import Pass
import FreeCADGui as Gui
import FreeCAD
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App
from . import StlStrdata2
class ParamStaire20:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        global hand_w
        global key
        
        label=obj.Name

        type=App.ActiveDocument.getObject(label).type 
        if type=='Stairs':
            key=0
        elif type=='With handrail' :
            key=1
        elif type=='With handrail_1' :
            key=2
        elif type=='With handrail_2' :
            key=3    

        Position=App.ActiveDocument.getObject(label).Position
        g32=3.38
        g25=2.43
        #L=App.ActiveDocument.getObject(label).L
        L1=App.ActiveDocument.getObject(label).L1
        H=App.ActiveDocument.getObject(label).H0
        L=H
        w=App.ActiveDocument.getObject(label).w
        t=App.ActiveDocument.getObject(label).t

        size=App.ActiveDocument.getObject(label).size
        sa=StlStrdata2.channel_ss[size]
        H0=float(sa[0])
        B=float(sa[1])
        t1=float(sa[2])
        r1=float(sa[4])
        r2=float(sa[5])
        Cy=float(sa[8])*10
        t2=float(sa[3])

        def channel(self):
            global c00
            x0=1
            vx=1
            vy=1
            vz=1
            w=0.0

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
            p2=(0,0,vz*H0)
            p3=(0,vy*B-w,vz*H0)
            p4=(0,vy*B-w,vz*(H0-y4))
            p5=(0,vy*(B-x1)-w,vz*(H0-(y4+y1)))
            p6=(0,vy*(B-x30)-w,vz*(H0-(y4+y2)))
            p7=(0,vy*(t1+x40)-w,vz*(H0-y10))
            p8=(0,vy*(t1+x5)-w,vz*(H0-y11))
            p9=(0,vy*t1-w,vz*(H0-y12))
            p10=(0,vy*t1-w,vz*y12)
            p11=(0,vy*(t1+x5)-w,vz*y11)
            p12=(0,vy*(t1+x40)-w,vz*y10)
            p13=(0,vy*(B-x30)-w,vz*(y4+y2))
            p14=(0,vy*(B-x1)-w,vz*(y4+y1))
            p15=(0,vy*B-w,vz*y4)
            p16=(0,vy*B-w,0)
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
            c00=pface_c.extrude(Base.Vector(L0,0,0))
            #Part.show(c00)
        def channel2(self):
            global c00
            x0=1
            vx=1
            vy=-1
            vz=1
           
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
            p1=(0,-w,0)
            p2=(0,-w,vz*H0)
            p3=(0,vy*B-w,vz*H0)
            p4=(0,vy*B-w,vz*(H0-y4))
            p5=(0,vy*(B-x1)-w,vz*(H0-(y4+y1)))
            p6=(0,vy*(B-x30)-w,vz*(H0-(y4+y2)))
            p7=(0,vy*(t1+x40)-w,vz*(H0-y10))
            p8=(0,vy*(t1+x5)-w,vz*(H0-y11))
            p9=(0,vy*t1-w,vz*(H0-y12))
            p10=(0,vy*t1-w,vz*y12)
            p11=(0,vy*(t1+x5)-w,vz*y11)
            p12=(0,vy*(t1+x40)-w,vz*y10)
            p13=(0,vy*(B-x30)-w,vz*(y4+y2))
            p14=(0,vy*(B-x1)-w,vz*(y4+y1))
            p15=(0,vy*B-w,vz*y4)
            p16=(0,vy*B-w,0)
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
            c00=pface.extrude(Base.Vector(L0,0,0))
            return
        def handrail(self):#てすり
            global c00
            global c
            global s
            global hand_w
            
            s0=float(math.atan(H/L)*(180.0/pi))
            s=float(math.atan(H/L))
            a1=50*math.sin(s)
            a2=50*math.cos(s)
            a3=50*math.tan(s/2)
            a4=50-a2
            a5=50+a2
            b2=50*math.cos(s/2)
            b1=50*math.sin(s/2)
            f1=50*math.sin((180-s)/2)
            f2=50*math.cos((180-s)/2)
            h0=1100.0
            h=h0+100.0
            h1=h-a3
            h2=H-60+h1
            if size[:2]=='125':
                c=35.0
            else:
                c=40.0
            #32A
            p1=(0,c,-100)
            p2=(0,c,h1-100)
            p4=(a4,c,h1+a1-100)
            p5=(L-60-a5,c,h1+a1+H-2*60*math.sin(s)-100)
            p7=(L-60,c,h1+H-2*60*math.sin(s)-100)
            p5=(L-60-(50+a2),c,h1+H-2*60*math.sin(s)+a1-100)
            p7=(L-60,c,h1+H-2*60*math.sin(s)-100)
            p8=(L-60,c,H-2*60*math.sin(s)-100)
            p9=(50-b2,c,h1+b1-100)
            p10=(L-60-(50-f2),c,h1+H-2*60*math.sin(s)+f1-100)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p9),Base.Vector(p4)).toShape()
            edge3=Part.makeLine(p4,p5)
            edge4=Part.Arc(Base.Vector(p5),Base.Vector(p10),Base.Vector(p7)).toShape()
            edge5=Part.makeLine(p7,p8)
            edge6 = Part.makeCircle(21.35, Base.Vector(0,c,0), Base.Vector(0,0,1), 0, 360)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            profile = Part.Wire([edge6])
            makeSolid=True
            isFrenet=True
            c01 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            #mass上部
            hand_L=aWire.Length/1000
            hand_w1=g32*hand_L
            #手すり下部27.2mm
            c02 = Part.makeCylinder(17.0,(L-60)/math.cos(s),Base.Vector(0,c,0),Base.Vector(1,0,0))
            c02.Placement=App.Placement(App.Vector(0,0,550),App.Rotation(App.Vector(0,1,0),-s0))
            c01=c01.fuse(c02)
            #mass
            hand_L=(L-60)/math.cos(s)/1000
            hand_w2=g25*hand_L
            #中間柱
            n1=int((L-60)/900)+1
            l1=float((L-60.0)/n1)
            h1=float(l1*math.tan(s))
            x=30*math.cos(s)
            z=30*math.sin(s)
            for i in range(n1-1):
                if i==0:
                    x1=l1+x
                    z1=h1+z-100
                    h=h+20
                else :
                    x1=(i+1)*l1+x
                    z1=(i+1)*(h1-z)
                    h=h+z-20

                c02 = Part.makeCylinder(17.0,h,Base.Vector(x1,c,z1),Base.Vector(0,0,1))
                c01=c01.fuse(c02)
                #mass
                hand_L=h/1000
                hand_w3=g25*hand_L

            #下部カット
            l0=L
            h0=200.0-a1+l0*math.tan(s)
            p1=(-a2,100+c,0)
            p2=(-a2,100+c,200-a1)
            p3=(l0-a2,100+c,h0)
            p4=(l0-a2,100+c,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p1,p4)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c02=pface.extrude(Base.Vector(0,-200,0))
            c02.Placement=App.Placement(App.Vector(0,0,-200),App.Rotation(App.Vector(0,0,0),0))
            h=float(sa[0])
            c01=c01.cut(c02)
            x=30
            z=30*math.tan(s)
            c01.Placement=App.Placement(App.Vector(x,0,z),App.Rotation(App.Vector(0,1,0),0))
            c00=c01
            #mass
            hand_w=hand_w1+hand_w2+hand_w3
            shape=c00
            return shape
        def handrail_1(self):#手すり1
            global c00
            global c
            global s
            global hand_w
            
            s0=float(math.atan(H/L)*(180.0/pi))
            s=float(math.atan(H/L))
            a1=50*math.sin(s)
            a2=50*math.cos(s)
            a3=50*math.tan(s/2)
            a4=50-a2
            a5=50+a2
            b2=50*math.cos(s/2)
            b1=50*math.sin(s/2)
            f1=50*math.sin((180-s)/2)
            f2=50*math.cos((180-s)/2)
            l1=50*math.tan(s/2)
            l2=l1*math.sin(s)
            l3=l1*math.cos(s)
            m1=50*math.sin(s/2)
            m2=50*math.cos(s/2)
            h0=1100.0
            h=h0+100.0
            h1=h-a3
            h3=(L-30)*math.tan(s)
            h2=h3+h-100
            if size[:2]=='125':
                c=35.0
            else:
                c=40.0
            #32A
            p1=(0,c,-100)
            p2=(0,c,h1-100)
            p4=(a4,c,h1+a1-100)
            p5=(L-100,c,h2+100)
            p6=(L,c,h2)
            p7=(L+L1,c,h2)
            p8=(0,c,(h1+a3)/2-50)
            p9=(L-100,c,h3+(h1+a3)/2-150)
            p10=(L+L1,c,h3+(h1+a3)/2-50)
            p11=(L,c,h3-100)
            p12=(50-b2,c,h1+b1-100)
            p13=(L-l3-100,c,h2-l2)
            p14=(L+l1-100,c,h2)
            p15=(L+l1-m1-100,c,h2-(50-m2))
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p12),Base.Vector(p4)).toShape()
            edge3=Part.makeLine(p4,p13)
            edge4=Part.Arc(Base.Vector(p13),Base.Vector(p15),Base.Vector(p14)).toShape()
            edge5=Part.makeLine(p14,p7)
            edge6=Part.makeLine(p8,p9)
            edge7=Part.makeLine(p9,p10)

            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            edge8 = Part.makeCircle(21.35, Base.Vector(0,c,0), Base.Vector(0,0,1), 0, 360)
            #Part.show(edge7)
            profile=Part.Wire([edge8])
            makeSolid=True
            isFrenet=True
            c01 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            #mass
            hand_L=aWire.Length/1000
            hand_w1=g32*hand_L

            p91=(L-l3-100,c,h2-l2-h/2+50)
            p92=(L+l1-100,c,h2-h/2+50)
            p93=(L+l1-m1-100,c,h2-(50-m2)-h/2+50)
            edge1=Part.makeLine(p8,p91)
            edge2=Part.Arc(Base.Vector(p91),Base.Vector(p93),Base.Vector(p92)).toShape()
            edge3=Part.makeLine(p92,p10)
            edge4= Part.makeCircle(17, Base.Vector(L+L1,c,h3+(h1+a3)/2-50), Base.Vector(1,0,0), 0, 360)
            aWire=Part.Wire([edge1,edge2,edge3])
            profile=Part.Wire([edge4])
            makeSolid=True
            isFrenet=True
            c02 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c01=c01.fuse(c02)
            #25Amass
            hand_L=aWire.Length/1000
            hand_w2=g25*hand_L

            #中間柱
            n1=int((L-60)/900)+1
            l1=float((L-60.0)/n1)
            h1=float(l1*math.tan(s))
            x=30*math.cos(s)
            z=30*math.sin(s)
            for i in range(n1-1):
                if i==0:
                    x1=l1+x
                    z1=x1*math.tan(s)-100
                else :
                    x1=(i+1)*l1+x
                    z1=x1*math.tan(s)-100
                c02 = Part.makeCylinder(17.0,h+35,Base.Vector(x1,c,z1),Base.Vector(0,0,1))
                c01=c01.fuse(c02)
                #mass
                hand_L=(h+35)/1000
                hand_w3=g25*hand_L

            x1=L
            z1=h3   
            c03 = Part.makeCylinder(17.0,h-120,Base.Vector(x1,c,z1),Base.Vector(0,0,1))    
            c01=c01.fuse(c03)
            #self.label.setText(QtGui.QApplication.translate("Dialog", str(int(h)), None))
            #mass
            hand_L=(h-120)/1000
            hand_w4=g25*hand_L
            #下部カット
            l0=L
            h0=200.0-a1+l0*math.tan(s)
            p1=(-a2,100+c,0)
            p2=(-a2,100+c,200-a1)
            p3=(l0-a2,100+c,h0)
            p4=(l0-a2,100+c,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p1,p4)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c02=pface.extrude(Base.Vector(0,-200,0))
            c02.Placement=App.Placement(App.Vector(0,0,-200),App.Rotation(App.Vector(0,0,0),0))
            h=float(sa[0])
            c01=c01.cut(c02)
            x=30
            z=30*math.tan(s)
            c01.Placement=App.Placement(App.Vector(x,0,z),App.Rotation(App.Vector(0,1,0),0))
            c00=c01
            #mass
            hand_w=hand_w1+hand_w2+hand_w3+hand_w4
            shape=c00
            return shape
        def handrail_2(self):#手すり2
            global c00
            global c
            global hand_w
            
            s0=float(math.atan(H/(L))*(180.0/pi))
            s=float(math.atan(H/(L)))
            a1=50*math.sin(s)
            a2=50*math.cos(s)
            a3=50*math.tan(s/2)
            a4=50-a2
            a5=50+a2
            b2=50*math.cos(s/2)
            b1=50*math.sin(s/2)
            f1=50*math.sin((180-s)/2)
            f2=50*math.cos((180-s)/2)
            l1=50*math.tan(s/2)
            l2=l1*math.sin(s)
            l3=l1*math.cos(s)
            m1=50*math.sin(s/2)
            m2=50*math.cos(s/2)
            h0=1100.0
            h=h0+100.0
            h1=h-a3
            h3=(L-30)*math.tan(s)
            h2=h3+h-100
            if size[:2]=='125':
                c=35.0
            else:
                c=40.0
            #32A
            p1=(0,c,-100)
            p2=(0,c,h1-100)
            p4=(a4,c,h1+a1-100)
            p5=(L-100,c,h2+100)
            p6=(L,c,h2)
            p7=(L+L1,c,h2)
            p8=(0,c,150)
            p9=(L-100,c,h3+(h1+a3)/2-150)
            p10=(L+L1,c,h3+100)
            p11=(L,c,h3-100)
            p12=(50-b2,c,h1+b1-100)
            p13=(L-l3-50,c,h2-l2)
            p14=(L+l1-50,c,h2)
            p15=(L+l1-m1-50,c,h2-(50-m2))
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p12),Base.Vector(p4)).toShape()
            edge3=Part.makeLine(p4,p13)
            edge4=Part.Arc(Base.Vector(p13),Base.Vector(p15),Base.Vector(p14)).toShape()
            edge5=Part.makeLine(p14,p7)
            edge6=Part.makeLine(p8,p9)
            edge7=Part.makeLine(p9,p10)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            edge8 = Part.makeCircle(21.35, Base.Vector(0,c,0), Base.Vector(0,0,1), 0, 360)
            profile=Part.Wire([edge8])
            makeSolid=True
            isFrenet=True
            c01 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            #mass
            hand_L=aWire.Length/1000
            hand_w1=g32*hand_L
            #手すり下部27.2mm
            p91=(L-l3-70,c,h2-l2-h+200)
            p92=(L+l1-70,c,h2-h+200)
            p93=(L+l1-m1-70,c,h2-(50-m2)-h+200)
            edge1=Part.makeLine(p8,p91)
            edge2=Part.Arc(Base.Vector(p91),Base.Vector(p93),Base.Vector(p92)).toShape()
            edge3=Part.makeLine(p92,p10)
            edge4= Part.makeCircle(17, Base.Vector(L+L1,c,h3+100), Base.Vector(1,0,0), 0, 360)
            aWire=Part.Wire([edge1,edge2,edge3])
            profile=Part.Wire([edge4])
            makeSolid=True
            isFrenet=True
            c02 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c01=c01.fuse(c02)
            #mass
            hand_L=aWire.Length/1000
            hand_w2=g25*hand_L
            #格子
            n1=int((L)/150)+1
            l1=float((L)/n1)
            h1=float(l1*math.tan(s))
            x=30
            z=30*math.tan(s)
            for i in range(n1-1):
                if i==0:
                    x1=l1
                    z1=(i+1)*l1*math.tan(s)+150
                else :
                    x1=(i+1)*l1
                    z1=(i+1)*h1+150
                c02 = Part.makeCylinder(17.0,h-250,Base.Vector(x1,c,z1),Base.Vector(0,0,1))
                c01=c01.fuse(c02)
                #mass
                hand_L=(h+35)/1000
                hand_w3=g25*hand_L
                hand_w3=hand_w3+hand_w3

            x1=L
            z1=h3   
            c03 = Part.makeCylinder(17.0,h-100,Base.Vector(x1,c,z1),Base.Vector(0,0,1))    
            c01=c01.fuse(c03)
            #mass
            hand_L=(h-120)/1000
            hand_w4=g25*hand_L

            #下部カット
            l0=L
            h0=200.0-a1+l0*math.tan(s)
            p1=(-a2,100+c,0)
            p2=(-a2,100+c,200-a1)
            p3=(l0-a2,100+c,h0)
            p4=(l0-a2,100+c,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p1,p4)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c02=pface.extrude(Base.Vector(0,-200,0))
            c02.Placement=App.Placement(App.Vector(0,0,-200),App.Rotation(App.Vector(0,0,0),0))
            h=float(sa[0])
            c01=c01.cut(c02)
            x=30
            z=30*math.tan(s)
            c01.Placement=App.Placement(App.Vector(x,0,z),App.Rotation(App.Vector(0,1,0),0))
            c00=c01
            #mass
            hand_w=hand_w1+hand_w2+hand_w3+hand_w4
            shape=c00
            return shape
        def hontai(self):
            global c001
            global L0
            bb='stairs'
            #本体
            
            s0=float(math.atan(H/L)*(180.0/pi))
            s=float(math.atan(H/L))
            L00=math.sqrt(L**2+H**2)
            L0=L00
            channel(self)
            c001=c00
            L0=L00
            channel2(self)
            c002=c00
            c001=c001.fuse(c002)
            #底部カット
            H1=float(sa[0])
            B1=float(sa[1])
            x1=math.sin(s)*H1
            y1=math.cos(s)*H1
            a=float(H1*math.tan(s))
            a1=float(H1*math.tan(s/2))
            p1=(0,B1,0)
            p2=(0,B1,H1)
            p3=(0+H1/math.tan(s),B1,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p1)
            aWire=Part.Wire([edge1,edge2,edge3])
            pface=Part.Face(aWire)
            #w0=float(self.lineEdit_W.text())
            w0=w
            c01=pface.extrude(Base.Vector(0,-(w0+2*B1),0))
            c001=c001.cut(c01)
            #上部カット
            p1=(L00,B1,0)
            p2=(L00,B1,H1)
            p3=(L00-a1,B1,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p1)
            aWire=Part.Wire([edge1,edge2,edge3])
            pface=Part.Face(aWire)
            #w0=float(self.lineEdit_W.text())
            c01=pface.extrude(Base.Vector(0,-(w0+2*B1),0))
            c001=c001.cut(c01)
            c001.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-s0))
            #本体2
            L0=L1
            channel(self)
            c01=c00
            L0=L1
            channel2(self)
            c02=c00
            
            p1=(0,B1,0)
            p2=(0,B1,H1)
            p3=(a1,B1,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p1)
            aWire=Part.Wire([edge1,edge2,edge3])
            pface=Part.Face(aWire)
            c03=pface.extrude(Base.Vector(0,-(w0+2*B1),0))
            c01=c01.cut(c03)
            
            c01.Placement=App.Placement(App.Vector(-x1+L,0,y1-H1+H),App.Rotation(App.Vector(1,0,1),0))
            c001=c001.fuse(c01)

            c02=c02.cut(c03)
            c02.Placement=App.Placement(App.Vector(-x1+L,0,y1-H1+H),App.Rotation(App.Vector(1,0,1),0))
            c001=c001.fuse(c02)

            #ベースプレート
            b1=H1/math.sin(s)

            for i0 in range(2):
                if i0==0:
                    y=0
                else:
                    y=w0+B1
                p1=(0-x1,B1-y,0+y1-t)
                p2=(0-x1,B1-y,t+y1-t)
                p3=(b1-x1,B1-y,t+y1-t)
                p4=(b1-x1,B1-y,0+y1-t)
                edge1=Part.makeLine(p1,p2)
                edge2=Part.makeLine(p2,p3)
                edge3=Part.makeLine(p3,p4)
                edge4=Part.makeLine(p1,p4)
                aWire=Part.Wire([edge1,edge2,edge3,edge4])
                pface=Part.Face(aWire)
                c01=pface.extrude(Base.Vector(0,-B1,0))
                c001=c001.fuse(c01)

            #ステップ
            n1=int(H/200)+1
            h=H/n1
            for i in range(n1-1):
                a=h/math.tan(math.radians(45))
                b=h/math.tan(s)
                c=b-a    
                if i==0:
                    x01=h/math.tan(s)+x1+c
                    z01=h+y1
                else:
                    x01=(i+1)*h/math.tan(s)+x1+c
                    z01=(i+1)*h+y1
                y=w0
                p1=(0+x01-b1,0-y,0-30+z01)
                p2=(0+x01-b1,0-y,30-30+z01)
                p3=(250+x01-b1,0-y,30-30+z01)
                p4=(250+x01-b1,0-y,56.8-30+z01)
                p5=(253.2+x01-b1,0-y,56.8-30+z01)
                p6=(253.2+x01-b1,0-y,26.8-30+z01)
                p7=(3.2+x01-b1,0-y,26.8-30+z01)
                p8=(3.2+x01-b1,0-y,0-30+z01)
                #Part.show(c1)
                edge1=Part.makeLine(p1,p2)
                edge2=Part.makeLine(p2,p3)
                edge3=Part.makeLine(p3,p4)
                edge4=Part.makeLine(p4,p5)
                edge5=Part.makeLine(p5,p6)
                edge6=Part.makeLine(p6,p7)
                edge7=Part.makeLine(p7,p8)
                edge8=Part.makeLine(p8,p1)
                aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
                pface=Part.Face(aWire)
                c01=pface.extrude(Base.Vector(0,w0,0))
                c001=c001.fuse(c01)
            x=H1*math.sin(math.radians(45))
            z=H1*math.cos(math.radians(45))
            c001.Placement=App.Placement(App.Vector(x,0,-z),App.Rotation(App.Vector(0,1,0),0))
   
        doc = App.ActiveDocument

        if key==0:
            hontai(self)
            c1=c001
            obj.Shape=c1

            
            body_w=c1.Volume*7850/10**9
            label='mass[kg]'
            try:
                obj.addProperty("App::PropertyFloat", "body",label)
                obj.addProperty("App::PropertyFloat", "handrail",label)
                obj.addProperty("App::PropertyFloat", "mass",label)
                obj.body=body_w
                obj.handrail=0
                obj.mass=body_w
                obj.ViewObject.Proxy=0
            except:
                obj.body=body_w
                obj.handrail=0
                obj.mass=body_w
                obj.ViewObject.Proxy=0
                pass 

        elif key==1 or key==2 or key==3:
            # メインコンテナ
            assy = doc.getObject(obj.Name + "_Assy") or doc.addObject("App::Part", obj.Name + "_Assy")
            hontai(self)
            obj.Shape=c001
            c1=c001
            H1 = float(sa[0])
            x_offset = H1 * math.sin(math.radians(45))
            z_offset = H1 * math.cos(math.radians(45)) 
            new_placement = App.Placement(App.Vector(x_offset, 0, -z_offset),App.Rotation(App.Vector(0, 1, 0), 0))
            obj.Placement = new_placement
            assy.addObject(obj)
            handrail_list=[]

            if size[:2]=='125':
                c=35.0
            else:
                c=40.0
            if Position=='Both':
                n=2
            else:
                n=1
            w0=w 
            #mass
            body_w=c1.Volume*7850/10**9 

            for i in range(n):
                if Position=='Both':
                    if i==0:
                        y=0
                    else:
                        y=-(2*c+w0)
                else:
                    if Position=='Right':
                        y=-(2*c+w0)
                    elif Position=='Left':
                        y=0 
                if key==1:        
                    shape =handrail(self)
                elif key==2:
                    shape =handrail_1(self)
                elif key==3:
                    shape =handrail_2(self)

                # 手すりを作成したら、hr_group に入れる
                hr_name = f"{obj.Name}_Handrail_{i}" 
                obj2=doc.getObject(hr_name)

                if obj2:
                    # 既にあるなら形状を更新するだけ（これで消えなくなる）
                    obj2.Shape = shape
                else:
                    # ない時だけ新しく作る
                    obj2 = doc.addObject("Part::Feature", hr_name)
                    obj2.Shape = shape
                    assy.addObject(obj2)

                s=float(math.atan(H/L))
                x=30
                z=30*math.tan(s)
                
                obj2.Placement=App.Placement(App.Vector(x,y,z),App.Rotation(App.Vector(0,1,0),0))
                handrail_list.append(obj2)    

                # --- 4. Fusion (手すりの合体) の処理 ---
                fusion_name = obj.Name + "_HandrailFusion"
                fuse = doc.getObject(fusion_name)

                if len(handrail_list) >= 2:
                    # 2つ以上ある場合のみFusionを作成/更新
                    if fuse is None:
                        fuse = doc.addObject("Part::MultiFuse", fusion_name)
                        assy.addObject(fuse)

                     # Shapesをセットしてからrecomputeを呼ぶ
                    fuse.Shapes = handrail_list
                    fuse.recompute()
                    fuse.ViewObject.show() # 表示を確実にする
                
                elif len(handrail_list) == 1:
                    # 1つしかない場合はFusionは不要（エラーの原因になるため）
                    if fuse:
                        fuse.ViewObject.hide() # 既存のFusionがあれば隠す
                    handrail_list[0].ViewObject.show()
                    
                else:
                    # 手すりがゼロの場合
                    if fuse:
                        fuse.ViewObject.hide()
       
            total=body_w+hand_w*n

            label='mass[kg]'
            try:
                obj.addProperty("App::PropertyFloat", "body",label)
                obj.addProperty("App::PropertyFloat", "handrail",label)
                obj.addProperty("App::PropertyFloat", "mass",label)
                obj.body_w=body_w
                obj.hand_w=hand_w*n
                obj.mass=total
                obj.ViewObject.Proxy=0
            except:
                obj.body=body_w
                obj.handrail=hand_w*n
                obj.mass=total
                obj.ViewObject.Proxy=0
                pass

        
class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self
