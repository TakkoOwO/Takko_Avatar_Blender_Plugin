import bpy
class Decimate_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "精简工具"
    bl_idname = "VIEW_3D_PT_DECIMATE_TOOL_UI"    
    bl_category = '獭可工具'   
    bl_order = 7
        
    def draw(self, context):        
        layout = self.layout
        layout.operator("decimate_tool.un_subdevide")
        layout.operator("decimate_tool.to_subdevide")