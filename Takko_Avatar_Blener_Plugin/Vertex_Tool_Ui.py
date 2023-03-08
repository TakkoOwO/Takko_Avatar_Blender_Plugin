import bpy
def Draw(panel):
    layout = panel.layout
    row = layout.row(align=True)    
    row.operator("vertex_tool.set_weight", text = "1.00").weight = 1
    row.operator("vertex_tool.set_weight", text = "0.00").weight = 0
    
    row = layout.row(align=True)
    row.operator("vertex_tool.set_weight", text = "0.75").weight = 0.75
    row.operator("vertex_tool.set_weight", text = "0.50").weight = 0.5
    row.operator("vertex_tool.set_weight", text = "0.25").weight = 0.25
    
    row = layout.row(align=True)
    row.operator("vertex_tool.set_weight", text = ".875").weight = 0.875
    row.operator("vertex_tool.set_weight", text = ".625").weight = 0.625
    row.operator("vertex_tool.set_weight", text = ".375").weight = 0.375
    row.operator("vertex_tool.set_weight", text = ".125").weight = 0.125

    layout.operator("vertex_tool.average_weight", icon = "FORCE_HARMONIC")
    layout.operator("vertex_tool.fill_weight", icon = "FILTER")
    layout.operator("vertex_tool.mirror_vtgs", icon = "MOD_MIRROR")
    layout.operator("vertex_tool.remove_empty", icon = "REMOVE")

class Vertex_Tool_Ui_Item(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "顶点组工具"
    bl_idname = "VIEW_3D_PT_vertex_tool_ui_item"    
    bl_category = 'Item'    
        
    def draw(self, context):        
        Draw(self)

class Vertex_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "顶点组工具"
    bl_idname = "VIEW_3D_PT_vertex_tool_ui"    
    bl_category = '獭可工具' 
    bl_order = 1   
        
    def draw(self, context):        
        Draw(self)