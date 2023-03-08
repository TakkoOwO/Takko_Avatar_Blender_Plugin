import bpy
class Debbuger_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Debug"
    bl_idname = "VIEW_3D_PT_Debbuger_UI"    
    bl_category = '獭可工具'   
    bl_order = 0
        
    def draw(self, context):        
        layout = self.layout
        layout.operator("debugger.test", text = "测试")