import bpy
class Shape_Key_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "形态键工具"
    bl_idname = "VIEW_3D_PT_Shape_Key_Tool_UI"    
    bl_category = '獭可工具'    
    bl_order = 4
        
    def draw(self, context):        
        layout = self.layout
        column = layout.column()
        column.operator("shape_key_tool.select_move_points",text = "查看位移点", icon = "VERTEXSEL")
        column.operator("shape_key_tool.reset_select_points", text = "复原选中点", icon = "DECORATE_OVERRIDE")
        column.operator("shape_key_tool.reset_select_points_from_all",text = "复原选中点(全部)", icon = "DECORATE_OVERRIDE")
        column.operator("shape_key_tool.mirror", text = "镜像形态键", icon = "MOD_MIRROR")
        column.operator("shape_key_tool.reset_zero", text = "全部值归零", icon = "ALIGN_LEFT")
         
        box = column.box()
        box.prop(context.scene,'shape_key_tool_shape_key_name',text = "名称 ")
        row = box.row()
        row.operator("shape_key_tool.mix", text = "到末尾", icon = "ADD").toActive = False
        row.operator("shape_key_tool.mix", text = "到活动", icon = "ADD").toActive = True
        
       