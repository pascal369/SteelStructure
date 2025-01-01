from FreeCAD import Base
import FreeCAD, Part , math
from math import pi
import FreeCAD as App
from . import HandData
class EndLine:#01 02
    def __init__(self, obj):
        self.Type = 'EndLine'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        type=App.ActiveDocument.getObject(label).type
        spec=App.ActiveDocument.getObject(label).spec
        spec_siyo=spec
        g0=App.ActiveDocument.getObject(label).g0*1000
        h=App.ActiveDocument.getObject(label).h
        l1=App.ActiveDocument.getObject(label).l1
        l2=App.ActiveDocument.getObject(label).l2  
        Reverse=App.ActiveDocument.getObject(label).Reverse
        k=App.ActiveDocument.getObject(label).k  
        p=App.ActiveDocument.getObject(label).p
        s=float(math.radians(k)) 
        x1=l1

        def sichu(self):
            global c00
            c00= Part.makeBox(130.0,50.0,6.0,Base.Vector(-65,-25,0),Base.Vector(0,0,1))
            for i in range(2):
                if i==0:
                    x=-45
                else:
                    x=45
                c01= Part.makeCylinder(7.5,6.0,Base.Vector(x,0,0),Base.Vector(0,0,1),360)
                c00=c00.cut(c01)
            c010= Part.makeCylinder(17.0,h,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c011= Part.makeCylinder(13.8,h,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
            if spec_siyo=='1':
                for i in range(6):
                    c010= Part.makeCylinder(10.85,h-100,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                    c011= Part.makeCylinder(8.05,h-100,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                    c01=c010.cut(c011)
                    c00=c00.fuse(c01)

        def Corner2(self):#コーナー
            global c00
            x1=50.0*math.cos(s/2)
            y1=50.0*math.sin(s/2)
            x2=50.0*math.cos(s)
            y2=50.0*math.sin(s)
            for i in range(3):
                if i==0:
                    h1=h
                    if type=='01_Corner with end':
                        edge200 = Part.makeCircle(21.35, Base.Vector(50,0,h1), Base.Vector(1,0,0), 0, 360)
                        edge210 = Part.makeCircle(17.85, Base.Vector(50,0,h1), Base.Vector(1,0,0), 0, 360)
                    else:
                        edge200 = Part.makeCircle(21.35, Base.Vector(0,0,h1), Base.Vector(1,0,0), 0, 360)
                        edge210= Part.makeCircle(17.85, Base.Vector(0,0,h1), Base.Vector(1,0,0), 0, 360)
                elif i==1:
                    if spec_siyo=='General':
                        h1=h/2
                    else:
                        h1=100    
                    edge200 = Part.makeCircle(17.0, Base.Vector(50,0,h1), Base.Vector(1,0,0), 0, 360)
                    edge210= Part.makeCircle(13.8, Base.Vector(50,0,h1), Base.Vector(1,0,0), 0, 360)
                elif i==2:
                    if spec_siyo=='Sewerage Works Agency':
                        return
                    h1=20
                    
                    if Reverse==True:
                        cx=int(-1)
                        x=17.0*cx
                        p4=(0,x-6,h1)
                        p5=(0,x-6,h1+50)
                        p6=(0,x,h1+50)
                        p7=(0,x,h1)

                    else:
                        cx=int(1)
                        x=17.0*cx
                        p4=(0,x,h1)
                        p5=(0,x,h1+50)
                        p6=(0,x+6,h1+50)
                        p7=(0,x+6,h1)

                    edge200=Part.makePolygon([p4,p5,p6,p7,p4])
                if i==1 or i==2:
                  p1=(0,0,h1)
                else:
                    if type=='01_Corner with end':
                        p1=(50,0,h1) 
                    else:
                        p1=(0,0,h1) 
                p2=(l1-50,0,h1)
                if k<0:
                    p3=(l1-50-y1,-(50-x1),h1)
                else:    
                    p3=(l1-50+y1,(50-x1),h1)

                p4=(l1+x2,y2,h1)
                p5=(l1+l2*math.cos(s),l2*math.sin(s),h1)
                edge1=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
                edge20=Part.makeLine(Base.Vector(p2),Base.Vector(p1))
                edge30=Part.makeLine(Base.Vector(p4),Base.Vector(p5))
                aWire=Part.Wire([edge20,edge1,edge30])
                profile1=Part.Wire([edge200])
                profile2=Part.Wire([edge210])
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
            edge40 = Part.makeCircle(21.35, Base.Vector(0,0,0), Base.Vector(0,0,1), 0, 360)
            edge41 = Part.makeCircle(17.85, Base.Vector(0,0,0), Base.Vector(0,0,1), 0, 360)
            
            profile1 = Part.Wire([edge40])
            profile2 = Part.Wire([edge41])
            makeSolid=True
            isFrenet=True
            c010 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c011 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
            if spec_siyo=='General':
                h1=h/2
            elif spec_siyo=='Sewerage Works Agency':
                h1=100    
            c01= Part.makeCylinder(17.0,50.0,Base.Vector(-50,0,h1),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            if spec_siyo=='SWA_Al' or spec_siyo=='Sewerage Works Agency':
                pass
            else:
                y=-17
                if Reverse==True:
                    cx=int(-1)
                    c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,cx*y+6,20),Base.Vector(1,0,0))
                else:
                    cx=int(1)
                    c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,cx*y,20),Base.Vector(1,0,0))
                c00=c00.fuse(c01)
        def Corner20a(self):#アルミ手すり
            global c00
            for i in range(2):
                if i==0:
                    H=50
                    B=70
                    h1=h
                    if k>0:
                        x=B/2*math.tan(s/2)
                    else:
                        x=B/2*math.tan(s/2)-B*math.tan(s/2)
                    pface1=Part.makePlane(H,B,Base.Vector(0,0,h1-50), Base.Vector(1,0,0))
                    pface2=Part.makePlane(H-10,B-10,Base.Vector(0,-5,h1-50+5), Base.Vector(1,0,0))
                    #Part.show(pface1)
                    #Part.show(pface2)
                    c001=pface1.extrude(Base.Vector(l1+x,0,0))
                    c002=pface2.extrude(Base.Vector(l1+x,0,0))
                    c00=c001.cut(c002)

                    pface1.Placement=App.Placement(App.Vector(l1-x,0,0),App.Rotation(App.Vector(0,0,1),0))
                    pface2.Placement=App.Placement(App.Vector(l1-x,0,0),App.Rotation(App.Vector(0,0,1),0))
                    c010=pface1.extrude(Base.Vector(l2+x,0,0))
                    c011=pface2.extrude(Base.Vector(l2+x,0,0))
                    c01=c010.cut(c011)
                    c01.rotate(Base.Vector(l1,-35,0),Base.Vector(0,0,1),k)
                    c00=c00.fuse(c01)
                elif i==1:
                    H=33
                    B=45
                    h1=100
                    if k>0:
                        x=B/2*math.tan(s/2)
                    else:
                        x=B/2*math.tan(s/2)-B*math.tan(s/2)
                    pface1=Part.makePlane(H,B,Base.Vector(0,-12.5,h1), Base.Vector(1,0,0))
                    pface2=Part.makePlane(H-10,B-10,Base.Vector(0,-17.5,h1+5), Base.Vector(1,0,0))
                    #Part.show(pface1)
                    #Part.show(pface2)
                    c020=pface1.extrude(Base.Vector(l1+x,0,0))
                    c021=pface2.extrude(Base.Vector(l1+x,0,0))
                    c02=c020.cut(c021)
                    pface1.Placement=App.Placement(App.Vector(l1-x,0,0),App.Rotation(App.Vector(0,0,1),0))
                    pface2.Placement=App.Placement(App.Vector(l1-x,0,0),App.Rotation(App.Vector(0,0,1),0))
                    c030=pface1.extrude(Base.Vector(l2+x,0,0))
                    c031=pface2.extrude(Base.Vector(l2+x,0,0))
                    c03=c030.cut(c031)
                    c03.rotate(Base.Vector(l1,-35,0),Base.Vector(0,0,1),k)
                    c02=c02.fuse(c03)
                    c00=c00.fuse(c02)
                c00=c00.removeSplitter()
        
        if spec_siyo=='General':#一般手すり
            if type=='01_Corner with end':
                sichu_tanbu(self)#支柱端部
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
                if l1<=500:
                    c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
                    pass
                else:
                    sichu(self)    
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(l1-500,0,0),App.Rotation(App.Vector(0,0,1),180))
                    c1=c1.fuse(c2)
            else:
                if l1<500:
                    #print(l1)
                    pass
                else:
                    sichu(self)    
                    c1=c00
                    c1.Placement=App.Placement(App.Vector(l1-500,0,0),App.Rotation(App.Vector(0,0,1),180))
                
                    n1=int(l1-p/2)/p
                    if n1<0:
                        n1=1
                    if (l1-p/2-n1*p)>=p:
                        if l1<=p:
                            pass
                        else:
                            sichu(self)    
                            c1=c00
                            c1.Placement=App.Placement(App.Vector(l1-500,0,0),App.Rotation(App.Vector(0,0,1),180))
                            sichu(self)    
                            c2=c00
                            c1=c1.fuse(c2)
                    else:
                        if l1<=p:
                            pass
                        else:
                            c1.Placement=App.Placement(App.Vector(((l1-500)*p/p),0,0),App.Rotation(App.Vector(0,0,1),180))  

            L0=l1
            n=int(l1/p+0.5)
            if type=='01_Corner with end':
                n=int(l1/p) 
            for i in range(n-1):
                if l1<1000:
                    pass
                else:
                    sichu(self)
                if type=='01_Corner with end' or type=='06_Channel':
                    if l1<1500:
                        sichu
                        c1=c00
                    else:
                        c3=c00
                        c3.Placement=App.Placement(App.Vector(l1-(500+(i+1)*p),0,0),App.Rotation(App.Vector(0,0,1),0))
                        c1=c1.fuse(c3)
                else:
                    c3=c00
                    if type=='06_Channel':
                        if l1<=1500:
                            c3.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
                        else:
                            c3.Placement=App.Placement(App.Vector(l1-(500+(i)*p),0,0),App.Rotation(App.Vector(0,0,1),0))
                    
                    else:
                        if l1<500:
                            pass
                            #c1=c3
                        else:
                            c3.Placement=App.Placement(App.Vector(l1-(500+(i+1)*p),0,0),App.Rotation(App.Vector(0,0,1),0))
                    if l1<500:
                        pass
                    else:
                        c1=c1.fuse(c3)
            #print(l1)            
            Corner2(self)
            c2=c00
            if type=='02_Corner' and l1<500:
                c1=c2
            else:    
                c1=c1.fuse(c2)

            if l1<100:
                c1=c2
            else:    
                c1=c1.fuse(c2)
                
            L0=l2-50
            n=int(l2/p+0.5)
            for i in range(n):
                sichu(self)
                c2=c00
                #c2.Placement=App.Placement(App.Vector(l1+((i+1)*p)*math.cos(s),(500+(i)*p)*math.sin(s),0),App.Rotation(App.Vector(0,0,1),k))
                c2.Placement=App.Placement(App.Vector(l1+(500+i*p)*math.cos(s),(500+i*p)*math.sin(s),0),App.Rotation(App.Vector(0,0,1),k))
                c1=c1.fuse(c2)
            if type=='06_Channel':
                c2 = c1.mirror(Base.Vector(0,0,0), Base.Vector(1,0,0)) 
                c1=c1.fuse(c2)
                if p<l1<1000:
                    sichu(self)
                    c3=c00
                    c1=c1.fuse(c3)

        elif spec_siyo=='Sewerage Works Agency':#事業団
            if type=='01_Corner with end':
                sichu_tanbu(self)#支柱端部
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
            else:
                #pass
                sichu(self)    
                c1=c00
                c1.Placement=App.Placement(App.Vector(l1-450,0,0),App.Rotation(App.Vector(0,0,1),180))
           
            L0=l1-200
            n=int(l1/900)
            for i in range(n):
                sichu(self)
                c3=c00
                #Part.show(c3)
                #c3.Placement=App.Placement(App.Vector(l1+450-(i+1)*900,0,0),App.Rotation(App.Vector(0,0,1),0))
                c3.Placement=App.Placement(App.Vector(l1+450-(i+1)*900,0,0),App.Rotation(App.Vector(0,0,1),0))
                #Part.show(c3)
                c1=c1.fuse(c3)

                n=int((l1)/150+0.5)
                for i in range(n-1):
                    c2= Part.makeCylinder(11.0,h-100,Base.Vector(l1-150,0,100),Base.Vector(0,0,1),360)  
                    c2.Placement=App.Placement(App.Vector(-i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                    c1=c1.fuse(c2)
                       
            Corner2(self)
            c2=c00
            c1=c1.fuse(c2)
            L0=l2-50
            n=int((l2)/900)
            for i in range(n):
                sichu(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(l1+(-450+(i+1)*900)*math.cos(s),(-450+(i+1)*900)*math.sin(s),0),App.Rotation(App.Vector(0,0,1),k))
                c1=c1.fuse(c2)
              
            n=int((l2)/150+0.5)
            for i in range(n): 
                c2= Part.makeCylinder(11.0,h-100,Base.Vector(l1,0,100),Base.Vector(0,0,1),360)  
                c2.Placement=App.Placement(App.Vector(((i+1)*150*math.cos(s)),((i+1)*150*math.sin(s)),0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2) 
                
            if type=='06_Channel':
                c2 = c1.mirror(Base.Vector(0,0,0), Base.Vector(1,0,0)) 
                c1=c1.fuse(c2)    
                
        elif spec_siyo=='SWA_Al':#事業団アルミ
            #端部支柱
            if type=='01_Corner with end':
                c10=Part.makeBox(60,60,h-50,Base.Vector(-60,5,0),Base.Vector(0,0,1))
                c11=Part.makeBox(50,50,h-50,Base.Vector(-55,10,0),Base.Vector(0,0,1))
                #Part.show(c11)
                c1=c10.cut(c11)
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
            else:
                c10=Part.makeBox(60,60,h-50,Base.Vector(-60,5,0),Base.Vector(0,0,1))
                c11=Part.makeBox(50,50,h-50,Base.Vector(-55,10,0),Base.Vector(0,0,1))
                c1=c10.cut(c11)
                c1.Placement=App.Placement(App.Vector(l1-450,0,0),App.Rotation(App.Vector(0,0,1),180))
            
            L0=l1-150
            n=int(l1/1950)
            for i in range(n+1):
                #支柱
                c20=Part.makeBox(60,60,h-50,Base.Vector(0,-65,0),Base.Vector(0,0,1))
                c21=Part.makeBox(50,50,h-50,Base.Vector(5,-60,0),Base.Vector(0,0,1))
                c2=c20.cut(c21)
                if i==0:
                    c2.Placement=App.Placement(App.Vector(l1-450,0,0),App.Rotation(App.Vector(0,0,1),0))
                else:
                    c2.Placement=App.Placement(App.Vector(l1-(i)*1950,0,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c2)

            n=int((l1)/150)
            for i in range(n):
                c2=Part.makeBox(20,20,h-183.0,Base.Vector(150-10,-45,133),Base.Vector(0,0,1))
                c2.Placement=App.Placement(App.Vector((l1-(i+1)*150+30-150),0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.fuse(c2)
            L0=l2-150
            n=int((l2-420)/1950)
            for i in range(n+1):
                c20=Part.makeBox(60,60,h-50,Base.Vector(l1-30,-65,0),Base.Vector(0,0,1))
                c21=Part.makeBox(50,50,h-50,Base.Vector(l1-30+5,-60,0),Base.Vector(0,0,1))
                c2=c20.cut(c21)
                if i==0:
                    c2.Placement=App.Placement(App.Vector(420,0,0),App.Rotation(App.Vector(0,0,1),0))
                else:
                    c2.Placement=App.Placement(App.Vector(((i)*1950+420),0),App.Rotation(App.Vector(0,0,1),0))
                    c2=c2.fuse(c2)
                c2.rotate(Base.Vector(l1,-35,0),Base.Vector(0,0,1),k)
                c1=c1.fuse(c2)
            n=int((l2)/150)

            for i in range(n): 
                c2= Part.makeBox(20,20,h-183,Base.Vector(l1-10,-45,133),Base.Vector(0,0,1))  
                c2.Placement=App.Placement(App.Vector(((-30+(i+1)*150)),0,0),App.Rotation(App.Vector(0,0,1),0))
                c2=c2.fuse(c2)
                c2.rotate(Base.Vector(l1,-35,0),Base.Vector(0,0,1),k)
                c1=c1.fuse(c2) 
            Corner20a(self)
            c2=c00
            c1=c1.fuse(c2)
            if type=='06_Channel':
                c2 = c1.mirror(Base.Vector(0,0,0), Base.Vector(1,0,0)) 
                c1=c1.fuse(c2)
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