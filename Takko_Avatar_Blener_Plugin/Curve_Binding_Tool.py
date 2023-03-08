from pickle import OBJ
import bpy
from .Core import Obj
from .Core import Mode 
from .Core import Log
from .Core import Curve
from .Core import Constraint
from .Core import Armature
from .Core import Word
from .Core import Mesh
from .Core import VertexGroup
from .Core import Modifier

#骨架物体
def ArmatureObj(self,object): return object.type == 'ARMATURE'
bpy.types.Scene.curve_binding_tool_armature = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll= ArmatureObj )

#骨骼层级
bpy.types.Scene.curve_binding_tool_bone_layer = bpy.props.IntProperty(
    default = 0, min = 0, max= 31)

#段数
bpy.types.Scene.curve_binding_tool_bone_count = bpy.props.IntProperty(
    default = 4, min = 2, max= 32)

#绑定方式
bpy.types.Scene.curve_binding_tool_bind_type = bpy.props.EnumProperty(
    name="绑定方式:",
    items=[ ('active', "活动", "以活动曲线为准绑定骨骼"),
            ('center', "中心", "以各个曲线中心绑定骨骼")],
    description = "绑定时创建骨骼的方式")

#骨骼名称
bpy.types.Scene.curve_binding_tool_bone_name = bpy.props.StringProperty(
    name ="骨骼名称",default = "fur")

#方向后缀
bpy.types.Scene.curve_binding_tool_direction_suffix = bpy.props.EnumProperty(
    name="骨骼方向后缀:",
    items=[ ("empty","无后缀","没有后缀"),
            ('left', ".L", "后缀添加.L"),
            ('right', ".R", "后缀添加.R")],
    description = "为生成的骨骼添加方向后缀，方便镜像操作")

#是否封口
bpy.types.Scene.curve_binding_tool_merge_end = bpy.props.BoolProperty(
    description  = "是否要合并两端的顶点",default = True)

class Curve_Binding_Tool_OT_Bind(bpy.types.Operator):
    bl_idname = "curve_bingding_tool.bind"
    bl_label = "绑定"
    
    def execute(self,context): 
        #获取全部选中的曲线物体
        if(not Mode.Is_Object()):
            return Log.Error_Cancelled(self,"操作需要在物体模式下进行")
        curve_objs = Obj.Selection_All_Get()
        if len(curve_objs) == 0:
            return Log.Error_Cancelled(self,"没有选中任何物体")
        for obj in curve_objs:
            if Obj.Type_Get(obj) != "CURVE":
                return Log.Error_Cancelled(self,"选中物体必须全部是曲线")
        curve_active = Obj.Acive_Get()

        arm_obj = context.scene.curve_binding_tool_armature
        if arm_obj is None: return Log.Error_Cancelled(self,"未设置目标骨架")

        sp_name = context.scene.curve_binding_tool_bone_name
        if sp_name == "": return Log.Error_Cancelled(self,"未设置动骨名称")

        layer = context.scene.curve_binding_tool_bone_layer
        merge_end = context.scene.curve_binding_tool_merge_end

        #记录UV信息
        uvs = []
        for curve_obj in curve_objs:
            uv = Curve.Get_UV(curve_obj)
            print(uv)
            if uv[1] == 0: return Log.Error_Cancelled(self,"绑定曲线需要有倒角厚度")
            uvs.append(uv)

        #创建空物体,添加跟随路径约束
        empty_obj = Obj.Create_Empty()
        follow_Path = Constraint.FOLLOW_PATH.Add(empty_obj)
        Constraint.FOLLOW_PATH.Use_Fixed_Location_Set(empty_obj,follow_Path,True)

        #根据骨骼段数，计算曲线等分点位置
        def __Calculate_Bone_Points(curverObj,boneCount):
            #设置空物体的跟随路径目标为某根曲线
            Constraint.FOLLOW_PATH.Target_Set(empty_obj,follow_Path,curverObj)
            #计算几个顶点的位置系数
            points = [0]
            v = 1.0 / boneCount
            for i in range(boneCount - 1):
                points.append((i + 1) / boneCount )
            points.append(1)
            #根据系数修改约束的值，获取此时空物体的位置
            for i in range(len(points)):
                Constraint.FOLLOW_PATH.Offset_Factor_Set(empty_obj,follow_Path,points[i])
                Obj.Update()
                points[i] = Obj.Position_World_Get(empty_obj)
            return points
        
        #根据绑定方式的不同，计算骨骼位置
        bone_count = context.scene.curve_binding_tool_bone_count
        positions = None
        if(context.scene.curve_binding_tool_bind_type == 'active' or len(curve_objs) == 0):
            positions = __Calculate_Bone_Points(curve_active,bone_count)
        else:
            positions = __Calculate_Bone_Points(curve_objs[0],bone_count)
            for i in range(1, len(curve_objs)):
                single_positons = __Calculate_Bone_Points(curve_objs[i],bone_count)
                for a in range(bone_count + 1):
                    positions[a][0] += single_positons[a][0]
                    positions[a][1] += single_positons[a][1]
                    positions[a][2] += single_positons[a][2]
            for a in range(bone_count + 1):
                    positions[a][0] = positions[a][0] / len(curve_objs)
                    positions[a][1] = positions[a][1] / len(curve_objs)
                    positions[a][2] = positions[a][2] / len(curve_objs)

        #删除空物体
        Obj.Delete(empty_obj)

        #确定骨骼的命名 sp_hair_001_01.L
        sp_prefix = "sp"
        sp_index = 0
        sp_direction = -1
        if context.scene.curve_binding_tool_direction_suffix == "left": sp_direction = 0
        elif context.scene.curve_binding_tool_direction_suffix == "right": sp_direction = 1
        #遍历原有骨骼确定序号
        names = Armature.Bone_Names_All_Get(arm_obj)
        for name in names:
            result = Word.Spring_Bone_Name_Check(name)
            if result is not None:
                if result[0] == sp_name:
                    #如果已有骨骼里存在同名但没有序号的的骨骼，给它改成001
                    if result[1] == 0: 
                        newName = Word.Spring_Bone_Name_Build(result[0],1,result[2],result[3])
                        Armature.Bone_Name_Change(arm_obj,name,newName)
                        if sp_index == 0: sp_index = 2
                    #根据同名骨骼序号推延新建骨骼的序号
                    elif result[1] >= sp_index: sp_index += 1

        #根据位置创建临时骨架和骨骼
        temp_arm_Obj = Armature.Create_Empty_Armature()
        Obj.Acive_Set(temp_arm_Obj)
        Mode.Switch_Edit()
        name_parent = None
        for i in range(len(positions) - 1):
            sp_joint_index = i + 1
            name_bone = Word.Spring_Bone_Name_Build(sp_name,sp_index,sp_joint_index,sp_direction,sp_prefix)
            #设置骨骼
            edit_bone = Armature.Create_Edit_Bone(temp_arm_Obj,name_bone)         
            #设置骨骼的Transform
            Armature.Edit_Bone_Transform_Set(
                temp_arm_Obj,edit_bone,
                positions[i],positions[i+1],0)    
            #设置父级
            if name_parent is not None:
                Armature.Edit_Bone_Parent_Set(temp_arm_Obj,name_bone,name_parent)
            #设置层级
            Armature.Edit_Bone_Layers_Set(temp_arm_Obj,name_bone,layer)
            name_parent = name_bone
        Mode.Switch_Object()

        #转化成网格体
        Obj.Selection_Clear()
        for curve_obj in curve_objs:
            Obj.Select_Set(curve_obj,True)
        Obj.Acive_Set(curve_objs[0])      
        Obj.Convert_Selection_To_Mesh()

        #合并端点
        if merge_end :
            for i in range(len(curve_objs)):
                Obj.Acive_Set(curve_objs[i])
                u,v = uvs[i][0],uvs[i][1]
                index = []
                for a in range((u-1) * v,u * v):index.append(a)  
                Mesh.Points_Select_Set(curve_objs[i],index)
                Mode.Switch_Edit()
                Mesh.Merge_Selected_Points_Center()
                Mode.Switch_Object()
                index.clear()
                for a in range(0, v):index.append(a)  
                Mesh.Points_Select_Set(curve_objs[i],index)
                Mode.Switch_Edit()
                Mesh.Merge_Selected_Points_Center()
                Mode.Switch_Object()

        #绑定物体
        Obj.Acive_Set(temp_arm_Obj)
        Armature.Binding_With_Auto_Weight()

        #平滑权重
        for i in range(len(curve_objs)):
            curve_obj = curve_objs[i]
            start = 0
            end = uvs[i][0]
            if merge_end: start,end = start + 1, end - 1
            v = uvs[i][1]
            for u in range(start,end):
                points = []
                if (merge_end): 
                    for i in range((u-1) * v + 1 , u * v + 1): points.append(i)
                else: 
                    for i in range(u * v , (u+1) * v): points.append(i)
                
                VertexGroup.Average_Weight(curve_obj,points)

        #清空绑定
        for curve_obj in curve_objs:
            Modifier.Clear(curve_obj)
            Obj.Parent_Set(curve_obj,None)
        
        #合并骨架
        Obj.Selection_Clear
        Obj.Select_Set(arm_obj,True)
        Obj.Acive_Set(arm_obj)
        Armature.Join()

        #再绑定
        for curve_obj in curve_objs:
            Obj.Select_Set(curve_obj,True)
        Armature.Binding_Default()
        return{"FINISHED"}