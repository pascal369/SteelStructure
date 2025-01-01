import FreeCADGui as Gui
import FreeCAD as App
class massCulc:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)    
    def execute(self,obj):
        #label=obj.Name
        #g0=App.ActiveDocument.getObject(label).g0
        

        #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        
        # オブジェクトを選択
        obj = Gui.Selection.getSelection()[0]
        g = obj.Shape.Volume * 7.85*1000/10**9
        # オブジェクトの質量を計算
        #c00=obj.Shape
        #g = c00.Volume * g0/10**9
        #print(g)
        #print(obj.Shape.Volume)
        # プロパティに質量を追加
        label='mass[kg]'
        try:
            
            #obj.addProperty("App::PropertyFloat", "mass",label)
            #obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyFloat", "g",label).g=g
            
        except:
            #obj = Gui.Selection.getSelection()[0]
            #obj.addProperty("App::PropertyFloat", "g0",'Specific gravity').g0=g0
            obj.addProperty("App::PropertyFloat", "g",label).g=g
            
            pass    