import os
import sys
import FreeCAD
import FreeCADGui
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from shpst_data import ShpstData
import Draft,DraftGui
Post=['Pst_H','Pst_L','Pst_C','Pst_SQ','Pst_Pipe',]
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        Dialog.move(1000, 0)
        #shapeSteel
        self.label_shp = QtGui.QLabel('shapeSteel',Dialog)
        self.label_shp.setGeometry(QtCore.QRect(10, 0, 60, 12))
        self.comboBox_Shp = QtGui.QComboBox(Dialog)
        self.comboBox_Shp.setGeometry(QtCore.QRect(80, 0, 200, 22))
        #size
        self.label_shp = QtGui.QLabel('shapeSteel',Dialog)
        self.label_shp.setGeometry(QtCore.QRect(10, 25, 60, 12))
        self.comboBox_Size = QtGui.QComboBox(Dialog)
        self.comboBox_Size.setGeometry(QtCore.QRect(80, 25, 200, 22))
        #hight
        self.label_H = QtGui.QLabel('H[mm',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 50, 60, 12))
        self.lineEdit_H = QtGui.QLineEdit('500',Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(80, 50, 200, 22))
        self.lineEdit_H.setAlignment(QtCore.Qt.AlignCenter)
        
        #basePlate thickness
        self.label_t = QtGui.QLabel('t[mm',Dialog)
        self.label_t.setGeometry(QtCore.QRect(10, 75 ,60, 12))
        self.lineEdit_t = QtGui.QLineEdit('9',Dialog)
        self.lineEdit_t.setGeometry(QtCore.QRect(80, 75, 200, 22))
        self.lineEdit_t.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 100, 200, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 125, 200, 22))
        #import
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 150, 200, 22))


        self.comboBox_Shp.setEditable(True)
        self.comboBox_Size.setEditable(True)

        self.comboBox_Shp.addItems(Post)

        self.comboBox_Shp.setCurrentIndex(1)
        self.comboBox_Shp.currentIndexChanged[int].connect(self.onShape)
        self.comboBox_Shp.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "post", None))
    def onShape(self):
        key=self.comboBox_Shp.currentText()
        if key=='Pst_H':
            ta=ShpstData.H_ss_w_size
        elif key=='Pst_L':
            ta=ShpstData.angle_ss_size
        elif key=='Pst_C':
            ta=ShpstData.channel_ss_size 
        elif key=='Pst_SQ':
            ta=ShpstData.Square_pipe_ss_size
        elif key=='Pst_Pipe':
            ta=ShpstData.STK_ss_size

        self.comboBox_Size.clear()    
        self.comboBox_Size.addItems(ta)
    def read(self):
        global HShapeSteel
        global AngleSteel
        global ChannelSteel
        global SquarePipe
        global Pipe
        global plt
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label[:11]=='HShapeSteel':
                         HShapeSteel=obj
                         self.comboBox_Shp.setCurrentIndex(0)
                         self.comboBox_Size.setCurrentText(HShapeSteel.size)
                         self.lineEdit_H.setText(HShapeSteel.L)
                     elif obj.Label[:10]=='AngleSteel':
                         AngleSteel=obj  
                         self.comboBox_Shp.setCurrentIndex(1)
                         self.comboBox_Size.setCurrentText(AngleSteel.size)
                         self.lineEdit_H.setText(AngleSteel.L)
                     elif obj.Label[:12]=='ChannelSteel':
                         ChannelSteel=obj  
                         self.comboBox_Shp.setCurrentIndex(2)
                         self.comboBox_Size.setCurrentText(ChannelSteel.size) 
                         self.lineEdit_H.setText(ChannelSteel.L)
                     elif obj.Label[:10]=='SquarePipe':
                         SquarePipe=obj  
                         self.comboBox_Shp.setCurrentIndex(3)
                         self.comboBox_Size.setCurrentText(SquarePipe.size)
                         self.lineEdit_H.setText(SquarePipe.L)
                     elif obj.Label[:4]=='Pipe':
                         Pipe=obj 
                         self.comboBox_Shp.setCurrentIndex(4)  
                         self.comboBox_Size.setCurrentText(Pipe.size)   
                         self.lineEdit_H.setText(Pipe.L)
                     elif obj.Label[:3]=='plt':
                         plt=obj
                   
    def update(self):
        key=self.comboBox_Shp.currentText()
        size=self.comboBox_Size.currentText()
        H=self.lineEdit_H.text()
        t=self.lineEdit_t.text()
        print(t)
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        if key=='Pst_H':
            HShapeSteel.size=size
            HShapeSteel.L=H
            sz='H'+size
        elif key=='Pst_L':
            AngleSteel.size=size
            AngleSteel.L=H 
            sz='L'+size
        elif key=='Pst_C':
            ChannelSteel.size=size
            ChannelSteel.L=H 
            sz='C'+size
        elif key=='Pst_SQ':
            SquarePipe.size=size
            SquarePipe.L=H 
            sz='□'+size
        elif key=='Pst_Pipe':
            Pipe.size=size
            Pipe.L=H 
            sz='Φ'+size
        plt.Length=t
        
        try:
            Standard=sz+' , H='+H
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            obj.Standard=Standard
        except:
            obj.Standard=Standard   
        try:
            g0=obj.g0
            g=obj.Shape.Volume*g0*1000/10**9 
            label='mass[kg]'
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            g0=obj.g0
            g=obj.Shape.Volume*g0*1000/10**9 
            obj.mass=g  
            App.ActiveDocument.recompute()       
        App.ActiveDocument.recompute()       
         
    def create(self): 
         doc = App.ActiveDocument
         fname='03_'+self.comboBox_Shp.currentText()+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'StlStu_data',fname) 
         Gui.ActiveDocument.mergeProject(joined_path)
         
         objs=doc.Objects
         if objs:
             last_obj=objs[-1]   
     
         #last_obj.addProperty("App::PropertyString", "Standard",'Standard')

         Gui.activateWorkbench("DraftWorkbench")
         Gui.Selection.addSelection(last_obj)
         Gui.runCommand('Draft_Move',0) 
        
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)                   
        