# -*- coding: utf-8 -*-

import maya.cmds as cmds

def Head_OuterCage(new_name="Head_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def UpperTorso_OuterCage(new_name="UpperTorso_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def LowerTorso_OuterCage(new_name="LowerTorso_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)

def LeftUpperLeg_OuterCage(new_name="LeftUpperLeg_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def LeftLowerLeg_OuterCage(new_name="LeftLowerLeg_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def LeftFoot_OuterCage(new_name="LeftFoot_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)

def RightUpperLeg_OuterCage(new_name="RightUpperLeg_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def RightLowerLeg_OuterCage(new_name="RightLowerLeg_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def RightFoot_OuterCage(new_name="RightFoot_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)

def LeftUpperArm_OuterCage(new_name="LeftUpperArm_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def LeftLowerArm_OuterCage(new_name="LeftLowerArm_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def LeftHand_OuterCage(new_name="LeftHand_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)

def RightUpperArm_OuterCage(new_name="RightUpperArm_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def RightLowerArm_OuterCage(new_name="RightLowerArm_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)
def RightHand_OuterCage(new_name="RightHand_OuterCage"):
    selected_objects = cmds.ls(selection=True, long=True)
    cmds.rename(selected_objects[0], new_name)

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

def create_spheres_and_parent_to_bones():
    # 骨骼名称和对应的球名称映射
    bone_sphere_mapping = {
        "Root": ["Root_Att"],
        "LowerTorso": ["WaistBack_Att", "WaistCenter_Att", "WaistFront_Att"],
        "UpperTorso": ["BodyFront_Att", "BodyBack_Att", "LeftCollar_Att", "Neck_Att", "RightCollar_Att"],
        "Head": ["FaceEye_Att","FaceMouth_Att", "Hat_Att", "Hair_Att", "HeadCenter_Att"],
        "LeftUpperArm": ["LeftShoulder_Att"],
        "LeftHand": ["LeftGrip_Att"],
        "RightUpperArm": ["RightShoulder_Att"],
        "RightHand": ["RightGrip_Att"],
        "LeftFoot": ["LeftFoot_Att"],
        "RightFoot": ["RightFoot_Att"]
    }

    for bone, spheres in bone_sphere_mapping.items():
        # 创建相应数量的球
        if isinstance(spheres, list):
            for sphere_name in spheres:
                sphere = cmds.polySphere(name=sphere_name)[0]
                # 查找骨骼
                if cmds.objExists(bone):
                    # 获取骨骼的世界坐标变换矩阵
                    bone_matrix = cmds.xform(bone, query=True, worldSpace=True, matrix=True)

                    # 获取物体名称中的"Front"和"Back"字符
                    if "Front" in sphere_name:
                        z_offset = 3
                    elif "Back" in sphere_name:
                        z_offset = -3
                    else:
                        z_offset = 0

                    # 获取物体名称中的"Left"和"Right"字符
                    if "Left" in sphere_name:
                        x_offset = 3
                    elif "Right" in sphere_name:
                        x_offset = -3
                    else:
                        x_offset = 0

                    # 设置球的父对象为骨骼
                    cmds.parent(sphere, bone)
                    # 将球的世界坐标变换矩阵设置为与骨骼相同，以匹配骨骼的位置和方向
                    cmds.xform(sphere, worldSpace=True, matrix=bone_matrix)
                    # 添加X轴和Z轴偏移
                    cmds.setAttr(sphere + ".translateX", x_offset)
                    cmds.setAttr(sphere + ".translateZ", z_offset)
                else:
                    cmds.warning("Can't find joint '%s', please confirm if it exists." % bone)

def replace_objects_with_locators():
    # 骨骼名称和对应的物体名称映射
    bone_sphere_mapping = {
        "Root": ["Root_Att"],
        "LowerTorso": ["WaistBack_Att", "WaistCenter_Att", "WaistFront_Att"],
        "UpperTorso": ["BodyFront_Att", "BodyBack_Att", "LeftCollar_Att", "Neck_Att", "RightCollar_Att"],
        "Head": ["FaceEye_Att","FaceMouth_Att", "Hat_Att", "Hair_Att", "HeadCenter_Att"],
        "LeftUpperArm": ["LeftShoulder_Att"],
        "LeftHand": ["LeftGrip_Att"],
        "RightUpperArm": ["RightShoulder_Att"],
        "RightHand": ["RightGrip_Att"],
        "LeftFoot": ["LeftFoot_Att"],
        "RightFoot": ["RightFoot_Att"]
    }

    for bone, spheres in bone_sphere_mapping.items():
        if cmds.objExists(bone):
            for sphere_name in spheres:
                full_object_name =  sphere_name
                if cmds.objExists(full_object_name):
                    # 获取物体的坐标
                    translation = cmds.xform(full_object_name, query=True, translation=True, worldSpace=True)
                    # 删除物体
                    cmds.delete(full_object_name)
                    # 在相同位置创建locator，注意父对象是骨骼
                    locator = cmds.spaceLocator(name=sphere_name)[0]
                    cmds.setAttr(locator + ".translateX", translation[0])
                    cmds.setAttr(locator + ".translateY", translation[1])
                    cmds.setAttr(locator + ".translateZ", translation[2])
                    cmds.setAttr(locator + ".overrideEnabled", 1)
                    cmds.setAttr(locator + ".overrideColor",14)
                    cmds.parent(locator, bone)
                else:
                    cmds.warning("未找到名为'%s'的物体，请确保物体存在。" % full_object_name)
        else:
            cmds.warning("未找到名为'%s'的骨骼，请确保骨骼存在。" % bone)

def reset_rotation():
    object_names = {
        "Root": ["Root_Att"],
        "LowerTorso": ["WaistBack_Att", "WaistCenter_Att", "WaistFront_Att"],
        "UpperTorso": ["BodyFront_Att", "BodyBack_Att", "LeftCollar_Att", "Neck_Att", "RightCollar_Att"],
        "Head": ["FaceEye_Att","FaceMouth_Att", "Hat_Att", "Hair_Att", "HeadCenter_Att"],
        "LeftUpperArm": ["LeftShoulder_Att"],
        "LeftHand": ["LeftGrip_Att"],
        "RightUpperArm": ["RightShoulder_Att"],
        "RightHand": ["RightGrip_Att"],
        "LeftFoot": ["LeftFoot_Att"],
        "RightFoot": ["RightFoot_Att"]
    }

    for category, names in object_names.items():
        for obj_name in names:
            if cmds.objExists(obj_name):
                cmds.setAttr(obj_name + ".rotate", 0, 0, 0)


cmds.window(title="Rename Body OutCage", sizeable=False)
cmds.columnLayout(adjustableColumn=True)

cmds.text(label="脊椎")
cmds.button(label='Head_OuterCage', width=400, height=30, command="Head_OuterCage()")
cmds.button(label='UpperTorso_OuterCage', width=400, height=30, command="UpperTorso_OuterCage()")
cmds.button(label='LowerTorso_OuterCage', width=400, height=30, command="LowerTorso_OuterCage()")
cmds.text(label="左腿")
cmds.button(label='LeftUpperLeg_OuterCage', width=400, height=30, command="LeftUpperLeg_OuterCage()")
cmds.button(label='LeftLowerLeg_OuterCage', width=400, height=30, command="LeftLowerLeg_OuterCage()")
cmds.button(label='LeftFoot_OuterCage', width=400, height=30, command="LeftFoot_OuterCage()")
cmds.text(label="右腿")
cmds.button(label='RightUpperLeg_OuterCage', width=400, height=30, command="RightUpperLeg_OuterCage()")
cmds.button(label='RightLowerLeg_OuterCage', width=400, height=30, command="RightLowerLeg_OuterCage()")
cmds.button(label='RightFoot_OuterCage', width=400, height=30, command="RightFoot_OuterCage()")
cmds.text(label="左手")
cmds.button(label='LeftUpperArm_OuterCage', width=400, height=30, command="LeftUpperArm_OuterCage()")
cmds.button(label='LeftLowerArm_OuterCage', width=400, height=30, command="LeftLowerArm_OuterCage()")
cmds.button(label='LeftHand_OuterCage', width=400, height=30, command="LeftHand_OuterCage()")
cmds.text(label="右手")
cmds.button(label='RightUpperArm_OuterCage', width=400, height=30, command="RightUpperArm_OuterCage()")
cmds.button(label='RightLowerArm_OuterCage', width=400, height=30, command="RightLowerArm_OuterCage()")
cmds.button(label='RightHand_OuterCage', width=400, height=30, command="RightHand_OuterCage()")
cmds.text(label="重置OutCage模型到坐标原点")
cmds.button(label='centerPivotToOrigin', width=400, height=30, command="centerPivotToOrigin()")
cmds.text(label="添加虚拟体")
cmds.button(label="create_spheres_help", width=400, height=30, command="create_spheres_and_parent_to_bones()")
cmds.button(label="replace_objects_with_locators", width=400, height=30, command="replace_objects_with_locators()")
cmds.button(label="reset_rotation", width=400, height=30, command="reset_rotation()")
cmds.showWindow()
