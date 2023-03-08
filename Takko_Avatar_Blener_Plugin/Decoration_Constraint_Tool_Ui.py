import bpy
class Decoration_Constraint_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "装扮约束工具"
    bl_idname = "VIEW_3D_PT_Decortaion_Constraint_Tool_Ui"    
    bl_category = '獭可工具'    
    bl_order = 6
        
    def draw(self, context):        
        layout = self.layout
        layout.label(text = "未制作完成")
        box = layout.box()
        box.prop(context.scene,'decoration_constraint_tool_main_armature')
        box.prop(context.scene,'decoration_constraint_tool_bone_group_name')
        box.operator("decoration_constraint_tool.seperate")