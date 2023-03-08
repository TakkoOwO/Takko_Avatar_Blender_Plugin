import bpy
class Modifier_Apply_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "应用修改器工具"
    bl_idname = "VIEW_3D_PT_MODIFIER_Apply_TOOL_UI"    
    bl_category = '獭可工具'   
    bl_order = 5
        
    def draw(self, context):        
        layout = self.layout
        layout.label(text = "作者: przemir")
        layout.operator("modifier_apply_tool.apply",icon = "MODIFIER_DATA")
        
        

      