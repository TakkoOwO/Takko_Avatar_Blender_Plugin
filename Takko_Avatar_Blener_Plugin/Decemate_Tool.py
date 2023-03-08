import bpy
from .Core import Obj
from .Core import Log
from .Core import Modifier
from .Core import Mode
from .Core import Mesh
from .Core import ShapeKey
class Decimate_Tool_OT_Un_Subdevide(bpy.types.Operator):
    bl_idname = "decimate_tool.un_subdevide"
    bl_label = "反细分"
    bl_description = "在编辑模式中点击，可以选中反细分之后的全部线段，反选后删除可以获得精简后的模型"

    def execute(self,context): 
        #编辑模式
        if not Mode.IsMode("EDIT_MESH"):
            return Log.Error_Cancelled(self,"需要在编辑网格模式下操作")
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')

        #获取活动物体
        meshObj = Obj.Acive_Get()
        #切物体模式
        Mode.Switch_Object()
        #克隆一个物体
        new_Obj = Obj.Clone(meshObj,False)
        #添加精简修改器
        modifierName = Modifier.Decimate.Create(new_Obj)
        Modifier.Decimate.Decimate_Type_Set(new_Obj,modifierName,"UNSUBDIV")
        Modifier.Decimate.Iterations_Set(new_Obj,modifierName,2)
        #应用修改器
        Obj.Acive_Set(new_Obj)
            #清除全部的ShapeKey
        if ShapeKey.Count_Get(new_Obj) > 0:
            ShapeKey.Active_Index_Set(new_Obj,0)
            ShapeKey.Delete_All()
        Modifier.Apply_To_Active(modifierName)
        
        #获取精简前后的全部的顶点
        point_Positions =  Mesh.Points_Position_Local_All_Get(meshObj)
        points_Positions_new = Mesh.Points_Position_Local_All_Get(new_Obj)
        
        #获取精简后的连接情况（边信息）
        edges_new = Mesh.Edge_Vertices_Get(new_Obj,-1)
        link_infos = []
        for i in range (len(edges_new)):
            link_infos.append([-1,-1])
        #删除克隆物体
        Obj.Delete(new_Obj)

        #找出精简后的点
        points_decimate_indexs = []
            #显示进度
        Log.Progress_Begin(0,len(point_Positions))
        check_index_a = 0
        for index_b in range(len(point_Positions)):
            Log.Progress_Update(index_b)
            for index_a in range(check_index_a,len(points_Positions_new)):
                if point_Positions[index_b] == points_Positions_new[index_a]:  
                    points_decimate_indexs.append(index_b)
                    #用相同的点更新连接信息
                    for x in range(len(edges_new)):
                        if edges_new[x][0] == index_a: link_infos[x][0] = index_b
                        elif edges_new[x][1] == index_a: link_infos[x][1] = index_b

            index_a += 1
        Log.Progress_End()
        
        #获取点连接的情况
        linked_edges = Mesh.Get_Linked_Edges(meshObj,-1)
        
        #对比所有的点-点连接信息，确定经过哪两个线相连
        resultEdges = []
        for link in link_infos:
            ver1,ver2 = link[0],link[1]
            edges1 = linked_edges[ver1]
            edges2 = linked_edges[ver2]
            ends1 = []
            ends2 = []
            for edge1 in edges1:
                p1,p2 = Mesh.Edge_Vertices_Get(meshObj,edge1)
                anotherEnd = p2
                if ver1 == p2: anotherEnd = p1
                ends1.append(anotherEnd)
            for edge2 in edges2:
                p1,p2 = Mesh.Edge_Vertices_Get(meshObj,edge2)
                anotherEnd = p2
                if ver2 == p2: anotherEnd = p1
                ends2.append(anotherEnd)
            
            get = False
            for i in range(len(ends1)):
                if get: break
                if ends1[i] == ver2:
                    resultEdges.append(edges1[i])
                    get = True
                    
            if not get:
                for i in range(len(ends1)):
                    for a in range(len(ends2)):
                        if ends2[a] == ends1[i]:
                            resultEdges.append(edges1[i])
                            resultEdges.append(edges2[a])
                            get = True
                            break
            if not get:
                print("!"*10 + "="*20+ "没有获取")
        
        
        #选中顶点,切换编辑模式
        Obj.Acive_Set(meshObj)
        #Mesh.Points_Select_Set(meshObj,points_decimate_indexs)
        Mesh.Edge_Select_Set(meshObj,resultEdges)
        Mode.Switch_Edit()
        return{"FINISHED"}


class Decimate_Tool_OT_To_Subdevide(bpy.types.Operator):
    bl_idname = "decimate_tool.to_subdevide"
    bl_label = "移到细分点"
    bl_description = "将顶点移动到细分之后的位置,可能造成法向问题，全选面，网格-法向-从面设置，可以解决"

    def execute(self,context): 
        #获取活动物体
        meshObj = Obj.Acive_Get()

        if Obj.Type_Get(meshObj) != "MESH":
            return Log.Error_Cancelled(self,"活动物体需要是网格体")

        modifier_old = Modifier.Get_By_Type(meshObj,"SUBSURF")
        if modifier_old is None:
            return Log.Error_Cancelled(self,"物体需要挂载表面细分")
        
        #切物体模式
        Mode.Switch_Object()
        
        #制作一个参考物体，用于应用表面细分
        sub_obj = Obj.Clone(meshObj,False)
        Modifier.Copy(sub_obj,meshObj,modifier_old)
        modifier_new = Modifier.Get_By_Type(sub_obj,"SUBSURF")

        #应用修改器
        Obj.Acive_Set(sub_obj)
            #清除全部的ShapeKey
        if ShapeKey.Count_Get(sub_obj) > 0:
            ShapeKey.Active_Index_Set(sub_obj,0)
            ShapeKey.Delete_All()
        Modifier.Apply_To_Active(modifier_new)
        
        #获取精简前后的全部的顶点位置
        point_Positions =  Mesh.Points_Position_Local_All_Get(meshObj)
        points_Positions_new = Mesh.Points_Position_Local_All_Get(sub_obj)
        
        #删除克隆物体
        Obj.Delete(sub_obj)

        #设置顶点位置
        for i in range(len(point_Positions)):
            point_Positions[i] = points_Positions_new[i]
        Mesh.Points_Position_Local_All_Set(meshObj,point_Positions)

        #删除修改器
        Modifier.Remove(meshObj,modifier_old)

        Obj.Acive_Set(meshObj)
        Mode.Switch_Edit()
        
        return{"FINISHED"}

