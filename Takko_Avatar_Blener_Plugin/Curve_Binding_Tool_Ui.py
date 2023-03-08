import bpy
class Curve_Binding_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "曲线绑定工具"
    bl_idname = "VIEW_3D_PT_CURVE_BINDING_TOOL_UI"    
    bl_category = '獭可工具'   
    bl_order = 3
        
    def draw(self, context):        
        layout = self.layout
        box = layout.box()
        box.prop(context.scene,'curve_binding_tool_armature',text = "骨架物体 ")
        box.prop(context.scene,'curve_binding_tool_bone_layer',text = "骨骼层 ")
        box.prop(context.scene,'curve_binding_tool_bone_count',text = "段数 ")

        box = layout.box()
        box.prop(context.scene,'curve_binding_tool_merge_end',text = "端点合并 ")
        box.prop(context.scene,'curve_binding_tool_bone_name',text = "骨骼名称 ")
        box.prop(context.scene,'curve_binding_tool_direction_suffix',text = "后缀 ")
        box.prop(context.scene,'curve_binding_tool_bind_type',text = "绑定方式 ")
        

        layout.operator("curve_bingding_tool.bind")