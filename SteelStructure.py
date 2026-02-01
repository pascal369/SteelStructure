# -*- coding: utf-8 -*-
import os
import sys
import csv
import pathlib
import subprocess
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import importlib
import FreeCAD,Part

CDia=['Post','ShapedSteel','SteelPlate','SteelStairs','Ladder','Handrail','Trestle',
      'SteelBrace','LatticeBeam','TrussBeam','TurnBackle','accodionGate','grating',]
Stair=['for 2F','2F or higher','spiral staircase with stanchions','spiral staircase']
Ladder=['LadderA','LadderA with cage','LadderB','LadderB with cage']
Handrail=['Straight line','Coner with end','Coner','Circular_arc','Edge','Channel']
Post=['Pst_H','Pst_L','Pst_C','Pst_SQ','Pst_Pip',]
ShpStl=['Angle','Channel','H_Wide','H_medium','H_thin','I_beam','CT','STK',
        'LightAngle','LightChannel','RipChannel','SQ_Pipe']
Trestle=['type01','type02','type03','type04','type05']
turnBackle_data=['turnBackle','forkEnd_L','forkEnd_R','turnBackle_Assy']
lang=['English','Japanese']
mater=['SS41','SUS304','S45C','PVC','Neoprene rubber']
class Ui_Dialog(object):
    global flag00
    flag00=0
    #print(flag00)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(370, 530)
        Dialog.move(1000, 0)
        #部材　Element
        self.label_element = QtGui.QLabel('Element',Dialog)
        self.label_element.setGeometry(QtCore.QRect(5, 8, 100, 22))
        self.label_element.setStyleSheet("color: black;")
        self.comboBox_element = QtGui.QComboBox(Dialog)
        self.comboBox_element.setGeometry(QtCore.QRect(80, 8, 130, 22))
        self.comboBox_element.setEditable(True)
        self.comboBox_element.lineEdit().setAlignment(QtCore.Qt.AlignCenter)  
        #言語
        self.pushButton_la=QtGui.QPushButton('language',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(220, 8, 125, 22))
        self.comboBox_lan = QtGui.QComboBox(Dialog)
        self.comboBox_lan.setGeometry(QtCore.QRect(220, 35, 125, 22))
        self.comboBox_lan.setEditable(True)
        self.comboBox_lan.lineEdit().setAlignment(QtCore.Qt.AlignCenter)  

        #部材2　Element2
        self.label_element2 = QtGui.QLabel('Element2',Dialog)
        self.label_element2.setGeometry(QtCore.QRect(8, 35, 100, 22))
        self.label_element2.setStyleSheet("color: black;")
        self.comboBox_element2 = QtGui.QComboBox(Dialog)
        self.comboBox_element2.setGeometry(QtCore.QRect(80, 35, 130, 22))

        #jpn text
        self.pushButton_jpn = QtGui.QPushButton('Jpn Text',Dialog)
        self.pushButton_jpn.setGeometry(QtCore.QRect(80, 62, 50, 22))
        self.le_jpn = QtGui.QLineEdit(Dialog)
        self.le_jpn.setGeometry(QtCore.QRect(175, 62, 170, 22))
        self.le_jpn.setAlignment(QtCore.Qt.AlignCenter)  

        #standard
        self.pushButton_st = QtGui.QPushButton('Standard',Dialog)
        self.pushButton_st.setGeometry(QtCore.QRect(80, 85, 50, 22))
        self.le_st = QtGui.QLineEdit(Dialog)
        self.le_st.setGeometry(QtCore.QRect(175, 85, 170, 22))
        self.le_st.setAlignment(QtCore.Qt.AlignCenter) 

        #material
        self.pushButton_mt = QtGui.QPushButton('Material',Dialog)
        self.pushButton_mt.setGeometry(QtCore.QRect(80, 110, 50, 22))
        self.comboBox_mt = QtGui.QComboBox(Dialog)
        self.comboBox_mt.setGeometry(QtCore.QRect(175, 108, 170, 22))
        self.comboBox_mt.setEditable(True)
        self.comboBox_mt.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

         #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(80, 135, 100, 22))
        self.pushButton_m.setObjectName("pushButton")  

        #質量集計
        self.pushButton_m2 = QtGui.QPushButton('massTally_spreadsheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(185, 135, 160, 22))
        self.pushButton_m2.setObjectName("pushButton")  

        #count
        self.pushButton_ct = QtGui.QPushButton('Count',Dialog)
        self.pushButton_ct.setGeometry(QtCore.QRect(80, 160, 100, 22))
        self.le_ct = QtGui.QLineEdit(Dialog)
        self.le_ct.setGeometry(QtCore.QRect(185, 160, 50, 22))
        self.le_ct.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_ct.setText('1')

        #massUpdate
        self.pushButton_mUp = QtGui.QPushButton('massUpdate',Dialog)
        self.pushButton_mUp.setGeometry(QtCore.QRect(235, 185, 110, 22))

        #sketchLength
        self.pushButtonS = QtGui.QPushButton('SketchLength',Dialog)
        self.pushButtonS.setGeometry(QtCore.QRect(235, 210, 110, 22))
        self.pushButtonS.setObjectName("pushButton")

        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(80, 185, 100, 22))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(182, 185, 50, 22))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')  

        #密度
        self.pushButton_gr = QtGui.QPushButton('SpecificGravity',Dialog)
        self.pushButton_gr.setGeometry(QtCore.QRect(80, 210, 100, 22))
        self.pushButton_gr.setObjectName("pushButton")  
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(182, 210, 50, 22))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')  

         #実行
        self.pushButton = QtGui.QPushButton('Execution',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 240, 100, 22))  

        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(80, 270, 250, 250))
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_element.addItems(CDia)
        self.comboBox_element.setCurrentIndex(1)
        self.comboBox_element.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_element.setCurrentIndex(0)

        self.comboBox_element.currentIndexChanged[int].connect(self.onDia2)

        self.comboBox_element2.setCurrentIndex(1)
        self.comboBox_element2.currentIndexChanged[int].connect(self.onDia2)
        self.comboBox_element2.setCurrentIndex(0)

        self.comboBox_lan.addItems(lang)
        self.comboBox_mt.addItems(mater)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
        QtCore.QObject.connect(self.pushButton_ct, QtCore.SIGNAL("pressed()"), self.countCulc)
        QtCore.QObject.connect(self.pushButton_jpn, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QObject.connect(self.pushButton_st, QtCore.SIGNAL("pressed()"), self.standard)
        QtCore.QObject.connect(self.pushButton_mt, QtCore.SIGNAL("pressed()"), self.material)
        QtCore.QObject.connect(self.pushButtonS, QtCore.SIGNAL("pressed()"), self.sketchLength)
        QtCore.QObject.connect(self.pushButton_mUp, QtCore.SIGNAL("pressed()"), self.massUpdate)
        QtCore.QObject.connect(self.pushButton_gr, QtCore.SIGNAL("pressed()"), self.specificGr)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "SteelStructure", None))

    def massUpdate(self):
        doc = App.ActiveDocument
        for i,obj in enumerate(doc.Objects):
            
            try:
                if obj.count > 0 :
                    obj.mass=obj.Shape.Volume*obj.g0/10**6
            except:
                pass

    def specificGr(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        try:
            obj.addProperty("App::PropertyFloat", "g0",label)
            obj.g0=g0
        except:
            obj.g0=g0 

    def japan(self):
        return
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label=obj.Label
        JPN=self.le_jpn.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN

    def standard(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        Standard=self.le_st.text()
        try:
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            obj.Standard=Standard
        except:
            obj.Standard=Standard     

    def material(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        material=self.comboBox_mt.currentText()
        #print(material)
        try:
            obj.addProperty("App::PropertyString", 'material','material')
            obj.material=material
        except:
            obj.material=material   

    def countCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        count=int(self.le_ct.text())
        try:
            obj.addProperty("App::PropertyFloat", "count",label)
            obj.count=count
        except:
            obj.count=count    

    def sketchLength(self):
        obj = Gui.Selection.getSelection()[0]  # 選択されたオブジェクトを取得
        if obj is None or obj.TypeId != "Sketcher::SketchObject":
            FreeCAD.Console.PrintError("スケッチを選択してください\n")
        else:
            total_length = 0.0
            for geo in obj.Geometry:
                if isinstance(geo, (Part.LineSegment, Part.ArcOfCircle )):
                           total_length += geo.length()
            FreeCAD.Console.PrintMessage(f"スケッチ '{obj.Label}' の合計エッジ長: {total_length} mm\n")

    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
         
    def massCulc(self):
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        try:
            g=obj.Shape.Volume*g0*1000/10**9 
        except:
             pass
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g

    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        spreadsheet = doc.getObject("Parts_List") 
        if spreadsheet is None:
            spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
        
        # ヘッダー行を記入
        gengo=self.comboBox_lan.currentText()
        if gengo=='Japanese':
            headers = ['No','名称','材質','規格', '数量','単重[kg]','重量[kg]']
        elif gengo=='English':
            headers = ['No','Name','Material','Standard', 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
            spreadsheet.set(f"G{1}", headers[6])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if hasattr(obj, "count") and obj.count > 0:
                try:
                    spreadsheet.set(f"A{row}", str(row-1))  # No
                    if gengo=='English':
                        n=obj.count
                        spreadsheet.set(f'B{row}',obj.Label)    
                    elif gengo=='Japanese':
                        #
                        n=obj.count
                        try:
                            spreadsheet.set(f"B{row}", obj.JPN) 
                        except:
                            spreadsheet.set(f"B{row}", obj.Base_JPN)  
                    try:
                        spreadsheet.set(f"C{row}", obj.material)
                    except:
                        pass
                    try:
                        spreadsheet.set(f"D{row}", obj.Standard)
                    except:
                        pass
                    
                    spreadsheet.set(f"E{row}", f"{n:.2f}")   # count
                    try:
                        obj.mass=obj.Shape.Volume*obj.g0/10**6
                    except:
                        #obj.mass=obj.Shape.Volume/10**6
                        pass
                    spreadsheet.set(f"F{row}", f"{obj.mass:.2f}")  # unit
                    spreadsheet.set(f"G{row}", f"{obj.mass*n:.2f}")  # mass
                except:
                    pass    
                s=obj.mass*n+s
                row += 1
                
            spreadsheet.set(f'G{row}',str(s))
        App.ActiveDocument.recompute()
                 
    def onDia(self):
         global key
         flag00=0 
         self.comboBox_element2.clear()
         key=self.comboBox_element.currentIndex()
         if key==0:#Post'
              self.comboBox_element2.hide()
              self.comboBox_element2.addItems(Post)  
         elif key==1:#ShapeSteel
              self.comboBox_element2.hide()   
         elif key==2:#SteelPlate
              self.comboBox_element2.hide()   
         elif key==3:#SteelStairs
              self.comboBox_element2.show()
              self.comboBox_element2.addItems(Stair)   
         elif key==4:#Ladder
              pic='01_Ladder.PNG'
              self.comboBox_element2.hide()   
         elif key==5:#Handrail
              pic='02_handrail.png'
              self.comboBox_element2.hide() 
         elif key==6:#PipeSuport
              pic='trestle01.png'
              self.comboBox_element2.hide()  
         elif key==7:#steelBrace
              pic='steelBracee01.png'
              self.comboBox_element2.hide()  
         elif key==8:#latticeBeam
              pic='LatticeBeam.png'
              self.comboBox_element2.hide()  
         elif key==9:#trussBeam
              pic='trussBeam.png'
              self.comboBox_element2.hide() 
         elif key==10:#turnBackle
              pic='turnBackle.png'
              self.comboBox_element2.hide()     
         elif key==11:#accodionGate
              pic='accodionGate.png'
              self.comboBox_element2.hide()  
         elif key==12:#grating
              pic='grating.png'
              self.comboBox_element2.hide() 

    def onDia2(self):
         global fname
         global key2
         key2=self.comboBox_element2.currentIndex()
         if key==0:#Post
            if key2==0:
                 fname='03_Pst_H.FCStd'  
                 pic='03_Pst_H.png'
            elif key2==1:
                fname='03_Pst_L.FCStd'  
                pic='03_Pst_L.png'
            elif key2==2:
                fname='03_Pst_C.FCStd' 
                pic='03_Pst_C.png'
            elif key2==3:
                fname='03_Pst_SQ.FCStd'  
                pic='03_Pst_SQ.png'
            elif key2==4:
                fname='03_Pst_Pip.FCStd'  
                pic='03_Pst_Pip.png'  
         elif key==1:
            pic='04_shapedSteel.png'
         elif key==2:
             pic='05_plnShape.png'
         elif key==3:
            if key2==0:
                pic='00_StlStr.png'   
            elif key2==1:
                pic='00_StlStr2.png'
            elif key2==2:
                pic='00_SplStrCasePost.png'
            elif key2==3:
                pic='00_SplStrCase.png'
         elif key==4:  
              pic='01_Ladder.png' 
         elif key==5:  
              pic='02_handrail.png' 
         elif key==6:  
              pic='trestle01.png' 
         elif key==7:  
              pic='steelBrace01.png'   
         elif key==8:  
              pic='LatticeBeam.png'  
         elif key==9:  
              pic='trussBeam.png' 
         elif key==10:  
              pic='turnBackle.png'   
         elif key==11:  
              pic='accodionGate.png'
         elif key==12:  
              pic='grating.png'   

         try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "StlStu_data",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))   
         except:
             pass                  

    def create(self): 
         
         key=self.comboBox_element.currentIndex()
         key2=self.comboBox_element2.currentIndex()
         
         if key==0:#Post
              import importlib
              import sys
              if 'postAssy' not in sys.modules:
                   import postAssy
              else:
                   importlib.reload(sys.modules['postAssy'])

         elif key==1:#shapedSteel
                import importlib
                import sys
                if 'Shaped_steelS' not in sys.modules:
                     import Shaped_steelS
                else:
                     importlib.reload(sys.modules['Shaped_steelS'])
         elif key==2:#steelPlate
              import importlib
              import sys
              if 'Pln_shape' not in sys.modules:
                   import Pln_shape
              else:
                   importlib.reload(sys.modules['Pln_shape'])
         elif key==3:#steelStairs
             if key2==0:#2階用
                  import importlib
                  import sys
                  if 'SteelStair2' not in sys.modules:
                      import SteelStair2
                  else:
                      importlib.reload(sys.modules['SteelStair2'])
             elif key2==1:#一般階用
                  import importlib
                  import sys 
                  if 'SteelStairs' not in sys.modules:
                      import SteelStairs
                  else:
                      importlib.reload(sys.modules['SteelStairs'])  
             elif key2==2:
                  import importlib
                  import sys 
                  if 'SplStairCase' not in sys.modules:
                      import SplStairCase
                  else:
                      importlib.reload(sys.modules['SplStairCase'])  
             elif key2==3:
                  import importlib
                  import sys 
                  if 'SplStairCaseNoProp' not in sys.modules:
                      import SplStairCaseNoProp
                  else:
                      importlib.reload(sys.modules['SplStairCaseNoProp'])
         elif key==4:#ladder
                import importlib
                import sys 
                if 'Ladder' not in sys.modules:
                    import Ladder
                else:
                    importlib.reload(sys.modules['Ladder'])
         elif key==5:#handrails
                import importlib
                import sys 
                if 'Handrails' not in sys.modules:
                    import Handrails
                else:
                    importlib.reload(sys.modules['Handrails'])
         elif key==6:#Trestle
                import importlib
                import sys 
                if 'Trestle' not in sys.modules:
                    import Trestle
                else:
                    importlib.reload(sys.modules['Trestle'])
         elif key==7:#steelBrace
                import importlib
                import sys 
                if 'steelBrace' not in sys.modules:
                    import steelBrace
                else:
                    importlib.reload(sys.modules['steelBrace']) 
         elif key==8:#latticeBeam
                import importlib
                import sys 
                if 'latticeBeam' not in sys.modules:
                    import latticeBeam
                else:
                    importlib.reload(sys.modules['latticeBeam'])
         elif key==9:#trussBeam
                import importlib
                import sys 
                if 'trussBeam' not in sys.modules:
                    import trussBeam
                else:
                    importlib.reload(sys.modules['trussBeam'])
         elif key==10:#turnBackle
                import importlib
                import sys 
                if 'turnBackleS' not in sys.modules:
                    import turnBackleS
                else:
                    importlib.reload(sys.modules['turnBackleS'])
                
         elif key==11:#accodionGate   
                #import accodionGate 

                import importlib
                import sys 
                if 'accodionGate' not in sys.modules:
                    import accodionGate
                else:
                    importlib.reload(sys.modules['accodionGate'])
                
         elif key==12:#grating
                #import grating 
                import importlib
                import sys 
                if 'grating' not in sys.modules:
                    import grating
                else:
                    importlib.reload(sys.modules['grating'])
                


             

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        
           