# -*- coding: utf-8 -*-
#Roblox绑定
import maya.cmds as cmds

def create_body_joints():
    joints_body_data = {
        # 脊柱
        'Root': (0, 0, 0),  'LowerTorso': (0, 2.067+62, 0),
        'UpperTorso': (0, 18.384+62, 0.931), 'Head': (0, 55.503+62, -1.433), 'DynamicHead': (0, 58.581+62, -1.433),
        # 下巴
        'Chin': (0, 57.323+62, 16.026),
        # 舌头，牙齿
        'Jaw': (0, 64.172+62, 4.179), 'LowerTeethRoot': (0, 64.172+62, 4.179), 'TongueRoot': (0, 64.172+62, 4.179),
        'TongueBase': (0, 60.647+62, 10.211), 'TongueTip': (0, 60.070+62, 17.868),
        # 嘴巴
        'LeftUpperOuterMouth': (3.305, 60.033+62, 19.656), 'LeftLowerOuterMouth': (3.305, 58.990+62, 19.656),
        'LeftLowerCornerMouth': (5.449, 60.144+62, 19.072),
        # 脸颊
        'LeftCheek': (18.781, 65.742+62, 7.529),
        # 眼睛
        'LeftEyeRoot': (7.892, 76.583+62, 2.493),
        'LeftUpperEyelid': (7.892, 76.583+62, 2.493), 'LeftUpperInnerEyelid': (6.288, 80.467+62, 18.356),
        'LeftUpperOuterEyelid': (12.103, 80.467+62, 16.033),
        'LeftLowerEyelid': (7.892, 76.583+62, 2.493), 'LeftLowerInnerEyelid': (5.847, 74.849+62, 18.356),
        'LeftLowerOuterEyelid': (11.662, 74.849+62, 16.033),
        # 眉弓
        'LeftInnerBrow': (5.363, 84.424+62, 19.334), 'LeftOuterBrow': (13.798, 84.633+62, 15.194),
        # 手
        'LeftUpperArm': (33.336, 41.653+62, -1.744), 'LeftLowerArm': (38.472, 22.092+62, -3.607),
        'LeftHand': (42.65, 1.020+62, -2.825),
        # 脚
        'LeftUpperLeg': (15.7, -4.859+62, 2.944), 'LeftLowerLeg': (14.872, -36.508+62, 2.711),
        'LeftFoot': (14.898, -61.702+62, -0.685)
    }

    cmds.headsUpMessage("Roblox Joint V1.0 ")
    # set the unit to centimeters
    cmds.currentUnit(linear='cm')
    # confirm the new unit
    unit = cmds.currentUnit(q=True, linear=True)
    print('Current linear unit: {}'.format(unit))

    # clear the current selection
    cmds.select(clear=True)

    for name, pos in joints_body_data.items():
        cmds.joint(p=pos, n=name, relative=True)
        cmds.select(clear=True)

def mirror_left_joints():
    selected = cmds.ls('LeftUpperArm','LeftUpperLeg',
                        'LeftLowerOuterMouth','LeftUpperOuterMouth','LeftLowerCornerMouth','LeftCheek',
                        'LeftEyeRoot','LeftInnerBrow','LeftOuterBrow')
    for s in selected:
        # Check if name starts with "l_"
        if not s.startswith("Left"):
            continue
        # Replace first "l_" with "r_"
        mirror_name = s.replace("Left", "Right", 1)
        cmds.mirrorJoint(s, mirrorYZ=True, mirrorBehavior=True, searchReplace=("Left", "Right"))
        cmds.rename(mirror_name)
    cmds.select(clear=True)

def connect_body_joints():
    cmds.headsUpMessage("Connect Joints")
    #脊柱
    cmds.parent('DynamicHead','Head')
    cmds.parent('Head', 'UpperTorso')
    cmds.parent('UpperTorso', 'LowerTorso')
    cmds.parent('LowerTorso', 'Root')

    #手臂
    cmds.parent('LeftHand', 'LeftLowerArm')
    cmds.parent('LeftLowerArm', 'LeftUpperArm')
    cmds.parent('LeftUpperArm', 'UpperTorso')
    #腿
    cmds.parent('LeftFoot', 'LeftLowerLeg')
    cmds.parent('LeftLowerLeg', 'LeftUpperLeg')
    cmds.parent('LeftUpperLeg', 'LowerTorso')
    #面部
    cmds.parent('LeftCheek', 'DynamicHead')
    cmds.parent('Chin', 'DynamicHead')
    cmds.parent('TongueTip', 'TongueBase')
    cmds.parent('TongueBase', 'TongueRoot')
    cmds.parent('TongueRoot', 'Jaw')
    cmds.parent('LowerTeethRoot', 'Jaw')
    cmds.parent('Jaw', 'DynamicHead')

    cmds.parent('LeftLowerOuterMouth', 'DynamicHead')
    cmds.parent('LeftUpperOuterMouth', 'DynamicHead')
    cmds.parent('LeftLowerCornerMouth', 'DynamicHead')

    cmds.parent('LeftLowerInnerEyelid', 'LeftLowerEyelid')
    cmds.parent('LeftLowerOuterEyelid', 'LeftLowerEyelid')
    cmds.parent('LeftLowerEyelid', 'LeftEyeRoot')

    cmds.parent('LeftUpperInnerEyelid', 'LeftUpperEyelid')
    cmds.parent('LeftUpperOuterEyelid', 'LeftUpperEyelid')
    cmds.parent('LeftUpperEyelid', 'LeftEyeRoot')
    cmds.parent('LeftEyeRoot', 'DynamicHead')

    cmds.parent('LeftInnerBrow', 'DynamicHead')
    cmds.parent('LeftOuterBrow', 'DynamicHead')

    cmds.select(clear=True)

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

def create_cube_ctrl():
    # 创建立方体的顶点坐标，直接指定新的大小
    vertices = [
        (5, 5, 5),(-5, 5, 5),(-5, 5, -5),(5, 5, -5),
        (5, 5, 5),(5, -5, 5),(5, -5, -5),(5, 5, -5),
        (5, -5, -5),(-5, -5, -5),(-5, 5, -5),(-5, -5, -5),
        (-5, -5, 5),(-5, 5, 5),(-5, -5, 5),(5, -5, 5)
    ]

    # 创建NURBS曲线
    curve = cmds.curve(d=1, p=vertices, k=[i for i in range(16)], n="CubeCtrl")
def create_circle_ctrl():
    # 创建NURBS圆形并设置固定半径为10.0
    circle = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=10)
    return circle[0]
def create_arrow_control():
    # 创建箭头形状的控制曲线
    vertices = [
        (1, 0, -1),
        (-3, 0, -1),
        (-2, 0, 0),
        (-3, 0, 1),
        (1, 0, 1),
        (1, 0, 2),
        (3, 0, 0),
        (1, 0, -2),
        (1, 0, -1)
    ]

    # 创建NURBS曲线，不需要显式设置结点矢量
    curve = cmds.curve(d=1, p=vertices, n="ArrowControl")
def create_arrow():
    # 创建箭头形状的控制曲线，将点坐标等比例放大10倍
    vertices = [
        (-5, 0, 0),
        (0, 0, -5),
        (5, 0, 0),
        (3, 0, 0),
        (0, 0, -3),
        (-3, 0, 0),
        (-5, 0, 0)
    ]

    # 创建NURBS曲线
    cmds.curve(d=1, p=vertices, k=(0, 1, 2, 3, 4, 5, 6))
    cmds.rename("curve1", "Arrow")
    cmds.select(clear=True)

def create_leg_ik():
    # Create left leg IK
    left_ik_handle = cmds.ikHandle(name="LeftLeg_IK_Handle", startJoint="IK_LeftUpperLeg", endEffector="IK_LeftFoot",
                                   solver="ikRPsolver")

    right_ik_handle = cmds.ikHandle(name="RightLeg_IK_Handle", startJoint="IK_RightUpperLeg", endEffector="IK_RightFoot",
                                    solver="ikRPsolver")
def create_hand_ik():
    # Create left leg IK
    left_ik_handle = cmds.ikHandle(name="LeftHand_IK_Handle", startJoint="IK_LeftUpperArm", endEffector="IK_LeftHand",
                                   solver="ikRPsolver")

    right_ik_handle = cmds.ikHandle(name="RightHand_IK_Handle", startJoint="IK_RightUpperArm", endEffector="IK_RightHand",
                                    solver="ikRPsolver")

def gtFKconForSelectBn():
    selected_objects = cmds.ls(selection=True)
    for sel in selected_objects:
        # 获取骨骼的名称
        joint_name = sel.split("|")[-1]

        # 创建控制器
        control_name = joint_name + "Con"
        cmds.circle(ch=False, o=True, nr=(1, 0, 0), r=5, n=control_name)

        # 创建控制器组（也可以叫做ConGrpA）
        control_group_additional_name = joint_name + "_Con_Grp"
        cmds.group(n=control_group_additional_name)

        # 解除父约束
        cmds.select(sel)
        cmds.select(control_group_additional_name, add=True)
        cmds.delete(cmds.parentConstraint())

        # 控制器约束
        cmds.select(control_name)
        cmds.select(sel, add=True)
        cmds.parentConstraint()

        # 设置控制器形状属性
        shape = cmds.listRelatives(control_name, s=True)[0]
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideColor", 6)

def switchIKFKArm():
    # 获取控制系统状态
    switch_value = cmds.getAttr("IKFK_Leftt_Arm_Switch.IK_FK")

    for joint_suffix in ["UpperArm", "LowerArm", "Hand"]:
        fk_joint = "FK_Left" + joint_suffix
        ik_joint = "IK_Left" + joint_suffix

        ik_rotate = cmds.xform(ik_joint, q=True, rotation=True, worldSpace=True)
        cmds.xform(fk_joint, rotation=ik_rotate, worldSpace=True)
        # Keyframe当前帧
        cmds.setKeyframe(fk_joint, time=cmds.currentTime(query=True))


###################################   UI   #################################

cmds.window("Roblox Tool Beta v7.0 ")
cmds.columnLayout()
cmds.text(label="Base Joint")
cmds.button(label="Base Body Joints", width=400, height=30, command="create_body_joints()")
cmds.button(label="connect_Body_joints", width=400, height=30, command="connect_body_joints()")
cmds.button(label="Mirror Joints", width=400, height=30, command="mirror_left_joints()")

cmds.text(label="Add Points")
cmds.button(label="create_spheres_help", width=400, height=30, command="create_spheres_and_parent_to_bones()")
cmds.button(label="replace_objects_with_locators", width=400, height=30, command="replace_objects_with_locators()")

cmds.text(label="Add NUBS Curve Ctrl")
cmds.button(label='Cube Ctrl', width=400, height=30, command="create_cube_ctrl()")
cmds.button(label='Circle Ctrl', width=400, height=30, command="create_circle_ctrl()")
cmds.button(label='Arrow control', width=400, height=30, command="create_arrow_control()")
cmds.button(label='create_arrow', width=400, height=30, command="create_arrow()")

cmds.text(label="Add  Ctrl")
cmds.button(label='create_leg_ik', width=400, height=30, command="create_leg_ik()")
cmds.button(label='create_hand_ik', width=400, height=30, command="create_hand_ik()")

cmds.text(label="FK CON")
cmds.button(label='FK control', width=400, height=30, command="gtFKconForSelectBn()")

cmds.text(label="IK_FK Switch")
cmds.button(label='switchIKFKArm', width=400, height=30, command="switchIKFKArm()")

cmds.showWindow()
