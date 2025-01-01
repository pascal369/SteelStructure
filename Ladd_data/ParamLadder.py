import FreeCAD as App
import FreeCADGui as Gui
import FreeCAD, Part, math
from FreeCAD import Base
from . import ladderdata
class ParametricLadder:
    def __init__(self, obj):
        self.Type = 'Ladder'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
        #return
    def execute(self, obj):
        label=obj.Name
        g0=App.ActiveDocument.getObject(label).g0*1000
        type=App.ActiveDocument.getObject(label).type
        h=App.ActiveDocument.getObject(label).StepHeight
        L0=App.ActiveDocument.getObject(label).FloorHeight
        L=App.ActiveDocument.getObject(label).RailingHeight
        #L1=App.ActiveDocument.getObject(label).L1
        n=int(L0/h)

        def ladder_c(self):
            global c00
            for i in range(2):
                if i==0:
                    y=0
                else:
                    y=400
                #本体
                p1=(0,y,0)
                p2=(0,y,L0+L-200)
                p3=(200,y,L0+L)
                p4=(400,y,L0+L-200)
                p5=(400,y,L0)

                edge1=Part.makeLine(p1,p2)
                edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
                edge3=Part.makeLine(p4,p5)
                aWire=Part.Wire([edge1,edge2,edge3])
                edge40 = Part.makeCircle(17.0, Base.Vector(0,y,0), Base.Vector(0,0,1), 0, 360)
                edge41 = Part.makeCircle(13.8, Base.Vector(0,y,0), Base.Vector(0,0,1), 0, 360)
                profile1 = Part.Wire([edge40])
                profile2 = Part.Wire([edge41])
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
                if type=='00_LadderA' or type=='01_LadderA with cage':
                    c02=Part.makeBox(100,500,9,Base.Vector(-50,-50,0),Base.Vector(0,0,1))    
                    c00=c00.fuse(c02)

                for i in range(2):
                        c03=Part.makeBox(200,9,100,Base.Vector(0,-4.5+400*i,(L0-100)),Base.Vector(0,0,1))  
                        c00=c00.fuse(c03) 
                        
                if type=='02_LadderB' or type=='03_LadderB with cage':
                    c03=Part.makeBox(100,500,250,Base.Vector(-50,-50,0),Base.Vector(0,0,1)) 
                    c00=c00.cut(c03) 
                    for j in range(2):
                        for i in range(2):
                            c04=Part.makeBox(200,9,100,Base.Vector(0,-4.5+400*i,300+(L0-400)*j),Base.Vector(0,0,1))  
                            c00=c00.fuse(c04) 

            #ステップ
            for j in range(n):
                c02= Part.makeCylinder(9.5,400,Base.Vector(0,0,300*j+300),Base.Vector(0,1,0),360)
                c00=c00.fuse(c02)

        def cage(self):
            global c00
            #h=App.ActiveDocument.getObject(label).h
            #L=App.ActiveDocument.getObject(label).L
            #L0=App.ActiveDocument.getObject(label).L0
            L00=L0+L-250
            L1=L00-2000  #ケージ長
            n1=int((L1+50)/1500)+1 #ケージ枠数
            n=int(L0/h)
            for i in range(n1+1):
                if i==0:
                    z=2000
                elif i==1:
                    z=L00
                else:
                    z=2000+(i-1)*L1/(n1)
                p1=(0,0,z)
                p2=(-47.5,0,z)
                p3=(-71.4,-11.8,z)
                p4=(-700,200,z)
                p5=(-71.4,411.8,z)
                p6=(-47.5,400,z)
                p7=(0,400,z)
                p8=(-60.8,-3.1,z)
                p9=(-60.8,403.1,z)

                p10=(0,-3,0+z)
                p11=(0,-3,50+z)
                p12=(0,3,50+z)
                p13=(0,3,0+z)

                edge1=Part.makeLine(p1,p2)
                edge2=Part.Arc(Base.Vector(p3),Base.Vector(p8),Base.Vector(p2)).toShape()
                edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
                edge4=Part.Arc(Base.Vector(p5),Base.Vector(p9),Base.Vector(p6)).toShape()
                edge5=Part.makeLine(p6,p7)
                aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])

                edge6=Part.makeLine(p10,p11)
                edge7=Part.makeLine(p11,p12)
                edge8=Part.makeLine(p12,p13)
                edge9=Part.makeLine(p13,p10)
                profile=Part.Wire([edge6,edge7,edge8,edge9])

                makeSolid=True
                isFrenet=True
                c1 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
                c00=c00.fuse(c1)
            #タテワク　FB50*6
            for i in range(3):
                if i==0:
                    x=-375
                    y=-145
                    c2= Part.makeBox(50.0,6.0,L00-2000,Base.Vector(x,y,2000),Base.Vector(0,0,1))
                elif i==1:
                    x=-695
                    y=175
                    c2= Part.makeBox(6.0,50.0,L00-2000,Base.Vector(x,y,2000),Base.Vector(0,0,1))
                else:
                    x=-375
                    y=540
                    c2= Part.makeBox(50.0,6.0,L00-2000,Base.Vector(x,y,2000),Base.Vector(0,0,1))

                c00=c00.fuse(c2)
        if type=='00_LadderA' or type=='02_LadderB':            
            label=obj.Name
            ladder_c(self)
            c1=c00
            
        elif type=='01_LadderA with cage' or type=='03_LadderB with cage':   
            label=obj.Name
            ladder_c(self)
            c1=c00
            cage(self)
            c2=c00
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