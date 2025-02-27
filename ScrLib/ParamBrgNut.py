from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ScrData
class BrgNut:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        Thread=App.ActiveDocument.getObject(label).Thread
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        st=App.ActiveDocument.getObject(label).st
        
        sa=ScrData.brg_nut[dia]
        D0=float(sa[0])
        p=float(sa[1])
        d1=float(sa[2])
        D3=float(sa[3])
        D4=float(sa[4])
        D5=float(sa[5])
        k=float(sa[6])
        Bn=float(sa[7])
        s=float(sa[8])
        T=float(sa[10])
        t=float(sa[11])
        E=float(sa[13])
        n=sa[14]
        H=Bn
        if st=='Bearing Nut':
            y=(D3-D4)/2
            x=y*math.tan(math.pi/6)
            p1=(0,0,0)
            p2=(0,0,D3/2)
            p3=(Bn-x,0,D3/2)
            p4=(Bn,0,D4/2)
            p5=(Bn,0,0)
            plist=[p1,p2,p3,p4,p5,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
            if Thread==True:
                sa=ScrData.fine_screw[dia]
                H1=sa[1]
                sa1=ScrData.brg_nut[dia]
                D0=sa1[0]
                p=sa1[1]
                H0=0.86625*p
                x=H1+H0/8
                y=x*math.tan(math.pi/6)
                r0=D0/2+H0/8
                a=p/2-y
                #ボルト部
                cb= Part.makeCylinder(D0/2,H,Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト部
                c00=cb
                #ねじ断面
                p1=(-(D0/2-x),0,-p/2)
                p2=(-(D0/2-x),0,p/2)
                p3=(-D0/2,0,a)
                p4=(-D0/2-a/2,0,0)
                p5=(-D0/2,0,-a)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
                edge4 = Part.makeLine(p5,p1)
                #らせん_sweep
                helix=Part.makeHelix(p,2*p+H,D0/2,0,False)
                helix.Placement=App.Placement(App.Vector(0,0,-p),App.Rotation(App.Vector(0,0,1),0))
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c2= Part.makeCylinder(d1/2,4*p+H,Base.Vector(0,0,-2*p),Base.Vector(0,0,1),360)
                pipe=pipe.fuse(c2)
                c1=c1.cut(pipe)
            else:
                c2=Part.makeCylinder(D0/2,H)
                c1=c1.cut(c2)
            #面取り
            p1=(d1/2,0,0)
            p2=(d1/2,0,0.5)
            p3=(D0/2+0.5,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c3=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c3.Placement=App.Placement(App.Vector(0,0,H),App.Rotation(App.Vector(0,1,0),180))
            c2=c2.fuse(c3)
            c1=c1.cut(c2)
            #ナット溝
            y1=D3/2-T
            s0=math.atan(s/(2*y1))
            for i in range(4):
                c2=Part.makeBox(s,T,H,Base.Vector(-s/2,y1,0),Base.Vector(0,0,1))
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,0),90+i*90))
                c1=c1.cut(c2)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),180))
        elif st=='Bearing Washer':
            #座金
            s0=math.radians(25)
            x=(D5-D4)/2
            y=x*math.tan(s0)
            x2=t*math.sin(s0)
            x3=t*math.cos(s0)
            p1=(0,0,0)
            p2=(D4/2,0,0)
            p3=(D5/2,0,y)
            p4=(D5/2-x2,0,y+x3)
            p5=(D4/2,0,t)
            p6=(0,0,t)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            #軸穴
            k0=k-D0/2
            y=(D0/2-k0)*2
            c2= Part.makeCylinder(D0/2,t,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c3=Part.makeBox(E,y,t,Base.Vector(-E/2,k0,0),Base.Vector(0,0,1))
            c2=c2.cut(c3)
            c1=c1.cut(c2)
            #歯
            c2= Part.makeCylinder(D4/2,1.5*y,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            sk=float(360.0/n)
            for i in range(n):
                c3=Part.makeBox(s,2*x,1.5*y,Base.Vector(-s/2,0.9*D4/2,0),Base.Vector(0,0,1))
                c3.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,0),i*sk))
                c2=c2.fuse(c3)
            c4= Part.makeCylinder(D5/2,1.5*y,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c4=c4.cut(c2)
            c1=c1.cut(c4)
        doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)     
        obj.Shape=c1    