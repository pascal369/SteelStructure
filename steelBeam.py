# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import string
import math
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
#from prt_data.CSnap_data import paramCSnap
bType=['Lattice','Truss']
BShp=['40x40x3','40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
      '75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7','100x100x10','100x100x13']
LShp=['6x38','9x38','6x44','9x44','4.5x50','6x50','9x50','6x65','9x65','6x75',
      '9x75','6x90','9x90',]
TShp=['40x40x3','40x40x5','50x50x4','50x50x6','65x65x6','65x65x8','75x75x6','75x75x9',
      '75x75x9','75x75x12','90x90x7','90x90x10','90x90x13','100x100x7','100x100x10','100x100x13']

# 画面を並べて表示する
class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 460)
        Dialog.move(1000, 0)
        #type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 10, 100, 20))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 20))
        #玄材
        self.label_BShp = QtGui.QLabel('chordMember',Dialog)
        self.label_BShp.setGeometry(QtCore.QRect(10, 38, 100, 20))
        self.label_BShp.setStyleSheet("color: black;")
        self.comboBox_BShp = QtGui.QComboBox(Dialog)
        self.comboBox_BShp.setGeometry(QtCore.QRect(110, 38, 100, 20))

        #ラチス材
        self.label_LShp = QtGui.QLabel('latticeMember',Dialog)
        self.label_LShp.setGeometry(QtCore.QRect(10, 65, 100, 20))
        self.label_LShp.setStyleSheet("color: black;")
        self.comboBox_LShp = QtGui.QComboBox(Dialog)
        self.comboBox_LShp.setGeometry(QtCore.QRect(110, 65, 100, 20))

        #梁成
        self.label_H = QtGui.QLabel('beamHight',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 90, 100, 20))
        self.label_H.setStyleSheet("color: black;")
        self.spinBoxH=QtGui.QSpinBox(Dialog)
        self.spinBoxH.setGeometry(110, 92, 100, 30)
        self.spinBoxH.setMinimum(200)  # 最小値を0.0に設定
        self.spinBoxH.setMaximum(1000.0)  # 最大値を100.0に設定
        self.spinBoxH.setSingleStep(10)
        self.spinBoxH.setAlignment(QtCore.Qt.AlignCenter)

        #梁長
        self.label_L = QtGui.QLabel('span',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 125, 100, 20))
        self.label_L.setStyleSheet("color: black;")
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(110, 125, 100, 30)
        self.spinBoxL.setMinimum(1000)  # 最小値
        self.spinBoxL.setMaximum(20000)  # 最大値
        self.spinBoxL.setSingleStep(50) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)

        #ガセットプレート幅
        self.label_GPL = QtGui.QLabel('GPL width',Dialog)
        self.label_GPL.setGeometry(QtCore.QRect(10, 160, 100, 20))
        self.label_GPL.setStyleSheet("color: black;")
        self.le_GPL = QtGui.QLineEdit('150',Dialog)
        self.le_GPL.setGeometry(QtCore.QRect(110, 160, 100, 20))
        self.le_GPL.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(45, 198, 60, 20))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 198, 60, 20))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(45, 220, 185, 20))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 250, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_BShp.addItems(BShp)
        self.comboBox_BShp.setEditable(True)
        self.comboBox_type.addItems(bType)
        

        self.comboBox_LShp.addItems(LShp)
        self.comboBox_LShp.setEditable(True)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)

        self.comboBox_type.currentIndexChanged[int].connect(self.onType) 

        self.spinBoxH.valueChanged[int].connect(self.spinMoveH) 
        self.spinBoxH.valueChanged[int].connect(self.update) 
        self.spinBoxL.valueChanged[int].connect(self.spinMoveL) 
        self.spinBoxL.valueChanged[int].connect(self.update) 

        fname='LatticeBeam.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Beam_data",fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Steel Beam", None))
         
    def onType(self):
        global myType
        self.comboBox_LShp.clear()
        myType=self.comboBox_type.currentText() 
        if myType=='Lattice':
            self.comboBox_LShp.addItems(LShp)
        elif myType=='Truss':
            self.comboBox_LShp.addItems(TShp)    

    def spinMoveH(self):
         dL=self.spinBoxH.value()
         spreadsheet.set('H0',str(dL))
         App.ActiveDocument.recompute() 

    def spinMoveL(self):
         dL=self.spinBoxL.value()
         spreadsheet.set('L0',str(dL))
         App.ActiveDocument.recompute() 

    def read_data(self):
         global angle
         global AngleSteel
         global spreadsheet
         global genzai
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label=='AngleSteel' :
                         
                         angle=obj
                     elif obj.Label=='AngleSteel20':
                         AngleSteel=obj 
                     elif obj.Label=='genzai01':
                         genzai=obj        
                     elif obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_type.setCurrentText(spreadsheet.getContents('myType')[1:])
                         self.comboBox_BShp.setCurrentText(spreadsheet.getContents('shp')[1:])
                         self.comboBox_LShp.setCurrentText(spreadsheet.getContents('Lshp')[1:])
                         self.le_GPL.setText(spreadsheet.getContents('Gb0')) 
                         self.spinBoxH.setValue(int(spreadsheet.getContents('H0')))
                         self.spinBoxL.setValue(int(spreadsheet.getContents('L0')))

    def update(self):
         try:
            Bshp=self.comboBox_BShp.currentText()#玄材
            Lshp=self.comboBox_LShp.currentText()#ラチス材
            Bhight=self.spinBoxH.value()#
            Blength=self.spinBoxL.value()#
            Gb0=self.le_GPL.text()#
            if myType=='Lattice':
                angle.size = str(Bshp)
            elif myType=='Truss':
                AngleSteel.size =str(Bshp)
                genzai.size = str(Bshp)
            #玄材ゲージライン 
            if myType=='Lattice':
                j1=17
                j2=32
            elif myType=='Truss':
                j1=20
                j2=34
            for i in range(j1,j2):
                Bshp3=spreadsheet.getContents('A'+str(i))
                if Bshp==Bshp3[1:]:
                    break
            row_B=i
            
            if myType=='Lattice': 
                GL0=spreadsheet.getContents('D'+str(row_B)) 
                spreadsheet.set('GL0',GL0)
            elif myType=='Truss':
               gL0=spreadsheet.getContents('D'+str(row_B))
               spreadsheet.set('gL0',gL0)
            #ラチス個数
            if myType=='Lattice':
                if myType=='Lattice':
                    for n in range(1,100):
                        rp03=(float(Blength)-2*float(GL0))/(n+1)
                        if float(rp03)<float(Bhight):
                            break
                    rn0=n
                    if float(rp03)<float(Bhight):
                        rn0=rn0+1
            elif myType=='Truss':
               for n in range(1,100):
                rp03=(float(Blength)-2*float(gL0))/(n*2)
                #print(rp03,Bhight,n)
                if float(rp03)<=float(Bhight):
                    break
                m0=n
                if float(rp03)<float(Bhight):
                        m0=m0+1
            #print(rn0,rp03,Blength-20,)
            #ラチス材幅、板厚
            if myType=='Lattice':
                i1=34
                i2=46
            elif myType=='Truss':
                i1=20
                i2=34    
            for i in range(i1,i2):
                Lshp3=spreadsheet.getContents('A'+str(i))
                if Lshp==Lshp3[1:]:
                    break
            row_L=i  
            Lt0=spreadsheet.getContents('B'+str(row_L))     
            Lb0=spreadsheet.getContents('C'+str(row_L))   
            if myType=='Truss':
                H0=self.spinBoxH.value()
                L0=self.spinBoxL.value()
                gL1=spreadsheet.getContents('D'+str(row_L))
                gL0=spreadsheet.getContents('D'+str(row_B))#ゲージ 
                H00=float(H0)-2.0*float(gL0)
                rp0=H00
                sita=math.atan(H00*2/rp0)*57.3
                lz=float(gL0)*math.sin(sita/57.3)
                l0=lz/math.sin(sita/57.3)
                lx=l0*math.cos(sita/57.3)
                a0=spreadsheet.getContents('a0')
                AngleSteel.size=str(Lshp)
                rp0=spreadsheet.getContents('rp0')
                m0=int(m0)
                rp0=(float(L0)-float(Gb0))/(m0+1)
                sita=math.atan(H00*2/rp0)*57.3
                spreadsheet.set('rp0',str(rp0))
                spreadsheet.set('sita',str(sita))
                spreadsheet.set('gL1',gL1)
                spreadsheet.set('lx',str(lx))
                spreadsheet.set('lz',str(lz))
                spreadsheet.set('m0',str(m0-1))
                spreadsheet.set('a0',str(a0))
                spreadsheet.set('H0',str(H0))
                spreadsheet.set('L0',str(L0))
            spreadsheet.set('H0',str(Bhight))
            spreadsheet.set('shp',Bshp)
            spreadsheet.set('Lshp',Lshp)
            spreadsheet.set('Lb0',Lb0)
            try:
                spreadsheet.set('Gt0',Lt0)
            except:
                pass
            spreadsheet.set('Gb0',Gb0)
            if myType=='Truss':
                spreadsheet.set('m0',str(m0))
            elif myType=='Lattice':
                spreadsheet.set('rn0',str(rn0))
                
            App.ActiveDocument.recompute()
         except:
             pass     
                
    def create(self): 
         global myType
         doc = App.ActiveDocument
         myType=self.comboBox_type.currentText()
         if myType=='Lattice':
             fname='latticeBeam.FCStd'
         elif myType=='Truss':
             fname='trussBeam.FCStd'    
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Beam_data',fname) 
         
         # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
         
         # マージ実行
         Gui.ActiveDocument.mergeProject(joined_path)
         doc.recompute() # 一旦再計算して内部IDを確定させる
     
         # --- インポート後に増えたオブジェクトを特定 ---
         new_objs = [o for o in doc.Objects if o.Name not in old_obj_names]
         
         if not new_objs:
             print("Error: オブジェクトが読み込まれませんでした。")
             return
     
         #latticeBeamというラベルを持つものを優先的に探す
         move_target = None
         for o in new_objs:
             if "latticeBeam"  in o.Label or "latticeBeam"  in o.Name:
                 move_target = o
                 break
             elif "trussBeam" in o.Label or "trussBeam" in o.Name:
                 move_target = o
                 break
         
         # 見つからなければ、新しく入ってきた最初のオブジェクトをターゲットにする
         if not move_target:
             move_target = new_objs[0]
     
         view = Gui.ActiveDocument.ActiveView
         callbacks = {}
     
         def move_cb(info):
             pos = info["Position"]
             # 重要：ビュー平面上の3D座標を取得
             p = view.getPoint(pos)
             if move_target:
                 move_target.Placement.Base = p
                 #view.softRedraw()
     
         def click_cb(info):
             if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                 # コールバック解除
                 view.removeEventCallback("SoLocation2Event", callbacks["move"])
                 view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                 App.ActiveDocument.recompute()
                 print("Placed: " + move_target.Label)
     
         # イベント登録
         callbacks["move"] = view.addEventCallback("SoLocation2Event", move_cb)
         callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)    

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        