from PySide import QtCore, QtGui
import FreeCADGui as Gui
import os
#import SteelStructure

class SteelStructure (Gui.Workbench):
    MenuText = "SteelStructure"
    ToolTip = "SteelStructure"
    #Icon = 'SteelStructure.svg'
    def Initialize(self):
        #import Handrails, Ladder,Pln_shape,Shaped_steel,SplStairCase,SplStairCaseNoProp,SteelStair2,SteelStairs,SteelStructure
        #self.list = ["SteelStructure"] 
        import SteelStructure
        self.list = ["SteelStructure"] 
        self.appendToolbar("SteelStructure", self.list) 
        # マクロのパスを指定します
        macro_path = "SteelStructure"
        print(macro_path)
        # ワークベンチを取得します
        workbench_name = "SteelStructure"
        workbench = Gui.getWorkbench(workbench_name)

        # マクロを関連付けます
        workbench.appendMenu("SteelStructure", [
            {"text": "SteelStructure", "tip": "SteelStructure", "": "", "command": 'importMacro("{0}")'.format(macro_path)}
        ])

        # GUIを再構築します
        Gui.updateGui()

    def Activated(self):
        import SteelStructure
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("SteelStructure", self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(SteelStructure())
