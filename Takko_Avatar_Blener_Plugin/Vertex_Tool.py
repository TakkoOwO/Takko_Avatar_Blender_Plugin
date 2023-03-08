import bpy
from .Core import Mode
from .Core import Mesh
from .Core import Log
from .Core import Obj
from .Core import VertexGroup
from .Core import Display
from .Core import Word

#设置顶点权重
class Vertex_Tool_OT_Set_Weight(bpy.types.Operator):
    bl_idname = "vertex_tool.set_weight"
    bl_label = "设置顶点权重"

    weight : bpy.props.FloatProperty(default=0)

    def execute(self, context):        
        #获取激活物体
        if not Mode.IsMode("EDIT_MESH"):
            Log.ReportError(self,"请在编辑网格模式中执行此操作")
            return {"CANCELLED"}
        obj = Obj.Acive_Get()
        Mode.Switch_Object()

        #获取激活顶点组
        vtg_active = VertexGroup.Active_Index_Get(obj)
        if vtg_active == -1:
            Log.ReportError(self,"操作对象没有顶点组")
            Mode.Switch_Edit()
            return {"CANCELLED"}

        #获取选中的顶点
        vers_selected = Mesh.Points_Select_Get(obj)
        if len(vers_selected) == 0:
            Log.ReportError(self,"没有选中任何顶点")
            Mode.Switch_Edit()
            return {"CANCELLED"}

        if (self.weight != 0):
            VertexGroup.Weight_Set(obj,vtg_active,vers_selected,self.weight)                       
        else:
            VertexGroup.Weight_Clear(obj,vtg_active,vers_selected) 

        Mode.Switch_Edit()

        Display.Vertex_Weight_Display_Set(True)
            
        return {"FINISHED"}

class Vertex_Tool_OT_Average_Weight(bpy.types.Operator):
    bl_idname = "vertex_tool.average_weight"
    bl_label = "平均顶点权重"
    bl_description = "将选中的顶点的权重进行平均，通常用于对毛发、飘带等柱状物体的自动权重进行修复"

    def execute(self, context):        
        #获取激活物体
        if not Mode.IsMode("EDIT_MESH"):
            Log.ReportError(self,"请在编辑网格模式中执行此操作")
            return {"CANCELLED"}
        meshObj = Obj.Acive_Get()  
        Mode.Switch_Object()
        #获取选中的顶点
        vers_selected = Mesh.Points_Select_Get(meshObj)
        if len(vers_selected) == 0:
            Log.ReportError(self,"没有选中任何顶点")
            Mode.Switch_Edit()
            return {"CANCELLED"}

        #遍历顶点组，设置权重
        VertexGroup.Average_Weight(meshObj,vers_selected)
        Mode.Switch_Edit()
        return {"FINISHED"}


class Vertex_Tool_OT_Fill_Weight(bpy.types.Operator):
    bl_idname = "vertex_tool.fill_weight"
    bl_label = "填充权重"
    bl_description = "遍历全部顶点组，判断选中顶点的剩余权重，全部填充在活动顶点组中"
    def execute(self, context):        
        #获取激活物体
        if not Mode.IsMode("EDIT_MESH"):
            Log.ReportError(self,"请在编辑网格模式中执行此操作")
            return {"CANCELLED"}
        meshObj = Obj.Acive_Get()
        
        Mode.Switch_Object()

        #获取激活顶点组
        vtg_active = VertexGroup.Active_Index_Get(meshObj)
        if vtg_active == -1:
            Log.ReportError(self,"操作对象没有顶点组")
            Mode.Switch_Edit()
            return {"CANCELLED"}

        #获取选中的顶点
        vers_selected = Mesh.Points_Select_Get(meshObj)
        if len(vers_selected) == 0:
            Log.ReportError(self,"没有选中任何顶点")
            Mode.Switch_Edit()
            return {"CANCELLED"}
        
        #将选中顶点的权重清空
        VertexGroup.Weight_Clear(meshObj,vtg_active,vers_selected)
        
        #初始化记录顶点权重的字典
        dic_weight = {}
        for ver in vers_selected:
            dic_weight[ver] = 0

        #遍历顶点组，计算选中点的全部权重
        for i in range(VertexGroup.Count_Get(meshObj)):
            for ver in vers_selected:
                dic_weight[ver] += VertexGroup.Weight_Get(meshObj,i,ver)
        
        #设置权重
        for ver in vers_selected:
            weight_rest = 1 - dic_weight[ver]
            if weight_rest <= 0: continue
            VertexGroup.Weight_Set(meshObj,vtg_active,ver,weight_rest)
        
        Mode.Switch_Edit()
        return {"FINISHED"}

class Vertex_Tool_OT_Mirror_Vtgs(bpy.types.Operator):
    bl_idname = "vertex_tool.mirror_vtgs"
    bl_label = "创建镜像顶点组"

    def execute(self, context): 
        meshObj = Obj.Acive_Get()
        if meshObj is None or Obj.Type_Get(meshObj) != "MESH":
            return Log.Error_Cancelled(self,"激活物体为空或不是网格体") 
        names = VertexGroup.Names_Get_All(meshObj)
        newNames = []
        for name in names:
            newName = Word.Get_Name_Mirror(name)
            if newName is not None:
                if newName not in names:
                    newNames.append(newName)
        for newName in newNames:
            VertexGroup.Create(meshObj,newName)
        Log.ReportInfo(self,"为网格体 {} 创建了 {} 个镜像的形态键".format(meshObj.name,len(newNames)))
        return {"FINISHED"}

class Vertex_Tool_OT_Remove_Empty(bpy.types.Operator):
    bl_idname = "vertex_tool.remove_empty"
    bl_label = "移除空顶点组"

    def execute(self, context): 

        meshObj = Obj.Acive_Get()
        if meshObj is None or Obj.Type_Get(meshObj) != "MESH":
            return Log.Error_Cancelled(self,"激活物体为空或不是网格体") 
        
        count = empty_grps = VertexGroup.Empty_Group_All_Remove(meshObj)

        Log.ReportInfo(self,"从活动物体中清除了{}个空顶点组".format(count))
        return {"FINISHED"}