import bpy
from . import Obj

#  ["DATA_TRANSFER", "MESH_CACHE", "MESH_SEQUENCE_CACHE", 
#  "NORMAL_EDIT", "WEIGHTED_NORMAL", "UV_PROJECT", "UV_WARP", 
#  "VERTEX_WEIGHT_EDIT", "VERTEX_WEIGHT_MIX", "VERTEX_WEIGHT_PROXIMITY", 
#  "ARRAY", "BEVEL", "BOOLEAN", "BUILD", "DECIMATE", "EDGE_SPLIT", 
#  "NODES", "MASK", "MIRROR", "MESH_TO_VOLUME", "MULTIRES", "REMESH", 
#  "SCREW", "SKIN", "SOLIDIFY", "SUBSURF", "TRIANGULATE", 
#  "VOLUME_TO_MESH", "WELD", "WIREFRAME", "ARMATURE", "CAST", 
#  "CURVE", "DISPLACE", "HOOK", "LAPLACIANDEFORM", "LATTICE", 
#  "MESH_DEFORM", "SHRINKWRAP", "SIMPLE_DEFORM", "SMOOTH", 
#  "CORRECTIVE_SMOOTH", "LAPLACIANSMOOTH", "SURFACE_DEFORM", 
#  "WARP", "WAVE", "VOLUME_DISPLACE", "CLOTH", "COLLISION", 
#  "DYNAMIC_PAINT", "EXPLODE", "FLUID", "OCEAN", "PARTICLE_INSTANCE", 
#  "PARTICLE_SYSTEM", "SOFT_BODY", "SURFACE"]

#根据类型获取修改器（返回修改器名称）
def Get_By_Type(obj,typeName): 
    r = ""
    for mod in obj.modifiers:
        if mod.type == typeName:
            r = mod.name
            break
    return r

#根据类型获取全部修改器(返回修改器名称列表)
def Get_All_By_Type(obj,typeName): 
    r = []
    for mod in obj.modifiers:
        if mod.type == typeName:
            r.append(mod.name)
    return r

#清空
def Clear(obj):
    obj.modifiers.clear()

#移除(根据名称)
def Remove(obj,modifierName):
    obj.modifiers.remove(obj.modifiers[modifierName])

#拷贝
def Copy(targetObj,sourceObj,modifierName):
    Obj.Selection_Clear()
    Obj.Select_Set(targetObj,True)
    Obj.Acive_Set(sourceObj)
    bpy.ops.object.modifier_copy_to_selected(modifier = modifierName)

def Copy_All(targetObj,sourceObj):
    Obj.Selection_Clear()
    Obj.Select_Set(targetObj,True)
    Obj.Acive_Set(sourceObj)
    for mod in sourceObj.modifiers:
        bpy.ops.object.modifier_copy_to_selected(modifier = mod.name)

#应用，需要激活物体
def Apply_To_Active(modifierName):
    bpy.ops.object.modifier_apply(modifier=modifierName)


#精简
class Decimate:
    def Create(obj):
        mo = obj.modifiers.new("精简","DECIMATE")
        return mo.name

    #精简方式设置
    def Decimate_Type_Set(targetObj,modifierName,decimate_type):
        #COLLAPSE\UNSUBDIV\DISSOLVE
        targetObj.modifiers[modifierName].decimate_type = decimate_type
    
    def Decimate_Type_Get(targetObj,modifierName,decimate_type):
        return targetObj.modifiers[modifierName].decimate_type

    #迭代次数设置（只在UNSUBDIV里有用）
    def Iterations_Set(targetObj,modifierName,iterations):
        targetObj.modifiers[modifierName].iterations = iterations
    
    def Iterations_Get(targetObj,modifierName,iterations):
        return targetObj.modifiers[modifierName].iterations
    