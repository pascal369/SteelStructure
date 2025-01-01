import FreeCAD as App
import FreeCAD, Part , math
from math import pi
from FreeCAD import Base
from . import HandData
class StraightLine:#00
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        type=App.ActiveDocument.getObject(label).type
        spec_siyo=App.ActiveDocument.getObject(label).spec
        h=App.ActiveDocument.getObject(label).h
        l1=App.ActiveDocument.getObject(label).l1
        p=App.ActiveDocument.getObject(label).p
        g0=App.ActiveDocument.getObject(label).g0*1000
        #print(p)
        Reverse=App.ActiveDocument.getObject(label).Reverse
        if spec_siyo=='General':
            l00=float(p)
        else:
            l00=1950

        n=int(l1/l00)
        x2=(l1-(n)*l00)/2
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
            edge5 = Part.makeCircle(17.85, Base.Vector(0,0,0), Base.Vector(0,0,1), 0, 360)
            edge6 = edge4.cut(edge5)
            profile = Part.Wire([edge6])
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
            if spec_siyo=='SWA_Al' or spec_siyo=='Sewerage Works Agency':
                pass
            else:
                y=23
                c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y,20),Base.Vector(1,0,0))
                c00=c00.fuse(c01)
        def sichu(self):
            global c00
            c00= Part.makeBox(130.0,50.0,6.0,Base.Vector(-65,-25,0),Base.Vector(0,0,1))
            x=45
            c010= Part.makeCylinder(7.5,6.0,Base.Vector(x,0,0),Base.Vector(0,0,1),360)
            c011= Part.makeCylinder(7.5,6.0,Base.Vector(-x,0,0),Base.Vector(0,0,1),360)
            c01=c010.fuse(c011)
            c00=c00.cut(c01)
            c01= Part.makeCylinder(17.0,h,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c02= Part.makeCylinder(13.8,h,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c03=c01.cut(c02)
            c00=c00.fuse(c03)
        def h_rail(self):#一般_手すり
            global c00
            x1=l1+150
            n=int(L0+1)
            
            #笠木
            c000= Part.makeCylinder(21.7,L0,Base.Vector(0,0,h),Base.Vector(1,0,0),360)
            c001= Part.makeCylinder(17.85,L0,Base.Vector(0,0,h),Base.Vector(1,0,0),360)
            c00=c000.cut(c001)
            #下弦材
            c010= Part.makeCylinder(17.0,L0,Base.Vector(0,0,h/2),Base.Vector(1,0,0),360)
            c011= Part.makeCylinder(13.1,L0,Base.Vector(0,0,h/2),Base.Vector(1,0,0),360)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
            if Reverse==True:
                cx=int(-1)
                c01= Part.makeBox(50.0,6.0,L0,Base.Vector(0,cx*(-17)+6,20),Base.Vector(1,0,0))
            else:
                cx=int(1)
                c01= Part.makeBox(50.0,6.0,L0,Base.Vector(0,cx*(-17),20),Base.Vector(1,0,0))
            c00=c00.fuse(c01)
            
            
        def h_rail2(self):#事業団_手すり
            global c00
            x1=l1+150
            n=int(L0+1)
            #笠木
            c000= Part.makeCylinder(21.7,L0,Base.Vector(0,0,h),Base.Vector(1,0,0),360)
            c001= Part.makeCylinder(17.85,L0,Base.Vector(0,0,h),Base.Vector(1,0,0),360)
            c00=c000.cut(c001)

            #下弦材
            c010= Part.makeCylinder(17.0,L0,Base.Vector(0,0,100),Base.Vector(1,0,0),360)
            c011= Part.makeCylinder(13.1,L0,Base.Vector(0,0,100),Base.Vector(1,0,0),360)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
        def SWA_Al(self):#事業団アルミ手すり
            global c00
            c000=Part.makeBox(50,70,l1,Base.Vector(0,35,h-50),Base.Vector(1,0,0))
            c001=Part.makeBox(40,60,l1,Base.Vector(0,-5+35,h-50+5),Base.Vector(1,0,0))
            c00=c000.cut(c001)
            c20=Part.makeBox(33,45,l1,Base.Vector(0,22.5,100),Base.Vector(1,0,0))
            c21=Part.makeBox(23,35,l1,Base.Vector(0,-5+22.5,100+5),Base.Vector(1,0,0))
            #Part.show(c21)
            c2=c20.cut(c21)
            
            c00=c00.fuse(c2)
            l00=1950
            n=int(l1/l00)
            x2=(l1-l00*n)/2
            #支柱
            if n>=1:
                for i in range(n+1):
                    if i==0:
                        c20=Part.makeBox(60,60,h-50.0,Base.Vector(x2-30,-30,0),Base.Vector(0,0,1))
                        c21=Part.makeBox(50,50,h-50.0,Base.Vector(x2-30+5,-25,0),Base.Vector(0,0,1))
                        #Part.show(c20)
                        #Part.show(c21)
                        c2=c20.cut(c21)
                        
                        c00=c00.fuse(c2)
                    else :
                        c20=Part.makeBox(60,60,h-50.0,Base.Vector(x2-30,-30,0),Base.Vector(0,0,1))
                        c21=Part.makeBox(50,50,h-50.0,Base.Vector(x2-30+5,-25,0),Base.Vector(0,0,1))
                        #Part.show(c20)
                        #Part.show(c21)
                        c2=c20.cut(c21)
                        c2.Placement=App.Placement(App.Vector(i*l00,0,0),App.Rotation(App.Vector(0,1,0),0))
                        c00=c00.fuse(c2)
            else:
                c20=Part.makeBox(60,60,h-50,Base.Vector(l1/2-30,-30,0),Base.Vector(0,0,1))
                c21=Part.makeBox(50,50,h-50,Base.Vector(l1/2-30+5,-25,0),Base.Vector(0,0,1))
                c2=c20.cut(c21)
                c00=c00.fuse(c2)
            #ラチス    
            for j in range(n+1):
                x2=(l1-1950*n)/2
                x00=x2+150
                n1=int(x2/(150))
                if n==0:
                    for i in range(n1):
                        c2=Part.makeBox(20,20,h-183.0,Base.Vector(x2+150-10,-10,133),Base.Vector(0,0,1))
                        c2.Placement=App.Placement(App.Vector(i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                        c00=c00.fuse(c2)

                if j==0:
                    if n==0:
                        n00=n1
                    else:
                        n00=13
                    for i in range(n00):
                        c2=Part.makeBox(20,20,h-183,Base.Vector(x2+150-10,-10,133),Base.Vector(0,0,1))
                        c2.Placement=App.Placement(App.Vector(i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                        c00=c00.fuse(c2)
                    for i in range(n1):
                        c2=Part.makeBox(20,20,h-183,Base.Vector(x2-150-10,-10,133),Base.Vector(0,0,1))
                        c2.Placement=App.Placement(App.Vector(-i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                        c00=c00.fuse(c2)
                        
                elif j==n:
                    #self.label_type.setText(QtGui.QApplication.translate("Dialog", str(n), None))
                    for i in range(n1):
                        c2= Part.makeBox(20,20,h-183,Base.Vector((n)*l00+x00-10,-10,133),Base.Vector(0,0,1))  
                        c2.Placement=App.Placement(App.Vector(i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                        c00=c00.fuse(c2)
                        
                else:
                    for i in range(13):
                        c2= Part.makeBox(20,20,h-183,Base.Vector((j)*l00+x00-150-10,-10,133),Base.Vector(0,0,1))  
                        c2.Placement=App.Placement(App.Vector(i*150,0,0),App.Rotation(App.Vector(1,0,0),0))
                        c00=c00.fuse(c2)  
                        
        
        if n>=1:
            for i in range(n+1):
                if i==0:
                    sichu(self)
                    c1=c00
                    c1.Placement=App.Placement(App.Vector(x2,0,0),App.Rotation(App.Vector(0,1,0),0))

                else :
                    sichu(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(i*l00+x2,0,0),App.Rotation(App.Vector(0,1,0),0))
                    c1=c1.fuse(c2)
        else:
            sichu(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(l1/2,0,0),App.Rotation(App.Vector(0,1,0),0))
        if spec_siyo=='General':
            #print(spec_siyo)
            L0=l1
            h_rail(self)
            c2=c00
            c1=c1.fuse(c2)
            '''
            sichu_tanbu(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(-50,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            '''
        elif spec_siyo=='Sewerage Works Agency':#事業団
            L0=l1
            h_rail2(self)
            c2=c00
            c1=c1.fuse(c2)
            #return
            for j in range(n+2):
                n1=int(x2/(150))
                #print(x2)
                #print(n1)
                if j==0:
                    for i in range(n1+1): 
                        c20= Part.makeCylinder(10.85,h-100,Base.Vector(x2,0,0),Base.Vector(0,0,1),360)  
                        c21= Part.makeCylinder(8.05,h-100,Base.Vector(x2,0,0),Base.Vector(0,0,1),360) 
                        c2=c20.cut(c21)
                        c2.Placement=App.Placement(App.Vector(-i*150,0,100),App.Rotation(App.Vector(1,0,0),0))
                        c1=c1.fuse(c2)
                elif j==n+1:
                    for i in range(n1+1):
                        x00=x2+150
                        #self.label_type.setText(QtGui.QApplication.translate("Dialog", str(x2), None))
                        c20= Part.makeCylinder(10.85,h-100,Base.Vector((j-1)*l00+x2,0,0),Base.Vector(0,0,1),360) 
                        c21= Part.makeCylinder(8.05,h-100,Base.Vector((j-1)*l00+x2,0,0),Base.Vector(0,0,1),360) 
                        c2=c20.cut(c21)
                        c2.Placement=App.Placement(App.Vector(i*150,0,100),App.Rotation(App.Vector(1,0,0),0))
                        #Part.show(c2)
                        c1=c1.fuse(c2)
                else:
                    for i in range(13): 
                        c20= Part.makeCylinder(10.85,h-100,Base.Vector((j-1)*l00+x2,0,0),Base.Vector(0,0,1),360) 
                        c21= Part.makeCylinder(8.05,h-100,Base.Vector((j-1)*l00+x2,0,0),Base.Vector(0,0,1),360)
                        c2=c20.cut(c21) 
                        c2.Placement=App.Placement(App.Vector(i*150,0,100),App.Rotation(App.Vector(1,0,0),0))
                        c1=c1.fuse(c2)

        elif spec_siyo=='SWA_Al':#SWA_Al
            SWA_Al(self)
            c1=c00

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