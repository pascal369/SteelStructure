from FreeCAD import Base
import FreeCAD, Part , math
from math import pi
import FreeCAD as App
from . import HandData
class circular_arc:#03 04
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        g0=App.ActiveDocument.getObject(label).g0*1000
        p=App.ActiveDocument.getObject(label).p
        Reverse=App.ActiveDocument.getObject(label).Reverse
        '''
        if Reverse==True:
            cx=int(-1)
        else:
            cx=int(1)
        '''
        def sichu(self):
            global c00
            c00= Part.makeBox(130.0,50.0,6.0,Base.Vector(-65,-25-R,0),Base.Vector(0,0,1))
            for i in range(2):
                if i==0:
                    x=-45
                else:
                    x=45
                c01= Part.makeCylinder(7.5,6.0,Base.Vector(x,0-R,0),Base.Vector(0,0,1),360)
                c00=c00.cut(c01)
            c010= Part.makeCylinder(17.0,h,Base.Vector(0,0-R,0),Base.Vector(0,0,1),360)
            c011= Part.makeCylinder(13.8,h,Base.Vector(0,0-R,0),Base.Vector(0,0,1),360)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)

        def Corner2_arc(self):#円弧 
            global c00
            x1=R*math.cos(s/2)
            y1=R*math.sin(s/2)
            x2=R*math.cos(s)
            y2=R*math.sin(s)
            if spec_siyo=='Sewerage Works Agency':
                n=2
            elif spec_siyo=='General':
                n=3    
            for i in range(n):
                if i==0:#笠木
                    h1=h
                    edge20 = Part.makeCircle(21.35, Base.Vector(0,-R,h1), Base.Vector(1,0,0), 0, 360)
                    edge21 = Part.makeCircle(17.85, Base.Vector(0,-R,h1), Base.Vector(1,0,0), 0, 360)
                    #edge2=edge20.cut(edge21)
                    if type=='03_Circular_arc':
                        edge20.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
                        edge21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
                elif i==1:#中間玄材
                    if spec_siyo=='General' :
                        h1=h/2
                    else:
                        h1=100    
                    edge20 = Part.makeCircle(17.0, Base.Vector(0,-R,h1), Base.Vector(1,0,0), 0, 360)
                    edge21 = Part.makeCircle(13.8, Base.Vector(0,-R,h1), Base.Vector(1,0,0), 0, 360)
                    #edge2=edge20.cut(edge21)
                elif i==2:
                    if spec_siyo=='Sewerage Works Agency':
                        return
                    h1=20

                    if Reverse==False:
                        x=17
                    else:
                        x=-17-6    

                    p4=(0,x-R,h1)
                    p5=(0,x-R,h1+50)
                    p6=(0,x+6-R,h1+50)
                    p7=(0,x+6-R,h1)
                    edge20=Part.makePolygon([p4,p5,p6,p7,p4])
                p1=(0,-R,h1)
                p2=(R*math.sin(s/2),-R*math.cos(s/2),h1)
                p3=(R*math.sin(s),-R*math.cos(s),h1)
                edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
                aWire=Part.Wire([edge1])
                profile1=Part.Wire([edge20])
                profile2=Part.Wire([edge21])
                makeSolid=True
                isFrenet=True
                if i==0:
                    c000 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
                    c001 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
                    c00=c000.cut(c001)
                else:
                    c010 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
                    c011 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
                    c01=c010.cut(c011)
                    #c00=c00.fuse(c01) 
                    c00=Part.makeCompound([c00,c01]) 
        def Corner2_arc_a(self):#円弧 アルミ
            global c00
            x1=R*math.cos(s/2)
            y1=R*math.sin(s/2)
            x2=R*math.cos(s)
            y2=R*math.sin(s)
            
            for i in range(2):
                if i==0:
                    H=50
                    B=70
                    h1=h-H
                    
                elif i==1:
                    H=33
                    B=45
                    h1=100
                    
                p4=(0,-B/2-R,h1)
                p5=(0,-B/2-R,h1+H)
                p6=(0,B/2-R,h1+H)
                p7=(0,B/2-R,h1)
                edge20=Part.makePolygon([p4,p5,p6,p7,p4])

                p40=(0,-(B-10)/2-R,h1+5)
                p50=(0,-(B-10)/2-R,h1+H-10+5)
                p60=(0,(B-10)/2-R,h1+H-10+5)
                p70=(0,(B-10)/2-R,h1+5)
                edge21=Part.makePolygon([p40,p50,p60,p70,p40])

                #Part.show(edge20)
                #Part.show(edge21)


                p1=(0,-R,h1)
                p2=(R*math.sin(s/2),-R*math.cos(s/2),h1)
                p3=(R*math.sin(s),-R*math.cos(s),h1)
                edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
                aWire=Part.Wire([edge1])
                profile1=Part.Wire([edge20])
                profile2=Part.Wire([edge21])
                makeSolid=True
                isFrenet=True
                if i==0:
                    c000 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
                    c001 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
                    c00=c000.cut(c001)
                else:
                    c010 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
                    c011 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
                    c01=c010.cut(c011)
                    c00=c00.fuse(c01) 
        def sichu_tanbu(self):#支柱端部
            global c00
            x1=50.0*math.sin(45.0*pi/180.0)
            y1=x1
            c00= Part.makeBox(130.0,50.0,6.0,Base.Vector(-65,-25,0),Base.Vector(0,0,1))
            for i in range(2):
                if i==0:
                    x=-45
                else:
                    x=45
                c01= Part.makeCylinder(7.5,6.0,Base.Vector(x,0,0),Base.Vector(0,0,1),360)
                c00=c00.cut(c01)
            p1=(0,0,0)
            p2=(0,0,h-50)
            p3=(-(50-x1),0,h-50+y1)
            p4=(-50,0,h)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p4),Base.Vector(p3),Base.Vector(p2)).toShape()
            aWire=Part.Wire([edge1,edge2])
            edge4 = Part.makeCircle(21.35, Base.Vector(0,0,0), Base.Vector(0,0,1), 0, 360)
            profile = Part.Wire([edge4])
            makeSolid=True
            isFrenet=True
            c01 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c00=c00.fuse(c01)
            if spec_siyo=='General':
                h1=h/2
            elif spec_siyo=='Sewerage Works Agency':
                h1=100    
            c01= Part.makeCylinder(17.0,50.0,Base.Vector(-50,0,h1),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            if spec_siyo=='SWA_Al' :
                pass
            else:
                if Reverse==True:
                    cx=int(-1)
                else:
                    cx=int(1)
                y=-17
                c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y,20),Base.Vector(1,0,0))
                c00=c00.fuse(c01)
        label=obj.Name
        #key=App.ActiveDocument.getObject(label).key  
        type=App.ActiveDocument.getObject(label).type
        spec_siyo=App.ActiveDocument.getObject(label).spec
        h=App.ActiveDocument.getObject(label).h
        R=App.ActiveDocument.getObject(label).R
        k=App.ActiveDocument.getObject(label).k
        s=float(math.radians(k)) 
        k1=150*180/(pi*R)
        k0=k1*6*p/1000
        s0=math.radians(k0)
        n=int(k/k0)
        x=R*math.sin(s0/2)
        y=R*math.cos(s0/2)
        if spec_siyo=='General':#一般
            for i in range(n+1):
                if i==0:
                    sichu(self)
                    c1=c00

                else:
                    sichu(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),i*k0))
                    c1=c1.fuse(c2)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),(k-n*k0)/2))
            Corner2_arc(self)
            c3=c00
            #c1=c1.fuse(c3)
            c1=Part.makeCompound([c1,c3])

        elif spec_siyo=='Sewerage Works Agency':#事業団
            for i in range(n+1):
                if i==0:
                    sichu(self)
                    c1=c00
                else:
                    sichu(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),i*k0))
                    c1=c1.fuse(c2)
                #c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),(0)))
            n1=int((k)/k1)
            for i in range(n1+1):
                if i==0:
                    c020= Part.makeCylinder(10.85,h-100.0,Base.Vector(0,-R,100),Base.Vector(0,0,1),360)
                    c021= Part.makeCylinder(8.05,h-100.0,Base.Vector(0,-R,100),Base.Vector(0,0,1),360)
                    c02=c020.cut(c021)
                else:
                    c020= Part.makeCylinder(10.85,h-100.0,Base.Vector(0,-R,100),Base.Vector(0,0,1),360)
                    c021= Part.makeCylinder(8.05,h-100.0,Base.Vector(0,-R,100),Base.Vector(0,0,1),360)
                    c02=c020.cut(c021)
                    c02.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),i*k1))
                    c1=c1.fuse(c02)
            
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),(k-n1*k1)/2))
            Corner2_arc(self)
            c3=c00
            c1=Part.makeCompound([c1,c3])
        elif spec_siyo=='SWA_Al':#事業団アルミ
            k0=k1*12
            n=int((k-k1*4)/k0)
            for i in range(n+1):
                if i==0:
                    c10=Part.makeBox(60,60,h-50,Base.Vector(-30,-R-30,0),Base.Vector(0,0,1)) 
                    c11=Part.makeBox(50,50,h-50,Base.Vector(-30+5,-R-30+5,0),Base.Vector(0,0,1)) 
                    #Part.show(c10)
                    #Part.show(c11)
                    c1=c10.cut(c11)
                    c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),4*k1)) 
                else:
                    c20=Part.makeBox(60,60,h-50,Base.Vector(-30,-R-30,0),Base.Vector(0,0,1)) 
                    c21=Part.makeBox(50,50,h-50,Base.Vector(-30+5,-R-30+5,0),Base.Vector(0,0,1)) 
                    c2=c20.cut(c21)
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),i*k0+4*k1))
                    c1=c1.fuse(c2)
            n1=int((k)/k1)
            for i in range(n1+1):
                c2=Part.makeBox(20,20,h-183.0,Base.Vector(-10,-R-10,133),Base.Vector(0,0,1))
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),i*k1))
                c1=c1.fuse(c2)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),(k-n1*k1)/2))
            Corner2_arc_a(self)
            c3=c00
            c1=Part.makeCompound([c1,c3])
        g=c1.Volume*g0/10**9 
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass         
        obj.Shape=c1