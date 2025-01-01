# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import FreeCAD as App
import FreeCADGui as Gui
#from PySide import QtGui
#from PySide import QtUiTools
#from PySide import QtCore
#from prt_data.CSnap_data import paramCSnap

class Ui_Dialog(object):
  
    def setupUi(self, Dialog):
        global fname
        global joined_path
        fname='GussetPlate.FCStd'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'pln_data',fname) 
        try:
            Gui.ActiveDocument.mergeProject(joined_path)
        except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

        

