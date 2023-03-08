import math
from msilib.schema import Error
from multiprocessing.sharedctypes import Value
from operator import mod
import bpy
from .Core import Mode
from .Core import Obj
from .Core import Mesh
from .Core import ShapeKey
from .Core import Log
from .Core import Word

#选中位置点
class Shape_Key_Tool_OT_Select_Move_Points(bpy.types.Operator):
    bl_idname = "shape_key_tool.select_move_points"
    bl_label = "选中位移点"
    bl_description = "选中活动形态键中发生了位移的顶点"
        
    def execute(self,context): 
        if not Mode.IsMode("EDIT_MESH"): 
            Log.ReportWarning(self,"需要在编辑网格模式下操作") 
            return{"CANCELLED"}  

        meshObj = Obj.Acive_Get()

        if ShapeKey.Count_Get(meshObj) == 0:
            Log.ReportWarning(self,"没有形态键") 
            return{"CANCELLED"}  

        Mode.Switch_Object()

        oriPositions = Mesh.Points_Position_Local_All_Get(meshObj)
        activeIndex = ShapeKey.Active_Index_Get(meshObj)
        keyPositions = ShapeKey.Position_Get(meshObj,activeIndex)
        movePointIndexs = []
        for i in range(len(oriPositions)):
            if(not math.isclose(oriPositions[i][0],keyPositions[i][0], abs_tol= 1e-6)
            or not math.isclose(oriPositions[i][1],keyPositions[i][1], abs_tol= 1e-6)
            or not math.isclose(oriPositions[i][2],keyPositions[i][2], abs_tol= 1e-6)):
                movePointIndexs.append(i)
        
        Mesh.Points_Select_Set(meshObj,movePointIndexs)
        Log.ReportInfo(self,"共有{}个位移点".format(len(movePointIndexs)))

        Mode.Switch_Edit()

        return {"FINISHED"} 

#将选中顶点位置还原
def Reset_Select_Points_In_shapeKey(operator,blAll):
    #确认_Edit模式
    if not Mode.IsMode("EDIT_MESH"): 
        Log.ReportWarning(operator,"需要在编辑网格模式下操作") 
        return{"CANCELLED"}        
    #在物体模式下操作
    Mode.Switch_Object()     
    #获取选中的顶点
    meshObj = Obj.Acive_Get()
    selectedVers = Mesh.Points_Select_Get(meshObj)
    #确认_形态键数量
    count = ShapeKey.Count_Get(meshObj)
    activeIndex = ShapeKey.Active_Index_Get(meshObj)
    if count == 0:
        Log.ReportWarning(operator,"没有形态键") 
        return{"CANCELLED"}     
    #获取原顶点位置
    oriPositions = Mesh.Points_Position_Local_All_Get(meshObj)
    
    #将某个序号的形态键中选中点位置复原
    def __ResetPoints(shapeKeyIndex):
        keyPositions = ShapeKey.Position_Get(meshObj,shapeKeyIndex)
        #更新选中顶点的位置到原位置
        for ver in selectedVers:
            keyPositions[ver] = oriPositions[ver]
        #根据选中顶点的序号，更新形态键顶点的位置
        ShapeKey.Position_Set(meshObj,shapeKeyIndex,keyPositions)
    
    #根据是否还原全部形态键进行还原操作
    if(blAll):
        for i in range(count):__ResetPoints(i)
        Log.ReportInfo(operator,"已将选中点在全部形态键中还原")
    else:
        __ResetPoints(activeIndex)  
        Log.ReportInfo(operator,"已将选中点在活动形态键中还原")
    #回到编辑模式
    Mode.Switch_Edit()
    return {"FINISHED"} 

#将选中顶点位置还原_活动
class Shape_Key_Tool_OT_Reset_Select_Points(bpy.types.Operator):
    bl_idname = "shape_key_tool.reset_select_points"
    bl_label = "点复原(活动)"
    bl_description = "将选中的顶点在活动形态键中复原位置"
        
    def execute(self,context): 
        return Reset_Select_Points_In_shapeKey(self,False)

#将选中顶点位置还原_全部
class Shape_Key_Tool_OT_Reset_Select_Points_From_All(bpy.types.Operator):
    bl_idname = "shape_key_tool.reset_select_points_from_all"
    bl_label = "点复原(全部)"
    bl_description = "将选择的顶点从全部的形态键中复原位置"
    
    #确定框
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self) 

    def execute(self,context): 
        return Reset_Select_Points_In_shapeKey(self,True)

#生成镜像形态键
class Shape_Key_Tool_OT_Mirror(bpy.types.Operator):
    bl_idname = "shape_key_tool.mirror"
    bl_label = "生成镜像形态键"
    bl_description = "为活动形态键生成一个镜像的形态键"
        
    def execute(self,context): 
        #确认_活动物体是网格、有形态键
        meshObj = Obj.Acive_Get()
        if Obj.Type_Get(meshObj) != "MESH":
            Log.ReportError(self,"活动物体不是网格体") 
            return{"CANCELLED"} 

        #形态键数量
        count = ShapeKey.Count_Get(meshObj)
        if count < 2:
            Log.ReportError(self,"形态键需要大于等于2个") 
            return{"CANCELLED"} 
        
        #形态键序号
        oriIndex = ShapeKey.Active_Index_Get(meshObj)
        if oriIndex == 0:
            Log.ReportError(self,"目标形态键是基型") 
            return{"CANCELLED"} 
        
        #记录模式
        blEdit = Mode.Is_Edit()

        #切到物体模式
        Mode.Switch_Object()

        #记录原来的Mute情况，并Mute掉全部的
        oriMutes = []
        for i in range(count):
            oriMutes.append(ShapeKey.Get_Mute(meshObj,i))
            ShapeKey.Set_Mute(meshObj,i,True)
        
        #活动形态键激活并value设置为1
        oriValue = ShapeKey.Get_Value(meshObj,oriIndex)
        ShapeKey.Set_Value(meshObj,oriIndex,1)
        ShapeKey.Set_Mute(meshObj,oriIndex,False)
        
        #生成形态键
        ShapeKey.Generate_Mixed()
        #镜像
        ShapeKey.Active_Index_Set(meshObj,count)
        ShapeKey.Mirror_Active()
        
        #复原Mute和Value
        for i in range(count):
            ShapeKey.Set_Mute(meshObj,i,oriMutes[i])
        ShapeKey.Set_Value(meshObj,oriIndex,oriValue)
        count += 1
        
        #新形态键名称
        oriName = ShapeKey.Name_Get(meshObj,oriIndex)
        newName = Word.Get_Name_Mirror(oriName)

        #若存在同名形态键，删除
        if(newName != oriName):
            tar = ShapeKey.Get_Index_By_Name(meshObj,newName)
            if tar != -1:
                ShapeKey.Active_Index_Set(meshObj,tar)
                ShapeKey.Delete_Active()
                count -= 1
                if tar < oriIndex: oriIndex -= 1
        
        #应用名称
        ShapeKey.Name_Set(meshObj,count -1,newName)
        
        #活动形态键设为新的
        ShapeKey.Active_Index_Set(meshObj,count - 1)
        #移动到正确位置
        offset = (count - oriIndex - 2) * -1
        if Word.Get_Name_Direction(newName) == 0: offset -= 1
        ShapeKey.Move_Active(meshObj,offset)

        #回到原模式
        if blEdit: Mode.Switch_Edit()
  
        return {"FINISHED"} 

class Shape_Key_Tool_OT_Reset_Zero(bpy.types.Operator):
    bl_idname = "shape_key_tool.reset_zero"
    bl_label = "全部值归零"
    bl_description = "将形态键数值归零"

    def execute(self,context): 
        #确认_活动物体是网格、有形态键
        meshObj = Obj.Acive_Get()
        if Obj.Type_Get(meshObj) != "MESH": return Log.Error_Cancelled(self,"活动物体不是网格体") 

        #确认有形态键
        count = ShapeKey.Count_Get(meshObj)
        if count == 0: return Log.Error_Cancelled(self,"网格体无形态键") 
        
        #记录模式
        blEdit = Mode.Is_Edit()

        Mode.Switch_Object()

        ShapeKey.Reset_All_Value(meshObj)

        #回到原模式
        if blEdit: Mode.Switch_Edit()


        return {"FINISHED"} 

bpy.types.Scene.shape_key_tool_shape_key_name = bpy.props.StringProperty(
    name ="形态键名称",default = "")
    
class Shape_Key_Tool_OT_Mix(bpy.types.Operator):
    bl_idname = "shape_key_tool.mix"
    bl_label = "混合形态键"
    bl_description = "将形态键混合并生成"

    toActive : bpy.props.BoolProperty(default=False)

    def execute(self,context): 
        #获取名称
        shapeKeyName = context.scene.shape_key_tool
        if (shapeKeyName == ""): return Log.Error_Cancelled(self,"未附形态键名称")
        
        #确认_活动物体是网格、有形态键
        meshObj = Obj.Acive_Get()
        if Obj.Type_Get(meshObj) != "MESH": return Log.Error_Cancelled(self,"活动物体不是网格体") 

        #确认有形态键
        count = ShapeKey.Count_Get(meshObj)
        if count == 0: return Log.Error_Cancelled(self,"网格体无形态键") 
        
        #活动形态键序号
        activeIndex = ShapeKey.Active_Index_Get(meshObj)
        
        #记录模式
        blEdit = Mode.Is_Edit()

        Mode.Switch_Object()

        #清空名称
        context.scene.shape_key_tool = ""
        
        #生成形态键
        ShapeKey.Generate_Mixed()

        #归零数值
        ShapeKey.Reset_All_Value(meshObj)

        #设置名称
        ShapeKey.Name_Set(meshObj,count,shapeKeyName)

        #移动到活动形态键位置下
        if (self.toActive):
            ShapeKey.Move_Active(meshObj,(count-activeIndex-1) * -1)

        #回到原模式
        if blEdit: Mode.Switch_Edit()

        return {"FINISHED"} 
