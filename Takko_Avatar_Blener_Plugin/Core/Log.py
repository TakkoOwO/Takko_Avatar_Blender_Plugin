import bpy

def ReportInfo(operator,info):
    operator.report({'INFO'},info)

def ReportWarning(operator,info):
    operator.report({'WARNING'},info)

def ReportError(operator,info):
    operator.report({'ERROR'},info)

def Error_Cancelled(operator,info):
    operator.report({'ERROR'},info)
    return {"CANCELLED"}

def Progress_Begin(min,max):
    bpy.context.window_manager.progress_begin(min,max)
def Progress_Update(value):
    bpy.context.window_manager.progress_update(value)
def Progress_End():
    bpy.context.window_manager.progress_end()
# 'DEBUG', 'INFO', 'OPERATOR', 'PROPERTY', 
# 'WARNING', 'ERROR', 'ERROR_INVALID_INPUT', 
# 'ERROR_INVALID_CONTEXT', 'ERROR_OUT_OF_MEMORY'