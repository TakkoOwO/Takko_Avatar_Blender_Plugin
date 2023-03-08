import bpy
from .Core import Mesh
from .Core import Word
from .Core import Mode
from .Core import Log

from .Core import Obj
class Debugger_OT_Test(bpy.types.Operator):
    bl_idname = "debugger.test"
    bl_label = "测试"
    
    def execute(self,context): 
        for i in range(5,-1,-1):
            print(i)
        return{"FINISHED"}