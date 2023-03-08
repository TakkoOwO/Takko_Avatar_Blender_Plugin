import bpy

#获取形态键数量
def Count_Get(meshObj):
    if (meshObj.data.shape_keys is None): return 0
    else: return len(meshObj.data.shape_keys.key_blocks)

#获取活动形态键序号
def Active_Index_Get(meshObj):
    return meshObj.active_shape_key_index
#设置活动形态键序号 
def Active_Index_Set(meshObj,index):
    meshObj.active_shape_key_index = index

#获取形态键中全部点的位置
def Position_Get(meshObj,shapeKeyIndex):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    result = []
    for p in shapeKey.data:
        result.append(p.co)
    return result

#更新形态键顶点位置(需要输入一个顶点位置列表)
def Position_Set(meshObj,shapeKeyIndex,positions):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    for i in range(len(positions)):
        shapeKey.data[i].co = positions[i]
  
#获取名称
def Name_Get(meshObj,shapeKeyIndex):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    return shapeKey.name
#设置名称
def Name_Set(meshObj,shapeKeyIndex,name):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    shapeKey.name = name

#根据名称获取序号，没有则返回-1
def Get_Index_By_Name(meshObj,name):
    count = Count_Get(meshObj)
    for i in range(count):
        shapeKey = meshObj.data.shape_keys.key_blocks[i]
        if shapeKey.name == name: return i
    return -1

#获取是否Mute
def Get_Mute(meshObj,shapeKeyIndex):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    return shapeKey.mute
#设置Mute
def Set_Mute(meshObj,shapeKeyIndex,blMute):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    shapeKey.mute = blMute

#获取值
def Get_Value(meshObj,shapeKeyIndex):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    return shapeKey.value
#设置值
def Set_Value(meshObj,shapeKeyIndex,value):
    shapeKey = meshObj.data.shape_keys.key_blocks[shapeKeyIndex]
    shapeKey.value = value
#值全归零
def Reset_All_Value(meshObj):
    for shapeKey in meshObj.data.shape_keys.key_blocks:
        shapeKey.value = 0

#混合出一个新的形态键
def Generate_Mixed():
    bpy.ops.object.shape_key_add(from_mix=True)

#创建一个新的形态键
def Add_New():
    bpy.ops.object.shape_key_add(from_mix=False)

#镜像形态键
def Mirror_Active():
    bpy.ops.object.shape_key_mirror(use_topology=False) 

#删除形态键
def Delete_Active():
    bpy.ops.object.shape_key_remove(all=False)

#删除全部形态键
def Delete_All():
    bpy.ops.object.shape_key_remove(all=True)

#移动活动形态键
def Move_Active(meshObj,offset):
    if offset > 0:
        for i in range(offset):
            bpy.ops.object.shape_key_move(type='DOWN')
    elif offset < 0:
        for i in range(-offset):
            bpy.ops.object.shape_key_move(type='UP')
    