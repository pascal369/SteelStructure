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
class SmlScrw:#05小ねじ
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        st=App.ActiveDocument.getObject(label).st
        Thread=App.ActiveDocument.getObject(label).Thread
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        sa=ScrData.regular[dia]
        p=sa[0]
        H1=sa[1]
        m=sa[6]
        m1=sa[7]
        s0=sa[8]
        e0=sa[9]
        D0=sa[2]
        D2=sa[3]
        D1=sa[4]
        dk=sa[5]
        z=sa[10]
        n=sa[11]
        H0=0.86625*p
        x=H1+H0/8
        y=x*math.tan(math.pi/6)
        r0=D0/2+H0/8
        a=p/2-y
        #ボルト部
        #らせん_sweep

        cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        c00=cb
        e=L1-L2
        #neck cut
        p1=((D1-1.1*a)/2,0,0)
        p2=((D1-1.1*a)/2,0,e)
        p3=(D0/2,0,e)
        p4=(D0/2,0,0)
        plist=[p1,p2,p3,p4,p1]
        w0=Part.makePolygon(plist)
        wface=Part.Face(w0)
        cbx=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        cbx.Placement=App.Placement(App.Vector(0,0,L2),App.Rotation(App.Vector(0,0,1),0))

        if Thread==True:
            p1=(D1/2,0,-a)
            p2=(D1/2-a/2,0,0)
            p3=(D1/2,0,a)
            p4=(r0,0,p/2)
            p5=(r0,0,-p/2)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2 = Part.makeLine(p3,p4)
            edge3 = Part.makeLine(p4,p5)
            edge4 = Part.makeLine(p5,p1)
            
            L3=L1-L2
            if  L3>0:
                helix=Part.makeHelix(p,L1-p,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            else:
                return
            cutProfile.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.cut(pipe)

        if st=='Pan_head':
            meishow='Pan_head_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.pan_head[dia]
            dk=float(sa[0])
            k=float(sa[1])
            r1=float(sa[2])
            r2=float(sa[3])
            t=float(sa[4])
            x1=r2/math.sqrt(2)
            x2=r2*(1-1/math.sqrt(2))
            x1=k-r2
            x2=r2/math.sqrt(2)
            x3=r2*(1-1/math.sqrt(2))
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(dk/2-r2,0,k)
            p4=(dk/2-x3,0,x1+x2)
            p5=(dk/2,0,x1)
            p6=(dk/2,0,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p1)
            w10=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            #c00=c00.cut(c01)
            c2=Part.makeBox(dk,n,t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)

        elif st=='Flat_head':
            meishow='Flat_head_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.flat_head[dia]
            dk=float(sa[0])
            k=float(sa[1])
            c=float(sa[2])
            t=float(sa[3])
            d1=D1
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(dk/2,0,k)
            p4=(dk/2,0,k-c)
            p5=(d1/2,0,0)
            plist=[p1,p2,p3,p4,p5,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,1.5*t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D1/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        elif st=='Round_flat_head':
            meishow='Round_flat_head_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.rflat_head[dia]
            dk=float(sa[0])
            k=float(sa[1])
            c=float(sa[2])
            t=float(sa[3])
            f=float(sa[4])
            rf=float(sa[5])
            d1=D1
            s=math.asin(dk/(2*rf))
            s0=math.degrees(s)
            x1=rf*math.cos(s)
            s15=math.radians(15)
            x2=rf*math.cos(s15)
            x=rf-x2
            x3=rf*math.sin(s15)
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(dk/2,0,k)
            p4=(dk/2,0,k-c)
            p5=(d1/2,0,0)
            p6=(0,0,x1-k)
            p7=(0,0,k+f)
            p8=(x3,0,rf-(x+x1-k))
            edge1 = Part.makeLine(p1,p7)
            edge2=Part.Arc(Base.Vector(p7),Base.Vector(p8),Base.Vector(p3)).toShape()
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p5)
            edge5 = Part.makeLine(p5,p1)
            w10=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,1.5*t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t+f),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D1/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        elif st=='Truss_screw':
            meishow='Truss_screw_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.truss_screw[dia]
            dk=float(sa[0])
            k=float(sa[1])
            c=float(sa[4])
            t=float(sa[3])
            r=float(sa[2])
            s15=math.radians(15)
            x1=r*math.sin(s15)
            x2=r*math.cos(s15)
            x=r-x2
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(x1,0,k-x)
            p4=(dk/2,0,c)
            p5=(dk/2,0,0)
            edge1 = Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
            edge3 = Part.makeLine(p4,p5)
            edge4 = Part.makeLine(p5,p1)
            w10=Part.Wire([edge1,edge2,edge3,edge4])
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,1.5*t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D0/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        elif st=='Binding_head':
            meishow='Binding_head_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.binding_screw[dia]
            dk=float(sa[0])
            k=float(sa[1])
            f=float(sa[2])
            t=float(sa[3])
            p1=(0,0,0)
            p2=(0,0,k+f)
            p3=(dk/3,0,k+0.8*f)
            p4=(dk/2,0,k)
            p5=(dk/2,0,0)
            edge1 = Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
            edge3 = Part.makeLine(p4,p5)
            edge4 = Part.makeLine(p5,p1)
            w10=Part.Wire([edge1,edge2,edge3,edge4])
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,1.5*t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t+f),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D0/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        elif st=='Round_screw':
            meishow='Round_screw_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.round_screw[dia]
            dk=float(sa[0])
            k=float(sa[1])
            r1=float(sa[2])
            r2=float(sa[3])
            t=float(sa[4])
            x1=r2/math.sqrt(2)
            x2=r2*(1-1/math.sqrt(2))
            x1=k-r2
            x2=r2/math.sqrt(2)
            x3=r2*(1-1/math.sqrt(2))
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(dk/2-r2,0,k)
            p4=(dk/2-x3,0,x1+x2)
            p5=(dk/2,0,x1)
            p6=(dk/2,0,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p1)
            w10=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D0/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        elif st=='Flat_screw':
            meishow='Flat_screw_' + dia + 'x' + str(L1) + '_'
            sa=ScrData.flat_screw[dia]
            dk=float(sa[0])
            k=float(sa[1])
            t=float(sa[2])
            p1=(0,0,0)
            p2=(0,0,k)
            p3=(dk/2,0,k)
            p4=(dk/2,0,0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
            c2.Placement=App.Placement(App.Vector(0,0,L1),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.fuse(c2)
            c2=Part.makeBox(dk,n,t)
            c2.Placement=App.Placement(App.Vector(-dk/2,-n/2,L1+k-t),App.Rotation(App.Vector(0,0,1),0))
            c00=c00.cut(c2)
            c2= Part.makeCylinder(D0/2,(L1-L2),Base.Vector(0,0,L2),Base.Vector(0,0,1),360)
            c00=c00.fuse(c2)
        c00=c00.cut(cbx)
        #Part.show(cbx)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c00