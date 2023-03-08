import bpy

#切换到编辑模式
def Switch_Edit():
    mode = bpy.context.mode
    if mode in ['EDIT_MESH','EDIT_CURVE','EDIT_ARMATURE']:
        return
    else:
        bpy.ops.object.mode_set(mode = "EDIT")



#切换到物体模式
def Switch_Object():
    mode = bpy.context.mode
    if mode == "OBJECT":
        return
    else:
        bpy.ops.object.mode_set(mode = "OBJECT")

#是否是某个模式(以下可选)
# ["EDIT_MESH", "EDIT_CURVE", "EDIT_CURVES", "EDIT_SURFACE", 
# "EDIT_TEXT", "EDIT_ARMATURE", "EDIT_METABALL", "EDIT_LATTICE", 
# "POSE", "SCULPT", "PAINT_WEIGHT", "PAINT_VERTEX", "PAINT_TEXTURE", 
# "PARTICLE", "OBJECT", "PAINT_GPENCIL", "EDIT_GPENCIL", "SCULPT_GPENCIL", 
# "WEIGHT_GPENCIL", "VERTEX_GPENCIL", "SCULPT_CURVES"]
def IsMode(modeName):
    if bpy.context.mode == modeName: return True
    else: return False
    
def Is_Edit():
    if bpy.context.mode in["EDIT_MESH","EDIT_CURVE","EDIT_SURFACE",
    "EDIT_TEXT","EDIT_ARMATURE","EDIT_METABALL","EDIT_LATTICE"]: return True
    else: return False  

def Is_Object():
    if bpy.context.mode == "OBJECT": return True
    else: return False 




#['OBJECT', 'EDIT', 'POSE', 'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 
# 'TEXTURE_PAINT', 'PARTICLE_EDIT', 'EDIT_GPENCIL', 'SCULPT_GPENCIL', 
# 'PAINT_GPENCIL', 'WEIGHT_GPENCIL', 'VERTEX_GPENCIL', 'SCULPT_CURVES']
#def ModeSet(modeName):
