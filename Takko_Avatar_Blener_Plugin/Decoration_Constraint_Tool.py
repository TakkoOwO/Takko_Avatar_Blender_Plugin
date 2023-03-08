import bpy
from .Core import Poll
from .Core import Log
from .Core import Armature
from .Core import Obj
from .Core import VertexGroup

def Get_Bone_Grp_Items(self, context):
    arm = context.scene.decoration_constraint_tool_main_armature
    if arm is None:return None
    bone_grps = Armature.Bone_Group_All_Get(arm)
    enum_list = []
    for grp in bone_grps:
        enum_list.append((grp,grp,""))
    return enum_list

#骨架物体
bpy.types.Scene.decoration_constraint_tool_main_armature = bpy.props.PointerProperty(
        name ="主骨架",
        type= bpy.types.Object,
        poll= Poll.ArmatureObj )
# bpy.types.Scene.decoration_constraint_tool_bone_group_name = bpy.props.StringProperty(
#     name ="身体骨骼组",default = "body")

bpy.types.Scene.decoration_constraint_tool_bone_group_name =  bpy.props.EnumProperty(
        name='身体骨骼组',
        items=Get_Bone_Grp_Items,
    )



class Decoration_Constraint_Tool_OT_Seperate(bpy.types.Operator):
    bl_idname = "decoration_constraint_tool.seperate"
    bl_label = "从主骨架中分离"
    bl_description = "从主骨架中分离出一个服装的骨架，并设置约束"
        
    def execute(self,context): 

        #获取选中的装饰物体
        decoration_objs = []     
        for obj in Obj.Selection_All_Get():
            if Obj.Type_Get(obj) == "MESH":
                decoration_objs.append(obj)
        if len(decoration_objs) == 0: return Log.Error_Cancelled(self,"未选中任何网格物体")

        #获取主骨架，以及全部的骨骼
        main_armaObj = context.scene.decoration_constraint_tool_main_armature
        if main_armaObj is None: return Log.Error_Cancelled(self,"未指定主骨架")
        all_bones = Armature.Bone_Names_All_Get(main_armaObj)

        #通过骨骼组获取身体骨骼
        group_name = context.scene.decoration_constraint_tool_bone_group_name
        if group_name == "": return Log.Error_Cancelled(self,"请指定身体骨骼所在骨骼组的名称")
        if not Armature.Bone_Group_Exist(main_armaObj,group_name): return Log.Error_Cancelled(self,"主骨架中并不包含 {} 这个骨骼组".format(group_name))
        body_bones = Armature.Bones_From_Group(main_armaObj,group_name)
        if(len(body_bones) == 0): return Log.Error_Cancelled(self,"骨骼组中没有指定骨骼")

        #通过装饰网格体获取全部的非空顶点组
        decoration_vtgs = set()
        for obj in decoration_objs:
            nonEmpty_grps = VertexGroup.Non_Empty_Group_All_Get(obj)
            #取并集
            decoration_vtgs = decoration_vtgs | set(nonEmpty_grps)
        
        #服装权重骨(跟服装权重有关的骨骼)
        decoration_weight_bones = decoration_vtgs & set(all_bones)

        #仅属服装骨（服装权重骨中只属于服装的）
        decoration_only_bones = (set(all_bones) - set(body_bones)) & decoration_weight_bones
        
        #额外服装骨（服装骨的子级和父级，不包括身体骨）
        decoration_extra_bone = set()
        
        #身体服装骨（同时属于身体和服装的骨骼，包括有权重的，以及父级）
        decoration_body_bone = set()

        def Get_All_Child(armatureObj,bone):
            #获取该骨骼的全部子骨骼
            children = Armature.Bone_Children_Get(armatureObj,bone)
            if children is not None:
                #遍历子骨骼
                for child_bone in children:
                    #如果子骨骼已经在 服装骨，就跳过
                    if(child_bone in decoration_only_bones): continue
                    #加入 额外服装骨，并继续遍历其子级
                    decoration_extra_bone.add(child_bone)
                    Get_All_Child(armatureObj,child_bone)
        
        def Get_All_Parent(armatureObj,bone):
            #获取骨骼的父级
            parent_bone = Armature.Bone_Parent_Get(armatureObj,bone)
            #如果父级不是空并且不在服装骨中
            if parent_bone is not None and parent_bone not in decoration_only_bones:
                #如果父级是身体骨
                if parent_bone in body_bones:
                    #加入 身体服装骨
                    decoration_body_bone.add(parent_bone)
                else:
                    #加入额外服装骨，继续遍历其父级
                    decoration_extra_bone.add(parent_bone)
                    Get_All_Parent(armatureObj,parent_bone)

        #获取 额外服装骨 和 身体服装骨
        for bone in decoration_only_bones:
            Get_All_Child(main_armaObj,bone)
        for bone in decoration_weight_bones:
            Get_All_Parent(main_armaObj,bone)
        
        #输出一下
        decoration_bone_count = len(decoration_only_bones | decoration_extra_bone | decoration_body_bone)
        print("服装骨 {0} 个，额外服装骨 {1} 个，身体服装骨 {2} 个，一共 {3} 个".format(
            len(decoration_only_bones),len(decoration_extra_bone),len(decoration_body_bone),decoration_bone_count
        ))

        #获取这些骨骼的关系


        #拷贝一个新的骨架并赋值，注意是拷贝

        



        return {"FINISHED"} 