from FreeCAD import Base
import FreeCAD, Part , math
from math import pi
import FreeCAD as App
from . import HandData
class edge:#04 05
    def __init__(self, obj):
        self.Type = 'EndLine'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        g0=App.ActiveDocument.getObject(label).g0*1000
        type=App.ActiveDocument.getObject(label).type
        spec=App.ActiveDocument.getObject(label).spec
        spec_siyo=spec
        h=App.ActiveDocument.getObject(label).h
        Reverse=App.ActiveDocument.getObject(label).Reverse

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


            profile1= Part.Wire([edge40])
            profile2= Part.Wire([edge41])
            makeSolid=True
            isFrenet=True
            c010 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c011 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
            #print(spec_siyo)
            if spec_siyo=='General':
                h1=h/2
            elif spec_siyo=='Sewerage Works Agency':
                h1=100    
            
            c010= Part.makeCylinder(17.0,50.0,Base.Vector(-50,0,h1),Base.Vector(1,0,0),360)
            c011= Part.makeCylinder(13.8,50.0,Base.Vector(-50,0,h1),Base.Vector(1,0,0),360)
            c01=c010.cut(c011)
            c00=c00.fuse(c01)
            if spec_siyo=='SWA_Al' or spec_siyo=='Sewerage Works Agency':
                pass
            else:
                if type=='04_Edge_R':
                    if Reverse==True:
                        cx=int(-1)
                        y=-17*cx
                        c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y+6,20),Base.Vector(1,0,0))
                    else:
                        cx=int(1)
                        y=-17*cx
                        c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y,20),Base.Vector(1,0,0))
                    c00=c00.fuse(c01)
                elif type=='05_Edge_L':
                    if Reverse==True:
                        cx=int(1)
                        y=-17*cx   
                        c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y,20),Base.Vector(1,0,0))
                    else:
                        cx=int(-1)
                        y=-17*cx
                        c01= Part.makeBox(50.0,6.0,50.0,Base.Vector(-50,y+6,20),Base.Vector(1,0,0))    
                    c00=c00.fuse(c01)
                
        
        if spec_siyo=='General':#一般手すり
            sichu_tanbu(self)#支柱端部
            c1=c00
        elif spec_siyo=='Sewerage Works Agency':#事業団
            sichu_tanbu(self)#支柱端部
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
                
        elif spec_siyo=='SWA_Al':#事業団アルミ
            #端部支柱
            c1=Part.makeBox(60,60,h-50,Base.Vector(-60,5,0),Base.Vector(0,0,1))
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),180))
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
