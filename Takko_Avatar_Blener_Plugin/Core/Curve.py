import bpy

#获取Curve物体中Splin的数量(一个曲线物体中可以有多个曲线)
def Splin_Count_Get(curveObj):
    return len(curveObj.data.splines)

def Test(curveObj,index):
    spline = curveObj.data.splines[index]
    print(spline.type)

#获取UV顶点数量
def Get_UV(curveObj):
    u = curveObj.data.resolution_u * (len(curveObj.data.splines[0].points) - 1)
    v = 0
    if (curveObj.data.bevel_mode == "ROUND"):
        v = 4 + curveObj.data.bevel_resolution * 2
    elif (curveObj.data.bevel_mode == "PROFILE"):
        v = 4 + curveObj.data.bevel_resolution * 4
    else:
        bevelObj = curveObj.data.bevel_object
        if bevelObj is not None:
            if bevelObj.data.splines[0].use_cyclic_u:
                v = bevelObj.data.resolution_u * (len(bevelObj.data.splines[0].points))
            else:
                v = bevelObj.data.resolution_u * (len(bevelObj.data.splines[0].points) - 1)
    return (u,v)

