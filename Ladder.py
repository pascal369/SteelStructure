# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import FreeCADGui as Gui
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
        Dialog.resize(260, 500)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 15, 60, 12))
        self.label_type.setObjectName("label_type")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 160, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        #ステップ高
        self.label_st = QtGui.QLabel(Dialog)
        self.label_st.setGeometry(QtCore.QRect(10, 40, 60, 12))
        self.label_st.setObjectName("label_st")
        self.comboBox_st = QtGui.QComboBox(Dialog)
        self.comboBox_st.setGeometry(QtCore.QRect(80, 35, 50, 22))
        self.comboBox_st.setObjectName("comboBox_st")
        #床面高さ
        self.label_size = QtGui.QLabel(Dialog)
        self.label_size.setGeometry(QtCore.QRect(10, 65, 60, 12))
        self.label_size.setObjectName("label_size")
        self.lineEdit_size = QtGui.QLineEdit(Dialog)
        self.lineEdit_size.setGeometry(QtCore.QRect(80, 60, 50, 22))
        self.lineEdit_size.setObjectName("lineEdit_size")
        self.lineEdit_size.setAlignment(QtCore.Qt.AlignCenter)
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 84, 61, 22))
        self.pushButton.setObjectName("pushButton")
        #手すり高
        self.label_l = QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(10, 90, 81, 20))
        self.label_l.setAlignment(QtCore.Qt.AlignLeft)
        self.label_l.setObjectName("label_l")
        self.lineEdit_l = QtGui.QLineEdit(Dialog)
        self.lineEdit_l.setGeometry(QtCore.QRect(80, 85, 50, 20))
        self.lineEdit_l.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_l.setObjectName("lineEdit_l")
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(30, 100, 200, 400))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.retranslateUi(Dialog)
        self.comboBox_type.addItems(ladderdata.type)
        self.comboBox_st.addItems(ladderdata.step_h)
        #self.comboBox_sp.addItems(spt_n)
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)
        self.lineEdit_l.setText(QtGui.QApplication.translate("Dialog", str('1100'), None))
        self.lineEdit_size.setText(QtGui.QApplication.translate("Dialog", str('2500'), None))
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Ladder", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None))
        self.label_st.setText(QtGui.QApplication.translate("Dialog", "Step height", None))
        self.label_size.setText(QtGui.QApplication.translate("Dialog", "Floor height", None))
        self.label_l.setText(QtGui.QApplication.translate("Dialog", "Railing height", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))

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
        L0=int(self.lineEdit_size.text())#床面高さ
        
        if key=='00' or key=='02':
            if key=='00':
                label='LadderA'
            else:
                label='LadderB'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyEnumeration", "type",label)
            obj.type=ladderdata.type
            i=self.comboBox_type.currentIndex()
            obj.type=ladderdata.type[i] 
            obj.addProperty("App::PropertyFloat", "StepHight",label).StepHight=h
            obj.addProperty("App::PropertyFloat", "RailingHight",label).RailingHight=L
            obj.addProperty("App::PropertyFloat", "FloorHight",label).FloorHight=L0
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
            obj.addProperty("App::PropertyFloat", "StepHight",label).StepHight=h
            obj.addProperty("App::PropertyFloat", "RailingHight",label).RailingHight=L
            obj.addProperty("App::PropertyFloat", "FloorHight",label).FloorHight=L0
            ParamLadder.ParametricLadder(obj) 
            obj.ViewObject.Proxy=0


class Main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)





