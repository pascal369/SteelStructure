# -*- coding: utf-8 -*-
import os
import sys
import Import
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCADGui as Gui
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD, FreeCADGui
import FreeCAD as App

from Ladd_data import ParamLadder
from Ladd_data import ladderdata

class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        return

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(260, 600)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 15, 60, 22))
        self.label_type.setObjectName("label_type")
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 160, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.setEditable(True)
        #ステップ高
        self.label_st = QtGui.QLabel('stepHeight',Dialog)
        self.label_st.setGeometry(QtCore.QRect(10, 43, 60, 22))
        self.label_st.setStyleSheet("color: black;")
        self.comboBox_st = QtGui.QComboBox(Dialog)
        self.comboBox_st.setGeometry(QtCore.QRect(80, 38, 50, 22))
        self.comboBox_st.setObjectName("comboBox_st")
        #床面高さ
        self.label_size = QtGui.QLabel('floorHeight',Dialog)
        self.label_size.setGeometry(QtCore.QRect(10, 65, 60, 22))
        self.label_size.setStyleSheet("color: black;")

        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(80, 65, 60, 32)
        self.spinBoxL.setMinimum(100)  # 最小値
        self.spinBoxL.setMaximum(20000)  # 最大値
        self.spinBoxL.setValue(2500)  # 
        self.spinBoxL.setSingleStep(100) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)
        #heightStep
        self.label_step = QtGui.QLabel('step',Dialog)
        self.label_step.setGeometry(QtCore.QRect(145, 65, 50, 22))
        self.label_step.setStyleSheet("color: black;")
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(180, 65, 40, 22))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        #Create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 160, 60, 22))
        #upDate
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 160, 60, 22))
        #import
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(30, 185, 190, 22))

        #手すり高
        self.label_l = QtGui.QLabel('railingHeight',Dialog)
        self.label_l.setGeometry(QtCore.QRect(10, 115, 81, 22))
        self.label_l.setAlignment(QtCore.Qt.AlignLeft)
        self.label_l.setStyleSheet("color: black;")
        self.lineEdit_l = QtGui.QLineEdit('1100',Dialog)
        self.lineEdit_l.setGeometry(QtCore.QRect(80, 110, 50, 22))
        self.lineEdit_l.setAlignment(QtCore.Qt.AlignCenter)

        #比重
        self.mtrl = QtGui.QLabel('Specific gravity of material',Dialog)
        self.mtrl.setGeometry(QtCore.QRect(10, 135, 150, 22))
        self.mtrl.setStyleSheet("color: black;")
        self.le_mtrl = QtGui.QLineEdit('7.85',Dialog)
        self.le_mtrl.setGeometry(QtCore.QRect(180, 135, 40, 22))
        self.le_mtrl.setAlignment(QtCore.Qt.AlignCenter)

        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 220, 200, 400))
        self.img.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslateUi(Dialog)
        self.comboBox_type.addItems(ladderdata.type)
        self.comboBox_st.addItems(ladderdata.step_h)
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)
        self.spinBoxL.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.spinMove)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Ladder", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None))

    def spinMove(self):
        try:
            type=self.comboBox_type.currentText()
            step=self.le_step.text()
            self.spinBoxL.setSingleStep(int(step)) 
            L=self.spinBoxL.value()    
            ladder.FloorHeight=(L)
            ladder.type=type
            App.ActiveDocument.recompute() 
        except:
            return    

    def read_data(self):
        global ladder
        selection = Gui.Selection.getSelection()
        for obj in selection:
            if obj.Label[:7]=="LadderA":
                ladder=obj
            elif obj.Label[:17]=="LadderA with cage":
                ladder=obj  
            elif obj.Label[:7]=="LadderB":
                ladder=obj  
            elif obj.Label[:17]=="LadderB with cage":
                ladder=obj        
            L=int(ladder.FloorHeight)
            type=ladder.type
            self.spinBoxL.setValue(int(L))
            self.comboBox_type.setCurrentText(type)
           
    def on_type(self):
        key = self.comboBox_type.currentText()[:2]
        #self.label_type.setText(QtGui.QApplication.translate("Dialog", str(key), None))
        if key=='00':
            pic='ladder_00.jpg'
        elif key=='01':
            pic='ladder_01.jpg'
        elif key=='02':
            pic='ladder_02.jpg'
        elif key=='03':
            pic='ladder_03.jpg'

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Ladd_data",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))
    def create(self):
        key = self.comboBox_type.currentText()[:2]
        h=float(self.comboBox_st.currentText())#ステップ高
        L=float(self.lineEdit_l.text())#手すり高
        L0=int(self.spinBoxL.value())#床面高さ
        g0=float(self.le_mtrl.text())
        if key=='00' or key=='02':
            if key=='00':
                label='LadderA'
            else:
                label='LadderB'
            JPN='ラダー'    
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN  
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=ladderdata.type
            i=self.comboBox_type.currentIndex()
            obj.type=ladderdata.type[i] 
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyFloat", "StepHeight",label).StepHeight=h
            obj.addProperty("App::PropertyFloat", "RailingHeight",label).RailingHeight=L
            obj.addProperty("App::PropertyFloat", "FloorHeight",label).FloorHeight=L0
            ParamLadder.ParametricLadder(obj) 
            Gui.SendMsgToActiveView("ViewFit")
            obj.ViewObject.Proxy=0

        elif key=='01' or key=='03':
            if key=='01':
                label='LadderA with cage'
            else:
                label='LadderB with cage'
            
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=ladderdata.type
            i=self.comboBox_type.currentIndex()
            obj.type=ladderdata.type[i] 
            obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyFloat", "StepHeight",label).StepHeight=h
            obj.addProperty("App::PropertyFloat", "RailingHeight",label).RailingHeight=L
            obj.addProperty("App::PropertyFloat", "FloorHeight",label).FloorHeight=L0
            
        
            ParamLadder.ParametricLadder(obj) 
            obj.ViewObject.Proxy=0

        try:        
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            Standard='FloorHeight='+str(obj.FloorHeight)
            obj.Standard=Standard
        except:
            pass  

        # 1. 作成したアセンブリを確実に取得
        assy_name = obj.Name + "_Assy"
        target_assy = App.ActiveDocument.getObject(assy_name)
        # もしアセンブリがまだなければ、階段本体を動かすようにフォールバック
        move_target = target_assy if target_assy else obj
        view = Gui.ActiveDocument.ActiveView
        
        # ドラッグ中、元の位置にあるアセンブリを一時的に隠すと見やすくなります
        # move_target.ViewObject.Visibility = False

        callbacks = {}
        # --- マウス移動時の処理 ---
        def move_cb(info):
            pos = info["Position"]
            p = view.getPoint(pos)
            # アセンブリの座標をマウス位置に即座に反映
            move_target.Placement.Base = p
            # 表示を更新（これがないと動いて見えない場合があります）
            view.softRedraw()

        # --- クリック時の処理 ---
        def click_cb(info):
            if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                # タイマーを使って終了処理を呼ぶ（FreeCADの安定のため）
                QtCore.QTimer.singleShot(0, finish)

        # --- 終了処理 ---
        def finish():
            try:
                view.removeEventCallback("SoLocation2Event", callbacks["move"])
                view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
            except:
                pass
            
            move_target.ViewObject.Visibility = True
            App.ActiveDocument.recompute()
            FreeCAD.Console.PrintMessage("配置が完了しました。\n")

        # --- イベントの登録 ---
        callbacks["move"] = view.addEventCallback("SoLocation2Event", move_cb)
        callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)      


class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        




