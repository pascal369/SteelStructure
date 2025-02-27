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
class Washer:
    def __init__(self, obj):
        self.Type = 'Angle'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        st=App.ActiveDocument.getObject(label).st
        #t=App.ActiveDocument.getObject(label).t
        #print('bbbbbbbbbbbbbb')
        def pwasher(self):
            global c01
            #print('ccccccccccccccc')
            p1=(d/2,0,0)
            p2=(d/2,0,t)
            p3=(D/2,0,t)
            p4=(D/2,0,0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            if st=='Spring_washer_general' or st=='Spring_washer_heavy':
                c01=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),359)
            else:
                c01=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)
        def cwasher(self):
            global c01
            p1=(-D/2,-D/2,0)
            p2=(-D/2,-D/2,t1)
            p3=(D/2,-D/2,t2)
            p4=(D/2,-D/2,0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c01=wface.extrude(Base.Vector(0,D,0))
            c02= Part.makeCylinder(d/2,2*t,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c01=c01.cut(c02)
        if st=='Small circle' :
            sa=ScrData.p_washer[dia]
            d=float(sa[0])
            D=float(sa[1])
            t=float(sa[2])
            pwasher(self)
            c1=c01
        elif st=='Polish circle':
            sa=ScrData.p_washer[dia]
            d=float(sa[3])
            D=float(sa[4])
            t=float(sa[5])
            pwasher(self)
            c1=c01
        elif st=='Common circle':
            sa=ScrData.p_washer[dia]
            d=float(sa[6])
            D=float(sa[7])
            t=float(sa[8])
            pwasher(self)
            c1=c01
        elif st=='Small corner':
            sa=ScrData.p_washer[dia]
            d=float(sa[9])
            D=float(sa[10])
            t=float(sa[11])
            t1=t
            t2=t
            cwasher(self)
            c1=c01
        elif st=='Large angle':
            sa=ScrData.p_washer[dia]
            d=float(sa[12])
            D=float(sa[13])
            t=float(sa[14])
            t1=t
            t2=t
            cwasher(self)
            c1=c01
        elif st=='Spring_washer_general':
            sa=ScrData.p_washer[dia]
            d=float(sa[15])
            D=float(sa[16])
            t=float(sa[17])
            pwasher(self)
            c1=c01
        elif st=='Spring_washer_heavy':
            sa=ScrData.p_washer[dia]
            d=float(sa[15])
            D=float(sa[19])
            t=float(sa[20])
            pwasher(self)
            c1=c01
        elif st=='Inclined_washer_5degrees':
            sa=ScrData.inc_washer[dia]
            d=float(sa[0])
            D=float(sa[1])
            t1=float(sa[2])
            t=float(sa[3])
            t2=float(sa[4])
            cwasher(self)
            c1=c01
        elif st=='Inclined_washer_8degrees':
            sa=ScrData.inc_washer[dia]
            d=float(sa[0])
            D=float(sa[1])
            t1=float(sa[5])
            t=float(sa[6])
            t2=float(sa[7])
            cwasher(self)
            c1=c01
        #print(t)
        #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        #obj.addProperty("App::PropertyFloat", "t",label).t=t  
        
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1
        #FreeCAD.ActiveDocument.recompute() 