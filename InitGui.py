#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class SteelStructureShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "SteelStructureworkbench.svg"),
          'MenuText': "SteelStructure",
          'ToolTip': "Show/Hide SteelStructure"}

    def IsActive(self):
        import SteelStructure
        SteelStructure
        return True

    def Activated(self):
        try:
          import SteelStructure
          SteelStructure.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import SteelStructure
        return not FreeCAD.ActiveDocument is None

class SteelStructureWorkbench(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "SteelStructureworkbench.svg")
        self.__class__.MenuText = "SteelStructure"
        self.__class__.ToolTip = "SteelStructure by Pascal"

    def Initialize(self):
        self.commandList = ["SteelStructure_Show"]
        self.appendToolbar("&SteelStructure", self.commandList)
        self.appendMenu("&SteelStructure", self.commandList)

    def Activated(self):
        import SteelStructure
        SteelStructure
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
    
FreeCADGui.addWorkbench(SteelStructureWorkbench())
FreeCADGui.addCommand("SteelStructure_Show", SteelStructureShowCommand())    
