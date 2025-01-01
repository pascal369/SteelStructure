from fnmatch import translate
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
class UBlt:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        fdia=App.ActiveDocument.getObject(label).fdia
        Thread=App.ActiveDocument.getObject(label).Thread
        flange=App.ActiveDocument.getObject(label).flange
        stem_length=App.ActiveDocument.getObject(label).stem_length
        thread_length=App.ActiveDocument.getObject(label).thread_length
        
        def hexagon_bolt(self):
            global c00
            global c0
            global C
            global D0
            global l
            global L3
            global c1
            global c02
            global c03
            #global stem_length
            sa=ScrData.haikan_u[dia]
            size1=sa[0]
            #d0=float(size1[1:])
            if flange==False:
                C=sa[1]
            else:
                if fdia=='5k':
                    C=sa[4]   
                elif fdia=='7.5k' :
                    C=sa[5]  
                elif fdia=='10k':  
                    C=sa[6]    
            #stem_length=C/2
            L=sa[2]
            l=sa[3]
            sa=ScrData.regular[size1]
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
            H0=0.86625*p
            x=H1+H0/8
            y=x*math.tan(math.pi/6)
            r0=D0/2+H0/8
            a=p/2-y
            #ボルト部
            if flange==True:
                L3=stem_length-thread_length
                c1= Part.makeCylinder(D0/2,stem_length+C/2,Base.Vector(-C/2,0,0),Base.Vector(0,0,1),360)#ねじ部 
                c2= Part.makeCylinder(D0/2,stem_length+C/2,Base.Vector(C/2,0,0),Base.Vector(0,0,1),360)#ねじ部 
                c02= Part.makeCylinder(D0/2,L3,Base.Vector(-C/2,0,stem_length),Base.Vector(0,0,1),360)#軸部
                c03= Part.makeCylinder(D0/2,L3,Base.Vector(C/2,0,stem_length),Base.Vector(0,0,1),360)#軸部
            else:
                L3=stem_length-thread_length
                c1= Part.makeCylinder(D0/2,stem_length+C/2,Base.Vector(-C/2,0,0),Base.Vector(0,0,1),360)#ねじ部 
                c2= Part.makeCylinder(D0/2,stem_length+C/2,Base.Vector(C/2,0,0),Base.Vector(0,0,1),360)#ねじ部 
                c02= Part.makeCylinder(D0/2,L3,Base.Vector(-C/2,0,stem_length),Base.Vector(0,0,1),360)#軸部
                c03= Part.makeCylinder(D0/2,L3,Base.Vector(C/2,0,stem_length),Base.Vector(0,0,1),360)#軸部
            #Part.show(c02)
            p1=(-D0/2,0,0)
            p2=(-D0/2,0,z)
            p3=(-D0/2+z,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0,0),Base.Vector(0.0,0.0,1.0),360)
            
            #ねじ断面
            if Thread==True:
                p1=(D1/2,0,-a)
                p2=(D1/2,0,a)
                p3=(r0,0,p/2)
                p4=(r0,0,-p/2)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeLine(p3,p4)
                edge4 = Part.makeLine(p4,p1)
                #らせん_sweep
                L3=stem_length-thread_length
                if  L3>0:
                    helix=Part.makeHelix(p,p+thread_length,D0/2,0,False)
                    cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                else:
                    helix=Part.makeHelix(p,p+thread_length,D0/2,0,False)
                    cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                cutProfile.Placement=App.Placement(App.Vector(0,0,-0.5*p),App.Rotation(App.Vector(0,0,1),0))
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                if flange==True:
                    pipe.Placement=App.Placement(App.Vector(-C/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                else:
                    pipe.Placement=App.Placement(App.Vector(-C/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                for i in range(2):
                    if i==1:
                        if flange==True:
                            pipe.Placement=App.Placement(App.Vector(C/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                        else:
                            pipe.Placement=App.Placement(App.Vector(C/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                        c2=c2.cut(pipe)
                    c1=c1.cut(pipe)
                    c1.cut(c02)
                    c1.fuse(c02)
                c1=c1.fuse(c2)   
            else:
                c1=c1.fuse(c2)  
             
        #ボルト部
        hexagon_bolt(self)
        #トーラス
        c2=Part.makeTorus(C/2,D0/2,Base.Vector(0,0,0),Base.Vector(0,1,0),0,360,180)
        c2.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
        #Part.show(c2)
        #Part.show(c1)
        if flange==True:
            c2.translate(Base.Vector(0,0,stem_length+C/2))
            #pass
        else:    
            c2.translate(Base.Vector(0,0,stem_length+C/2))
        c01=c1.fuse(c2)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0) 
        obj.Shape=c01