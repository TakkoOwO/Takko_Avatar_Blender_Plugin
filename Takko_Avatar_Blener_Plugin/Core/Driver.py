import bpy

#在物体的某个通道上新建一个脚本表达式驱动器
#channel in ["location","rotation_euler","rotation_quaternion","scale"]
#driverType in ["AVERAGE", "SUM", "SCRIPTED", "MIN", "MAX"]
def New_Driver(obj,channel,channelIndex,driverType):
    #获取这个物体的动画信息，若没有则创建
    animData = obj.animation_data
    if animData is None: animData = obj.animation_data_create()
    #获取动画信息中的驱动器信息（Fcurves的集合）
    FCurves = animData.drivers
    #从中获取/创建一个特定通道的Fcurve
    target_FCurve = FCurves.find(channel,index = channelIndex)
    if target_FCurve is None:
        target_FCurve = FCurves.new(channel,index = channelIndex)
    #获取这个Fcurve上的驱动器
    driver = target_FCurve.driver
    #清除掉驱动器上的全部变量
    vars = driver.variables
    for var in vars: vars.remove(var)
    #设置其类型为脚本
    driver.type = driverType

 #给驱动器设置表达式
def Set_Script(obj,channel,channelIndex,script):
    driver = obj.animation_data.drivers.find(channel,index = channelIndex).driver
    driver.expression = script

#给某一个驱动器输入变量（需要提前创建一个变量结构体）
def Add_Variable(obj,channel,channelIndex,varStruct):
    driver = obj.animation_data.drivers.find(channel,index = channelIndex).driver
    vars = driver.variables
    var = vars.new()

    var.name = varStruct.name
    var.type = varStruct.type
    
    tar = var.targets[0]
    tar.id = varStruct.obj.id_data
    tar.bone_target = varStruct.bone_target
    tar.rotation_mode = varStruct.rotation_mode
    tar.transform_space = varStruct.transform_space
    tar.transform_type = varStruct.transform_type

#变量结构体，存储它的信息
class VarStruct:
        def __init__(self):
            self.name = "untitled"
            self.type = 'TRANSFORMS'

            self.obj = None
            self.bone_target = ""
            self.rotation_mode = "AUTO"
            self.transform_space = "LOCAL_SPACE" 
            #[WORLD_SPACE,LOCAL_SPACE,TRANSFORM_SPACE]
            self.transform_type = "LOC_X" 
            #[LOC_X, LOC_Y, LOC_Z, 
            # ROT_X, ROT_Y, ROT_Z, ROT_W, 
            # SCALE_X, SCALE_Y, SCALE_Z, SCALE_AVG]