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


CDia=['Post','ShapedSteel','SteelPlate','SteelStairs','Ladder','Handrail',]
Stair=['for 2F','2F or higher','spiral staircase with stanchions','spiral staircase']
Ladder=['LadderA','LadderA with cage','LadderB','LadderB with cage']
Handrail=['Straight line','Coner with end','Coner','Circular_arc','Edge','Channel']
Post=['Pst_H','Pst_L','Pst_C','Pst_SQ','Pst_Pip',]
ShpStl=['Angle','Channel','H_Wide','H_medium','H_thin','I_beam','CT','STK',
        'LightAngle','LightChannel','RipChannel','SQ_Pipe']

class Ui_Dialog(object):
    global flag00
    flag00=0
    print(flag00)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 410)
        Dialog.move(1500, 0)
        #部材　Element
        self.label_element = QtGui.QLabel(Dialog)
        self.label_element.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_element = QtGui.QComboBox(Dialog)
        self.comboBox_element.setGeometry(QtCore.QRect(80, 10, 200, 22))
        #部材2　Element2
        self.label_element2 = QtGui.QLabel(Dialog)
        self.label_element2.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_element2 = QtGui.QComboBox(Dialog)
        self.comboBox_element2.setGeometry(QtCore.QRect(80, 35, 200, 22))

        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 100, 22))

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(80, 85, 100, 23))
        self.pushButton_m.setObjectName("pushButton")  
        #質量集計
        self.pushButton_m2 = QtGui.QPushButton('massTally',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(180, 85, 100, 23))
        self.pushButton_m2.setObjectName("pushButton")
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(80, 115, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(180, 115, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(80, 145, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(180, 142, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 140, 250, 250))
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_element.addItems(CDia)
        self.comboBox_element.setCurrentIndex(1)
        self.comboBox_element.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_element.setCurrentIndex(0)

        self.comboBox_element.currentIndexChanged[int].connect(self.onDia2)

        self.comboBox_element2.setCurrentIndex(1)
        self.comboBox_element2.currentIndexChanged[int].connect(self.onDia2)
        self.comboBox_element2.setCurrentIndex(0)

        

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally2)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "SteelStructure", None))
        self.label_element.setText(QtGui.QApplication.translate("Dialog", "Element", None))  
        self.label_element2.setText(QtGui.QApplication.translate("Dialog", "Element2", None))   
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Execution", None))  

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
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g

    def massTally2(self):
        #def get_object_mass():
        doc = App.ActiveDocument
        objects = doc.Objects
        #print('aaa')
        
        mass_list = []
        
        for obj in objects:
            if Gui.ActiveDocument.getObject(obj.Name).Visibility:
                if obj.isDerivedFrom("Part::Feature"):
                    if hasattr(obj, "mass"):
                        # Add the object's name, count, and mass to the list
                        mass_list.append([obj.Label, 1, obj.mass])
                else:
                     pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        print(doc_path)
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Object Name",'Count', "Mass[kg]"])
            writer.writerows(mass_list) 
                 
    def onDia(self):
         global key
         
         flag00=0 
         self.comboBox_element2.clear()
         key=self.comboBox_element.currentIndex()
         if key==0:#Post'
              self.comboBox_element2.show()
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
         try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "StlStu_data",pic)
            self.img.setPixmap(QtGui.QPixmap(joined_path))   
         except:
             pass                  

    def create(self): 
         if key==0:
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, 'StlStu_data',fname) 
                try:
                    Gui.ActiveDocument.mergeProject(joined_path)
                except:
                    doc=App.newDocument()
                    Gui.ActiveDocument.mergeProject(joined_path)    
                App.ActiveDocument.recompute()  
                Gui.ActiveDocument.ActiveView.fitAll()
                pass       
         elif key==1:
                import Shaped_steel

         elif key==2:
              import Pln_shape
         elif key==3:
             if key2==0:
                  import SteelStair2
             elif key2==1:
                  import SteelStairs 
             elif key2==2:
                  import SplStairCase   
             elif key2==3:
                  import SplStairCaseNoProp      
         elif key==4:
                import Ladder
                
         elif key==5:
                import Handrails
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        
           