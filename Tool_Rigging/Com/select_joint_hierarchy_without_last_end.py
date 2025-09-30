# -*- coding: utf-8 -*-
# 在 Maya 中选择一个或多个骨骼运行
# 作用：快速选择骨骼层级（去掉每个链条的最后一个末端骨骼）
import maya.cmds as cmds

def select_joint_hierarchy_without_last_end():
    # 获取当前选择的骨骼
    selection = cmds.ls(selection=True, type='joint')
    if not selection:
        cmds.warning("请先选择一个或多个骨骼")
        return []

    all_result_joints = []

    for root_joint in selection:
        # 获取该骨骼下的所有子骨骼，包括自身
        joints = cmds.listRelatives(root_joint, allDescendents=True, type='joint') or []
        joints.append(root_joint)
        joints = list(reversed(joints))  # 确保顺序从上到下

        # 找到末端的最后一个骨骼（叶子关节）
        leaf_joints = [j for j in joints if not cmds.listRelatives(j, children=True, type='joint')]
        if leaf_joints:
            last_leaf = leaf_joints[-1]
            joints.remove(last_leaf)

        # 添加到总结果中
        all_result_joints.extend(joints)

    # 去重（防止多个骨架交叉时重复）
    all_result_joints = list(dict.fromkeys(all_result_joints))

    # 打印结果
    print("最终骨骼列表:", all_result_joints)

    # 在 Maya 中选择这些骨骼
    cmds.select(all_result_joints)

    return all_result_joints

select_joint_hierarchy_without_last_end()
