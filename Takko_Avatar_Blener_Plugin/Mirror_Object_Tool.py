import bpy
from .Core import Obj
from .Core import Log
from .Core import Mode
from .Core import Driver
from .Core import Word
from .Core import Modifier

def Driver_Mirror(operator,scaleReverse):
    #获取全部选中物体
    if (not Mode.Is_Object()):
        Log.ReportError(operator,"请在物体模式下操作")
        return{"CANCELLED"}
    oriObjs = Obj.Selection_All_Get()
    if (oriObjs is None or len(oriObjs) == 0):
        Log.ReportError(operator,"请选中至少一个物体")
        return{"CANCELLED"}
    
    for oriObj in oriObjs:
        #克隆物体(没必要镜像名称，大量重名不好处理)
        newObj = Obj.Clone(oriObj,True)

        #创建变量
        varStruc = Driver.VarStruct() 
        varStruc.name = "var"
        varStruc.obj = oriObj
        varStruc.transform_space = "TRANSFORM_SPACE"

        Driver.New_Driver(newObj, "location", 0, "SCRIPTED") #位置X
        varStruc.transform_type = "LOC_X"
        Driver.Add_Variable(newObj, "location", 0, varStruc)
        Driver.Set_Script(newObj, "location", 0, "var * -1")

        Driver.New_Driver(newObj, "location", 1, "SCRIPTED") #位置Y
        varStruc.transform_type = "LOC_Y"
        Driver.Add_Variable(newObj, "location", 1, varStruc)
        Driver.Set_Script(newObj, "location", 1, "var")

        Driver.New_Driver(newObj, "location", 2, "SCRIPTED") #位置Z
        varStruc.transform_type = "LOC_Z"
        Driver.Add_Variable(newObj, "location", 2, varStruc)
        Driver.Set_Script(newObj, "location", 2, "var")

        Driver.New_Driver(newObj, "rotation_euler", 0, "SCRIPTED") #旋转X
        varStruc.transform_type = "ROT_X"
        Driver.Add_Variable(newObj, "rotation_euler", 0, varStruc)
        Driver.Set_Script(newObj, "rotation_euler", 0, "var")

        Driver.New_Driver(newObj, "rotation_euler", 1, "SCRIPTED") #旋转Y
        varStruc.transform_type = "ROT_Y"
        Driver.Add_Variable(newObj, "rotation_euler", 1, varStruc)
        Driver.Set_Script(newObj, "rotation_euler", 1, "var * -1")

        Driver.New_Driver(newObj, "rotation_euler", 2, "SCRIPTED") #旋转Z
        varStruc.transform_type = "ROT_Z"
        Driver.Add_Variable(newObj, "rotation_euler", 2, varStruc)
        Driver.Set_Script(newObj, "rotation_euler", 2, "var * -1")


        Driver.New_Driver(newObj, "scale", 0, "SCRIPTED") #缩放X
        varStruc.transform_type = "SCALE_X"
        Driver.Add_Variable(newObj, "scale", 0, varStruc)
        #是否反转缩放
        if scaleReverse: Driver.Set_Script(newObj, "scale", 0, "var * -1")      
        else: Driver.Set_Script(newObj, "scale", 0, "var")

        Driver.New_Driver(newObj, "scale", 1, "SCRIPTED") #缩放Y
        varStruc.transform_type = "SCALE_Y"
        Driver.Add_Variable(newObj, "scale", 1, varStruc)
        Driver.Set_Script(newObj, "scale", 1, "var")

        Driver.New_Driver(newObj, "scale", 2, "SCRIPTED") #缩放Z
        varStruc.transform_type = "SCALE_Z"
        Driver.Add_Variable(newObj, "scale", 2, varStruc)
        Driver.Set_Script(newObj, "scale", 2, "var")
        
        #拷贝修改器
        Modifier.Copy_All(newObj,oriObj)

    return {"FINISHED"}



class Mirror_Object_Tool_OT_Mirror(bpy.types.Operator):
    bl_idname = "mirror_object_tool.mirror"
    bl_label = "镜像"
    bl_description = "利用驱动器实现物体镜像，并进行轴对称翻转，适用于绝大多数情况"
    def execute(self,context): 
        return Driver_Mirror(self,True)

class Mirror_Object_Tool_OT_Mirror_Only_Position(bpy.types.Operator):
    bl_idname = "mirror_object_tool.mirror_only_position"
    bl_label = "镜像(仅位置)"
    bl_description = "利用驱动器实现物体镜像，仅对称位置，不镜像翻转，通常运用于眼球"
    def execute(self,context): 
        return Driver_Mirror(self,False)