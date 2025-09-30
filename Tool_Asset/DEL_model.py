import maya.cmds as cmds


# 检查场景内所有模型的UV是否一样，并对一样的进行分组
def get_vertex_uvs(obj):
    """Returns a tuple of UV coordinates for each vertex of the mesh object."""
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
    if not shapes:
        return None

    uv_coords = []
    for shape in shapes:
        vertices = cmds.polyEvaluate(shape, vertex=True)
        for i in range(vertices):
            uvs = cmds.polyListComponentConversion(f'{shape}.vtx[{i}]', fromVertex=True, toUV=True)
            if uvs:
                uv_coords.extend(cmds.polyEditUV(uvs, query=True))

    return tuple(sorted(uv_coords)) if uv_coords else None


def group_by_uv():
    # 获取场景中的所有模型
    all_meshes = cmds.ls(type='mesh', long=True)
    all_transforms = cmds.listRelatives(all_meshes, parent=True, fullPath=True)

    # 创建一个字典来存储模型的UV和对应的模型
    uv_dict = {}

    # 遍历所有的模型
    for transform in all_transforms:
        # 获取模型的UV信息
        uvs = get_vertex_uvs(transform)

        if uvs is None:
            continue

        # 将UV信息作为键，将模型添加到字典
        if uvs in uv_dict:
            uv_dict[uvs].append(transform)
        else:
            uv_dict[uvs] = [transform]

    # 创建新的组
    for i, (uvs, transforms) in enumerate(uv_dict.items(), start=1):
        if len(transforms) > 1:
            group_name = f'UV_Group_{i}'
            cmds.group(transforms, name=group_name)
            print(f"Grouped models: {transforms} into {group_name}")
        else:
            print(f"No grouping needed for model: {transforms[0]}")


# ——————————————————————
# 删除组内多余的模型，保留命名最短的模型
def keep_shortest_name_in_group(group_name):
    # 获取组内的所有模型
    children = cmds.listRelatives(group_name, children=True, fullPath=True) or []

    # 如果组内只有一个模型，无需处理
    if len(children) <= 1:
        return

    # 找到字符数量最少的模型
    shortest_name = None
    shortest_name_length = float('inf')
    for child in children:
        model_name = cmds.ls(child, shortNames=True)[0]
        name_length = len(model_name)
        if name_length < shortest_name_length:
            shortest_name = child
            shortest_name_length = name_length

    # 删除组内其他模型
    for child in children:
        if child != shortest_name:
            cmds.delete(child)
            print(f"Deleted model: {child}")


def keep_shortest_name_in_all_groups():
    # 获取场景中的所有组
    all_transforms = cmds.ls(type='transform')
    all_groups = [grp for grp in all_transforms if cmds.listRelatives(grp, children=True, type='transform')]

    # 遍历所有组，保留字符数量最少的模型
    for group in all_groups:
        keep_shortest_name_in_group(group)


# 调用函数处理所有模型
group_by_uv()
# 调用函数处理所有组
keep_shortest_name_in_all_groups()
