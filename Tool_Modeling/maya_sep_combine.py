# -*- coding: utf-8 -*-
# 自制的常用的建模工具
import maya.cmds as cmds

def separate_objects():
    # 获取所选对象
    selected_objects = cmds.ls(selection=True, long=True)

    if not selected_objects:
        cmds.warning("No objects selected. Please select some objects.")
        return

    # 对每个选定的对象执行分离操作
    for obj in selected_objects:
        cmds.select(obj, replace=True)
        cmds.polySeparate()
        cmds.delete(obj, constructionHistory=True)

def detach_separate():
    name_split_skip = []
    face_num = []
    temp = []
    new_obj = []
    new_face_sel = []

    orig_face_sel = cmds.filterExpand(sm=34, ex=1)
    orig_obj_shape = cmds.listRelatives(orig_face_sel[0], parent=True)
    orig_obj = cmds.listRelatives(orig_obj_shape[0], parent=True)

    # 获取所选面的编号并存储在face_num中
    for step in range(len(orig_face_sel)):
        temp = orig_face_sel[step].split(".")
        name_split_skip.extend(temp)
        temp = []

    for step2 in range(0, len(name_split_skip), 2):
        face_num.append(name_split_skip[step2 + 1])

    # 复制原始对象
    new_obj = cmds.duplicate(orig_obj[0], un=True)
    cmds.delete(new_obj[0], ch=True)
    new_all_faces = cmds.ls(new_obj[0] + ".f[*]")

    # 为$newObj上的面选择创建新数组
    for step3 in range(len(face_num)):
        new_face_sel.append(new_obj[0] + "." + face_num[step3])

    # 删除原始面选择
    cmds.delete(orig_face_sel)

    # 删除副本上的反向面选择
    cmds.select(new_all_faces)
    cmds.select(new_face_sel, d=True)
    cmds.delete()
    cmds.select(new_obj[0])

def mergeAndDeleteHistory():
    selected_objects = cmds.ls(selection=True)

    if len(selected_objects) < 2:
        cmds.warning("Select at least two objects to merge.")
        return

    # Merge selected objects
    merged_object = cmds.polyUnite(selected_objects, ch=False, mergeUVSets=True, centerPivot=True)[0]

    # Delete history of merged object
    cmds.delete(merged_object, ch=True)
    cmds.select(merged_object, replace=True)

def center_pivot_to_selected():
    # 获取当前选择的物体
    selected_objects = cmds.ls(selection=True)

    if selected_objects:
        for obj in selected_objects:
            # 选择当前的物体
            cmds.select(obj)

            # 执行Center Pivot命令
            cmds.CenterPivot()

def centerPivotToOrigin():
    # 获取当前选择的物体列表
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("请先选择物体！")
        return

    # 遍历每个选择的物体
    for obj in selected_objects:
        # 获取物体的轴心点位置
        pivot_position = cmds.xform(obj, query=True, rotatePivot=True, worldSpace=True)

        # 将轴心点位置设置为坐标原点
        cmds.xform(obj, pivots=(0, 0, 0), worldSpace=True)

        # 输出操作信息
        print("将物体 {} 的轴心点移动到坐标原点。".format(obj))

def reverse_normals():
    # 获取当前选择的物体
    selected_objects = cmds.ls(selection=True,  long=True)

    if not selected_objects:
        cmds.warning("请先选择要反转法线的物体")
        return

    for obj in selected_objects:
        cmds.polyNormal(nm=3)
        cmds.delete(obj, constructionHistory = True)

def delete_joints():
    mesh_objects = cmds.ls(type='mesh', long=True)
    joints_objects = cmds.ls(type='joint', long=True)

    # 遍历所有 mesh 物体
    for obj in mesh_objects:
        skin_cluster = cmds.listConnections(obj, type='skinCluster')
        if skin_cluster:
            cmds.skinCluster(skin_cluster[0], edit=True, unbind=True)
            print "已解绑定蒙皮：{}".format(obj)

    # 删除所有骨骼
    if joints_objects:
        cmds.delete(joints_objects)
        print "已删除 {} 个骨骼对象".format(len(joints_objects))

def rename_object_to_material_name():
    # 获取当前选择的物体
    selected_objects = cmds.ls(selection=True)

    if selected_objects:
        for obj in selected_objects:
            # 获取物体的形状节点
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []

            if not shapes:
                print "物体 %s 没有形状节点." % obj
                continue

            # 连接的shadingEngines
            shadingEngines = cmds.listConnections(shapes, type="shadingEngine")

            if not shadingEngines:
                print "物体 %s 没有关联的着色引擎." % obj
                continue

            # 连接的材质
            materials = cmds.ls(cmds.listConnections(shadingEngines), materials=True)

            if not materials:
                print "物体 %s 没有关联的材质." % obj
                continue

            # 获取第一个关联材质的名称
            material_name = materials[0]

            # 将物体名称更改为材质名称
            cmds.rename(obj, material_name)


cmds.window("Detach&Combine", widthHeight=(600, 300))
cmds.columnLayout(adjustableColumn=True)

cmds.text(label="自动分离打断独立的部件")
cmds.button(label="separate", width=400, height=40, backgroundColor=(0.345, 0.525, 1.0), command="separate_objects()")

cmds.text(label="从一个物体上分离选择的面")
cmds.button(label="detach separate face", width=400, height=40, backgroundColor=(0.345, 0.525, 1.0), command="detach_separate()")

cmds.text(label="至少选择两个物体")
cmds.button(label="Combine", width=200, height=40, command="mergeAndDeleteHistory()")

cmds.text(label="重置轴心点到中心点")
cmds.button(label="center pivot", width=200, height=40, command="center_pivot_to_selected()")

cmds.text(label="轴心点移动到原点")
cmds.button(label="center Pivot To Origin", width=400, height=40, command="centerPivotToOrigin()")

cmds.text(label="翻转法线")
cmds.button(label="flip normals", width=200, height=40, command="reverse_normals()")

cmds.text(label="删除骨骼及蒙皮")
cmds.button(label="delete joints", width=200, height=40, command="delete_joints()")

cmds.text(label="命名物体为材质类型")
cmds.button(label="rename by mat", width=200, height=40, command="rename_object_to_material_name()")

cmds.showWindow()
