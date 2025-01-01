import FreeCAD
import FreeCADGui as Gui
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import FreeCAD as App

class SplCaseNP:
    def __init__(self, obj):
        self.Type = 'S01'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
        #return
    def execute(self, obj):
        label=obj.Name   
        H=App.ActiveDocument.getObject(label).H
        st=App.ActiveDocument.getObject(label).st
        d=App.ActiveDocument.getObject(label).d
        D=App.ActiveDocument.getObject(label).D
        #hs=App.ActiveDocument.getObject(label).hs
        a=App.ActiveDocument.getObject(label).a
        t1=App.ActiveDocument.getObject(label).t1 
        t2=App.ActiveDocument.getObject(label).t2 
        h=App.ActiveDocument.getObject(label).h
        C=App.ActiveDocument.getObject(label).C
        b=App.ActiveDocument.getObject(label).b
        f=App.ActiveDocument.getObject(label).f
        H0=App.ActiveDocument.getObject(label).H0
        #p=App.ActiveDocument.getObject(label).p
        n=App.ActiveDocument.getObject(label).n
        k=App.ActiveDocument.getObject(label).k
        m=App.ActiveDocument.getObject(label).m
        def handrail1(self):
            global c00
            c00=Part.makeCylinder(34/2,1100,Base.Vector(D/2-34/2,0,h),Base.Vector(0,0,1))
            c01=Part.makeCylinder(34/2,1100,Base.Vector(d/2+34/2,0,h),Base.Vector(0,0,1))
            c00=c00.fuse(c01)
        def handrail2(self):
            global c00
            helix=Part.makeHelix(p,H,C,0,False)
            helix.Placement=App.Placement(App.Vector(0,0,1100+h-25),App.Rotation(App.Vector(0,0,1),0))
            r=21.5
            p1=(0,0,r)
            p2=(-r,0,0)
            p3=(0,0,-r)
            p4=(r,0,0)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2])
            awire.Placement=App.Placement(App.Vector(D/2-17,0,1100+h-25),App.Rotation(App.Vector(0,0,1),0))
            #awire.Placement=App.Placement(App.Vector(D/2-17,0,1100+h),App.Rotation(App.Vector(0,0,1),0))
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(helix).makePipeShell([awire],makeSolid,isFrenet)
        def handrail3(self):
            global c00
            helix=Part.makeHelix(p,H,C,0,False)
            helix.Placement=App.Placement(App.Vector(0,0,1100+h-25),App.Rotation(App.Vector(0,0,1),0))
            r=21.5
            p1=(0,0,r)
            p2=(-r,0,0)
            p3=(0,0,-r)
            p4=(r,0,0)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2])
            awire.Placement=App.Placement(App.Vector(d/2+17,0,1100+h-25),App.Rotation(App.Vector(0,0,1),0))
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(helix).makePipeShell([awire],makeSolid,isFrenet)
        def cutter(self):
            global c00
            p1=(0,0,h)
            p2=(D/2+100,0,h)
            p3=((D/2+100)*math.cos(k),(D/2+100)*math.sin(k),h)
            #p3=((D/2+10)*math.cos(k),(D/2+10)*math.sin(ra),h)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeCircle(D/2+100,Base.Vector(0,0,h),Base.Vector(0,0,1),0,math.degrees(k))
            #edge2=Part.makeCircle(D/2+10,Base.Vector(0,0,h),Base.Vector(0,0,1),0,rd)
            edge3=Part.makeLine(p3,p1)
            wire=Part.Wire([edge1,edge2,edge3])
            face=Part.Face(wire)
            c00=face.extrude(Base.Vector(0,0,h+hs+t1+200))
            #Part.show(c00)
        def step2(self):
            global c00
            p1=(0,0,h)
            p2=(D/2+100,0,h)
            p3=((D/2+100)*math.cos(k),(D/2+100)*math.sin(k),h)
            #p3=((D/2+10)*math.cos(k),(D/2+10)*math.sin(ra),h)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeCircle(D/2+100,Base.Vector(0,0,h),Base.Vector(0,0,1),0,math.degrees(k))
            #edge2=Part.makeCircle(D/2+10,Base.Vector(0,0,h),Base.Vector(0,0,1),0,rd)
            edge3=Part.makeLine(p3,p1)
            wire=Part.Wire([edge1,edge2,edge3])
            face=Part.Face(wire)
            c00=face.extrude(Base.Vector(0,0,t1))
        def step(self):
            global c00
            #self.label_H.setText(QtGui.QApplication.translate("Dialog", str(math.degrees(k)), None))
            p1=(d/2-a,0,h)
            p2=(D/2+a,0,h)
            p3=((D/2+a)*math.cos(k),(D/2+a)*math.sin(k),h)
            p4=((d/2-a)*math.cos(k),(d/2-a)*math.sin(k),h)
            #p3=((D/2+a)*math.cos(ra),(D/2+a)*math.sin(ra),h)
            #p4=((d/2-a)*math.cos(ra),(d/2-a)*math.sin(ra),h)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p4,p1)
            wire=Part.Wire([edge1,edge2,edge3,edge4])
            face=Part.Face(wire)
            c00=face.extrude(Base.Vector(0,0,t1)) 
            #c00=face.extrude(Base.Vector(0,0,H/n)) 
            c00.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))  
        st=float(st) 
        C=d/2+(D-d)/4
        b=(D-d)/2
        f=b+2*a
        D1=(D-d)/2
        hs=150
        n=int(H/hs) 
        ra=math.radians(st/n)
        rd=float(st/n)
        h0=h+t1+hs
        p=H*360/(st-0.1)
        k=float(st/360*math.radians(st*p/(H*n)))
        H0=(n-1)*hs+h+t1

        helix=Part.makeHelix(p,H,C,0,False)
        h2=300+hs+t1
        p1=(d/2,0,0)
        p2=(d/2,0,h2)
        p3=(d/2+a,0,h2)
        p4=(d/2+a,0,0)
        p5=(D/2-a,0,h2)
        p6=(D/2,0,h2)
        p7=(D/2,0,0)
        p8=(D/2-a,0,0)
        
        Profile=Part.makePolygon([p1,p2,p3,p4,p1])
        Profile2=Part.makePolygon([p5,p6,p7,p8,p5])
        makeSolid=True
        isFrenet=True
        pipe = Part.Wire(helix).makePipeShell([Profile],makeSolid,isFrenet)
        pipe2 = Part.Wire(helix).makePipeShell([Profile2],makeSolid,isFrenet)
        c1=pipe.fuse(pipe2)
        #Part.show(c1)
        for i in range(n):
            cutter(self)
            c01=c00
            hs=H/n
            c01.Placement=App.Placement(App.Vector(0,0,i*hs*m),App.Rotation(App.Vector(0,0,1),i*math.degrees(k)))
            c1=c1.cut(c01)
            #Part.show(c01)
            
            step2(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,i*(hs*m)),App.Rotation(App.Vector(0,0,1),i*math.degrees(k)))
            #Part.show(c01)
            c1=c1.fuse(c01)
            c2=Part.makeCylinder(C-f/2,2*H0)
            c1=c1.cut(c2)
            handrail1(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(0,0,i*hs+t1),App.Rotation(App.Vector(0,0,1),i*math.degrees(k)+math.degrees(k)/2))
            c1=c1.fuse(c2)
        print('stephight='+str(hs))

        handrail2(self)
        c2=c00
        c1=c1.fuse(c2) 
        handrail3(self)
        c2=c00
        c1=c1.fuse(c2) 
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)  
        obj.Shape=c1 