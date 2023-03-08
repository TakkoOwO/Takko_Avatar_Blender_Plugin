lsLeft=["left","Left","LEFT",".L"]
lsRight = ["right","Right","RIGHT",".R"]

#获取镜像的名称
def Get_Name_Mirror(name):
    newName = None
    for i in range(len(lsLeft)):
        if lsLeft[i] in name:
            newName = name.replace(lsLeft[i],lsRight[i])
            break
        elif lsRight[i] in name:
            newName = name.replace(lsRight[i],lsLeft[i])
            break
    return newName

#获取名称的方向，0左1右 -1无
def Get_Name_Direction(name):
    for i in range(len(lsLeft)):
        if lsLeft[i] in name:
            return 0
        elif lsRight[i] in name:
            return 1
    return -1


#动骨名称形式为 前缀-名称-动骨序号-关节序号.方向 sp_hair_001_01.L 
#也可能没有动骨序号 sp_ear_02.L sp_tail_03
#分析动骨名称信息，如果不是动骨名，返回None
#如果是，返回（名称，动骨序号，关节序号，方向）
def Spring_Bone_Name_Check(name, prefix = "sp"):
    if name[0: len(prefix)] != prefix or name[len(prefix)] != "_": return None
    flag = len(prefix) + 1
    #截取动骨名称
    spring_Name = None
    for i in range(flag,len(name)):
        if name[i] == "_": 
            spring_Name = name[flag:i]
            flag = i + 1
            break
    if (spring_Name is None): return None
    spring_index = 0
    joint_index = 1
    direction = -1
    #通过下一个"_"获取信息
    for i in range(flag,len(name)):
        if name[i] == "_" or name[i] == "." or i == len(name) - 1:
            if i - flag == 3:
                spring_index = int(name[flag:i])
                flag = i + 1
                joint_index = int(name[flag:flag + 2])
                flag += 2
                break
            elif i - flag == 2:
                spring_index = 0
                joint_index = int(name[flag:i])
                flag = i
                break
            elif i == len(name) - 1:
                spring_index = 0
                joint_index = int(name[flag:i+1])
                flag = i
            else: return None
    #获取方向
    if flag <= len(name) - 2:
        if name[flag:flag + 2] == ".L": direction = 0
        elif name[flag:flag + 2] == ".R": direction = 1

    return (spring_Name,spring_index,joint_index,direction)

def Spring_Bone_Name_Build(spring_Name,spring_index,joint_index,direction,prefix = "sp"):
    name = None
    suffix = None
    if direction == 0: suffix = ".L"
    elif direction == 1: suffix = ".R"
    else: suffix = ""

    if spring_index == 0:
        #sp_tail_02.R
        name = "{}_{}_{:0>2}{}".format(prefix,spring_Name,joint_index,suffix)
    else:
        #sp_hair_015_02.R
        name = "{}_{}_{:0>3}_{:0>2}{}".format(prefix,spring_Name,spring_index,joint_index,suffix)
    return name



            


    


