from cgitb import reset
from unittest import result
import bpy
import bmesh

#获取全部顶点Local位置 (坐标列表)
def Points_Position_Local_All_Get(meshObj):
    result = []
    for ver in meshObj.data.vertices:
        result.append(ver.co)
    return result

#获取全部顶点Local位置 (坐标列表)
def Points_Position_Local_All_Set(meshObj,positions):
    vers = meshObj.data.vertices
    for i in range(len(vers)):
        vers[i].co = positions[i]


#获得选中的点（index列表）
def Points_Select_Get(meshObj): 
    result = []
    for ver in meshObj.data.vertices:
        if ver.select:
            result.append(ver.index)
    return result

#获取顶点数量
def Points_count_Get(meshObj):
    return len(meshObj.data.vertices)

#选中点
def Points_Select_Set(meshObj,indexs):
    vers = meshObj.data.vertices
    for i in range(len(vers)):
        if i in (indexs): vers[i].select = True
        else: vers[i].select = False
#选中边
def Edge_Select_Set(meshObj,indexs):
    edges = meshObj.data.edges
    for i in range(len(edges)):
        if i in (indexs): edges[i].select = True
        else: edges[i].select = False

#选中点合并到中心
def Merge_Selected_Points_Center():
    bpy.ops.mesh.merge(type='CENTER')

#获取线的两个端点，由元组列表组成
def Edge_Vertices_Get(meshObj,edgeIndexs = -1):
    result = []
    if (type(edgeIndexs) is list): #输入的是edge的列表   
        for i in edgeIndexs:
            edge = meshObj.data.edges[i]
            verTuple = (edge.vertices[0],edge.vertices[1])
            result.append(verTuple)
    elif edgeIndexs == -1: #输入的是-1，返回全部
        for edge in meshObj.data.edges:
            verTuple = (edge.vertices[0],edge.vertices[1])
            result.append(verTuple)
    else: #输入的是序号，返回一个
        edge = meshObj.data.edges[edgeIndexs]
        return (edge.vertices[0],edge.vertices[1])
    return result
        
#获取与点相连的全部线
def Get_Linked_Edges(meshObj,verIndexs):
    bm = bmesh.new()
    bm.from_mesh(meshObj.data)
    bm.verts.ensure_lookup_table()
    result = None
    if type(verIndexs) is list:  
        result = [] 
        for i in verIndexs:
            r = []
            for edge in bm.verts[i].link_edges:
                r.append(edge.index)
            result.append(r)
    elif verIndexs == -1:
        result = [] 
        for ver in bm.verts:
            r = []
            for edge in ver.link_edges:
                r.append(edge.index)
            result.append(r)
    else:
        result = []
        for edge in bm.verts[verIndexs].link_edges:
            result.append(edge.index)
    bm.free()
    return result

