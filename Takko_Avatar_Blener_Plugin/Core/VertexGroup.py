import bpy
#获取全部顶点组名称
def Names_Get_All(obj):
    r = []
    for vtg in obj.vertex_groups:
        r.append(vtg.name)
    return r

#重命名顶点组
def Vtg_Rename(obj,oldName,newName): 
    obj.vertex_groups[oldName].name = newName

#获取顶点组数量
def Count_Get(obj): 
    return len(obj.vertex_groups)

#获取活动的顶点组的index
def Active_Index_Get(obj): 
    return obj.vertex_groups.active_index

#获取特定点的顶点组权重
def Weight_Get(obj,vtgIndex,vIndex): 
    weight = 0
    try:
        weight = obj.vertex_groups[vtgIndex].weight(vIndex)
    except:
        weight = 0
    return weight

#设置顶点组权重
def Weight_Set(obj,vtgIndex,vIndexs,weight):
    if type(vIndexs) is int: vIndexs = [vIndexs]
    obj.vertex_groups[vtgIndex].add(vIndexs,weight,"REPLACE")
    return

#从顶点组中删除顶点权重
def Weight_Clear(obj,vtgIndex,vIndexs): 
    obj.vertex_groups[vtgIndex].remove(vIndexs)
    return

#平均权重
def Average_Weight(meshObj,points):
    for i in range(Count_Get(meshObj)):
        weight_taotal = 0
        for ver in points:
            weight_taotal += Weight_Get(meshObj,i,ver)
        if weight_taotal == 0: continue
        weight_average = weight_taotal / len(points)
        for ver in points:
            Weight_Set(meshObj,i,ver,weight_average)

#创建顶点组
def Create(meshObj,vtgName):
    meshObj.vertex_groups.new(name =vtgName)

#移除顶点组
def Remove(meshObj,vtgName):
    meshObj.vertex_groups.remove(meshObj.vertex_groups[vtgName])

#获取不空的顶点组
def Non_Empty_Group_All_Get(meshObj):
    #获取不空的序号
    nonEmpty_indexes = set()
    for vertice in meshObj.data.vertices:
        for vgrp in vertice.groups:
            if vgrp.weight > 0.0001:
                nonEmpty_indexes.add(vgrp.group)
    nonEmpty_vtgs = []
    for index in nonEmpty_indexes:
        nonEmpty_vtgs.append(meshObj.vertex_groups[index].name)
    return nonEmpty_vtgs



#移除空的顶点组,返回一共清空了几个
def Empty_Group_All_Remove(meshObj):
    #获取全部的顶点组名称组成set
    all_vtgs = set(Names_Get_All(meshObj))
    #差集
    empty_vtgs = all_vtgs - set(Non_Empty_Group_All_Get(meshObj))
    #清除
    for vtg in empty_vtgs:
        meshObj.vertex_groups.remove(meshObj.vertex_groups[vtg])
    return len(empty_vtgs)
        




