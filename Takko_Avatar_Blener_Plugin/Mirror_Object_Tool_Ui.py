import bpy
class Mirror_Object_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "物体镜像工具"
    bl_idname = "VIEW_3D_PT_Mirror_Object_Tool_Ui"    
    bl_category = '獭可工具'    
    bl_order = 2
        
    def draw(self, context):        
        layout = self.layout
        column = layout.column()
        column.operator("mirror_object_tool.mirror",icon = "MOD_MIRROR")
        column.operator("mirror_object_tool.mirror_only_position",icon = "MOD_MIRROR")
        
       