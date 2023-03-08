import bpy
# "CAMERA_SOLVER", "FOLLOW_TRACK", "OBJECT_SOLVER", "COPY_LOCATION", "COPY_ROTATION", 
# "COPY_SCALE", "COPY_TRANSFORMS", "LIMIT_DISTANCE", "LIMIT_LOCATION", "LIMIT_ROTATION", 
# "LIMIT_SCALE", "MAINTAIN_VOLUME", "TRANSFORM", "TRANSFORM_CACHE", "CLAMP_TO", 
# "DAMPED_TRACK", "IK", "LOCKED_TRACK", "SPLINE_IK", "STRETCH_TO", "TRACK_TO", 
# "ACTION", "ARMATURE", "CHILD_OF", "FLOOR", "FOLLOW_PATH", "PIVOT", "SHRINKWRAP"

#跟随路径
class FOLLOW_PATH:
    def Add(obj):
        con = obj.constraints.new("FOLLOW_PATH")
        return con.name

    #偏移系数设置
    def Offset_Factor_Set(obj,conName,value):
        obj.constraints[conName].offset_factor = value
        print(obj.constraints[conName].offset_factor)

    #是否固定位置
    def Use_Fixed_Location_Set(obj,conName,value_bool):
        obj.constraints[conName].use_fixed_location = value_bool
    
    #目标设置
    def Target_Set(obj,conName,curveObj):
        obj.constraints[conName].target = curveObj
