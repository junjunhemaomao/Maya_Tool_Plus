import maya.cmds as cmds

def count_models_in_scene():
    # 获取场景中的所有模型
    all_meshes = cmds.ls(type='mesh', long=True)
    all_transforms = cmds.listRelatives(all_meshes, parent=True, fullPath=True)

    # 统计模型的数量
    model_count = len(all_transforms)

    print(f"Total number of models in the scene: {model_count}")
    return model_count


# 调用函数统计场景内的模型数量
count_models_in_scene()
