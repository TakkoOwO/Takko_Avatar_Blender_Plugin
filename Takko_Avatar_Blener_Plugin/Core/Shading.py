import bpy

def AO_Bake(useClear):
    #https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.bake
    bpy.ops.object.bake(
        use_clear = useClear,
        target = 'IMAGE_TEXTURES',
        use_selected_to_active = False,
        type = "AO"
        )

#获取物体的全部材质槽（传回一个string的list，里面是材质槽的名称，如果槽里没有材质球，则名称为空字符串）
def Material_Slot_All_Get(obj):
    return (obj.material_slots.keys())

#根据材质名称获取选中的Node名称
def Node_Acive_Get_From_Material(material_name):
    material = bpy.data.materials[material_name]
    node_active = material.node_tree.nodes.active
    return node_active.name

#根据材质球和里面的材质名称获取材质的类型 (暂未找到Node类型合集，只能挨个测试)
def Node_Type_Get(material_name,node_name):
    material = bpy.data.materials[material_name]
    node = material.node_tree.nodes[node_name]
    return node.type

#获取TexImage节点上面的图像
def Imgae_Get_From_TexImageNode(material_name,node_name):
    material = bpy.data.materials[material_name]
    node = material.node_tree.nodes[node_name]
    if node.type == "TEX_IMAGE":
        image = node.image
        if image != None:
            return image.name
    return ""

#获取Data中的全部Image
def Image_All_Get():
    images = bpy.data.images
    image_names = []
    for image in bpy.data.images:
        image_names.append(image.name)
    return image_names

#创建Image
def Image_Create(Image_Name,width,height):
    bpy.data.images.new(Image_Name,width,height)

#删除Image
def Image_Delete(Image_Name):
    bpy.data.images.remove(bpy.data.images[Image_Name])

#获得Image的尺寸
def Image_Size_Get(Image_Name):
    return bpy.data.images[Image_Name].size

#获得全部像素
def Pixels_Get(Image_Name):
    #你敢信，这个pixels居然是blender内部参数
    return list(bpy.data.images[Image_Name].pixels)

#设置全部像素
def Pixels_Set(Image_Name,pixels):
    bpy.data.images[Image_Name].pixels = pixels

#刷新图片
def Image_Update(Image_Name):
    bpy.data.images[Image_Name].update()