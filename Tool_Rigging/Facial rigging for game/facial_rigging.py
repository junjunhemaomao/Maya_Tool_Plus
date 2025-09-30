from maya import cmds, mel
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os, shutil, sys, threading, time, webbrowser, re, json, ssl, urllib.request, urllib.error
import importlib

# ========================
# 全局变量和配置
# ========================
modeling_tools_dialog = None
CURRENT_VERSION = "1.1"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/junjunhemaomao/assistant_paint_tool/main/version.txt"
GITHUB_SCRIPT_URL = "https://raw.githubusercontent.com/junjunhemaomao/assistant_paint_tool/main/Assistant_tool.py"
GITHUB_BANNER_URL = "https://raw.githubusercontent.com/junjunhemaomao/assistant_paint_tool/main/GameFaceRigTool.png"
GITHUB_PAGE_URL = "http://yunhaohuofiea.blogspot.com/2017/04/maya-mirror-driven-key-tool-guide.html"
TIMEOUT = 60
SSL_CTX = ssl.create_default_context()

# ========================
# 面部绑定功能函数
# ========================
def create_face_joints():
    """创建面部骨骼"""
    joints_face_data = {
        # 脖子
        'root_anim': (0, 141.3, -6.88), 'neck_a_anim': (0, 145.8, -4.98), 'neck_b_anim': (0, 150.225, -3.85),
        # 头
        'head_anim': (0, 154.3, -3.1), 'head_anim_end': (0, 172, -3),
        # 下巴
        'jaw_anim': (0, 157.6, -1.6), 'jaw_bone_a_anim_end': (0, 154, -0.6), 'jaw_bone_b_anim_end': (0, 149.6, 6.2),
        # 眉弓
        'brow_mid_anim': (0, 161.7, 8), 'brow_mid_upper_anim': (0, 163.8, 8),
        'l_brow_inner_anim': (1.85, 162.5, 8), 'l_brow_mid_anim': (3.78, 162.6, 7.48),
        'l_brow_outer_anim': (5.5, 162, 6),
        'l_brow_inner_upper_anim': (1.92, 164.66, 7.95), 'l_brow_mid_upper_anim': (4.17, 164.94, 6.71),
        'l_brow_outer_upper_anim': (6.24, 163.6, 4.74),
        'l_brow_bone_anim': (3.95, 163.7, 7.1),
        # 眼眶
        'l_lid_above_inner_anim': (2.54, 160.92, 6.59), 'l_lid_above_outer_anim': (4.2, 160.89, 6.56),
        # 眼睛中心骨骼
        'l_lid_upper_inner_pivot_anim': (3.415, 160.213, 5.126), 'l_lid_upper_mid_pivot_anim': (3.415, 160.213, 5.126),
        'l_lid_upper_outer_pivot_anim': (3.415, 160.213, 5.126),
        'l_lid_lower_inner_pivot_anim': (3.415, 160.213, 5.126), 'l_lid_lower_mid_pivot_anim': (3.415, 160.213, 5.126),
        'l_lid_lower_outer_pivot_anim': (3.415, 160.213, 5.126),
        # 眼睛
        'l_eyeball_anim': (3, 160, 5), 'l_eyeball_anim_end': (3, 160, 8.3),
        # 眼睛一圈
        'l_lid_upper_inner_anim': (2.384, 160.439, 6.503), 'l_lid_upper_mid_anim': (3.441, 160.817, 6.742),
        'l_lid_upper_outer_anim': (4.341, 160.492, 6.418),
        'l_lid_inner_anim': (1.755, 159.844, 6.278),
        'l_lid_lower_inner_anim': (2.528, 159.569, 6.468), 'l_lid_lower_mid_anim': (3.496, 159.334, 6.567),
        'l_lid_lower_outer_anim': (4.398, 159.514, 6.233),
        'l_lid_outer_anim': (4.842, 159.945, 5.764),
        # 脸颊，靠眼眶
        'l_squint_inner_anim': (2, 158.7, 6.5), 'l_squint_mid_anim': (3.8, 158.2, 6.4),
        'l_squint_outer_anim': (5.4, 158.7, 5.5),
        # 脸颊，侧面
        'l_cheek_upper_inner_anim': (6, 157.75, 5.2), 'l_cheek_lower_inner_anim': (5.7, 154.4, 4.3),
        'l_cheek_upper_outer_anim': (7.2, 157, -2.35), 'l_cheek_bone_outer_anim': (7.3, 159.9, 2),
        # 耳朵
        'l_ear_anim': (7.3, 157.9, 0), 'l_ear_anim_end': (9.5, 158, -3.83),
        # 鼻子
        'nose_bridge_crease_anim': (0, 160, 7.7),
        'nose_anim': (0, 156.6, 9.7),
        'l_nasolabial_upper_anim': (1.23, 158.6, 7),
        'l_nose_crease_anim': (1.6, 156.6, 7.8),
        'l_nostril_anim': (0.6, 156.3, 8),
        # 嘴周围
        'l_nasolabial_mid_anim': (3.1, 156.6, 6.87),
        'lip_above_anim': (0, 154.8, 8.2),
        'l_lip_below_nose_anim': (1.1, 155, 7.7),
        'l_lip_nasolabial_crease_anim': (2.6, 154.7, 7),
        'l_nasolabial_mouth_corner_anim': (3.5, 153.5, 6),
        'lip_below_anim': (0, 151.6, 7),
        'chin_anim': (0, 150, 7),
        'l_nasolabial_lower_anim': (2.5, 151, 6.1),
        # 下颚
        'l_chin_anim': (3, 150, 5), 'l_jawline_anim': (5, 151.7, 3), 'l_jaw_clench_anim': (6.5, 154.3, 0.3),
        # 嘴
        'lip_mid_upper_anim': (0, 153.8, 8.3), 'l_lip_upper_inner_anim': (1.1, 153.8, 8),
        'l_lip_upper_outer_anim': (2, 153.5, 7.3),
        'lip_mid_lower_anim': (0, 152.8, 8), 'l_lip_lower_inner_anim': (1, 153, 7.8),
        'l_lip_lower_outer_anim': (1.6, 153, 7),
        'l_lip_corner_anim': (2.4, 153.3, 6.6),
        # 腮帮子
        'below_jaw_anim': (0, 148.8, 4.4), 'l_below_jaw_anim': (2.7, 149.4, 1.96),
        # 喉结
        'throat_anim': (0, 146.7, 0.6),
        # 胸锁乳突肌
        'l_neck_muscle_upper_anim': (5.1, 151, -2.3), 'l_neck_muscle_mid_anim': (3.9, 147, -1.5),
        'l_neck_muscle_lower_anim': (1.6, 142, -1)
    }

    cmds.headsUpMessage("Face Data V1.0")
    # 设置单位为厘米
    cmds.currentUnit(linear='cm')
    # 确认新单位
    unit = cmds.currentUnit(q=True, linear=True)
    print('Current linear unit: {}'.format(unit))

    # 清除当前选择
    cmds.select(clear=True)

    for name, pos in joints_face_data.items():
        cmds.joint(p=pos, n=name, relative=True)
        cmds.select(clear=True)


def mirror_left_joints():
    """镜像左侧骨骼到右侧"""
    selected = cmds.ls('l_*')
    for s in selected:
        # 检查名称是否以"l_"开头
        if not s.startswith("l_"):
            continue
        # 将第一个"l_"替换为"r_"
        mirror_name = s.replace("l_", "r_", 1)
        cmds.mirrorJoint(s, mirrorYZ=True, mirrorBehavior=True, searchReplace=("l", "r"))
        cmds.rename(mirror_name)
    cmds.select(clear=True)


def connect_joints():
    """连接骨骼层级关系"""
    cmds.headsUpMessage("Parent Joints")

    cmds.parent('l_ear_anim_end', 'l_ear_anim')
    cmds.parent('r_ear_anim_end', 'r_ear_anim')
    cmds.parent('l_ear_anim', 'r_ear_anim', 'head_anim')

    cmds.parent('l_lid_upper_inner_anim', 'l_lid_upper_inner_pivot_anim')
    cmds.parent('l_lid_upper_mid_anim', 'l_lid_upper_mid_pivot_anim')
    cmds.parent('l_lid_upper_outer_anim', 'l_lid_upper_outer_pivot_anim')
    cmds.parent('l_lid_lower_inner_anim', 'l_lid_lower_inner_pivot_anim')
    cmds.parent('l_lid_lower_mid_anim', 'l_lid_lower_mid_pivot_anim')
    cmds.parent('l_lid_lower_outer_anim', 'l_lid_lower_outer_pivot_anim')
    cmds.parent('l_lid_upper_inner_pivot_anim', 'l_lid_upper_mid_pivot_anim', 'l_lid_upper_outer_pivot_anim',
                'l_lid_lower_inner_pivot_anim', 'l_lid_lower_mid_pivot_anim', 'l_lid_lower_outer_pivot_anim',
                'head_anim')

    cmds.parent('r_lid_upper_inner_anim', 'r_lid_upper_inner_pivot_anim')
    cmds.parent('r_lid_upper_mid_anim', 'r_lid_upper_mid_pivot_anim')
    cmds.parent('r_lid_upper_outer_anim', 'r_lid_upper_outer_pivot_anim')
    cmds.parent('r_lid_lower_inner_anim', 'r_lid_lower_inner_pivot_anim')
    cmds.parent('r_lid_lower_mid_anim', 'r_lid_lower_mid_pivot_anim')
    cmds.parent('r_lid_lower_outer_anim', 'r_lid_lower_outer_pivot_anim')
    cmds.parent('r_lid_upper_inner_pivot_anim', 'r_lid_upper_mid_pivot_anim', 'r_lid_upper_outer_pivot_anim',
                'r_lid_lower_inner_pivot_anim', 'r_lid_lower_mid_pivot_anim', 'r_lid_lower_outer_pivot_anim',
                'head_anim')

    cmds.parent('jaw_bone_b_anim_end', 'jaw_bone_a_anim_end')
    cmds.parent('jaw_bone_a_anim_end', 'jaw_anim')
    cmds.parent('jaw_anim', 'head_anim')

    cmds.parent('l_neck_muscle_upper_anim', 'l_below_jaw_anim', 'r_neck_muscle_upper_anim', 'r_below_jaw_anim',
                'below_jaw_anim', 'neck_b_anim')
    cmds.parent('l_neck_muscle_mid_anim', 'r_neck_muscle_mid_anim', 'throat_anim', 'l_neck_muscle_lower_anim',
                'r_neck_muscle_lower_anim', 'neck_a_anim')

    cmds.parent('head_anim_end', 'head_anim')
    cmds.parent('head_anim', 'neck_b_anim')
    cmds.parent('neck_b_anim', 'neck_a_anim')
    cmds.parent('neck_a_anim', 'root_anim')

    cmds.parent('brow_mid_anim', 'brow_mid_upper_anim', 'l_brow_inner_anim', 'l_brow_mid_anim', 'l_brow_outer_anim',
                'l_brow_inner_upper_anim', 'l_brow_mid_upper_anim', 'l_brow_outer_upper_anim', 'l_brow_bone_anim',
                'r_brow_inner_anim', 'r_brow_mid_anim', 'r_brow_outer_anim',
                'r_brow_inner_upper_anim', 'r_brow_mid_upper_anim', 'r_brow_outer_upper_anim', 'r_brow_bone_anim',
                'head_anim')
    cmds.parent('l_lid_above_inner_anim', 'l_lid_above_outer_anim', 'l_nose_crease_anim', 'l_lip_corner_anim',
                'l_lip_upper_outer_anim', 'l_squint_inner_anim',
                'l_lip_lower_inner_anim', 'l_nasolabial_mid_anim', 'lip_below_anim', 'l_squint_mid_anim',
                'l_cheek_bone_outer_anim', 'l_lip_upper_inner_anim',
                'l_cheek_lower_inner_anim', 'l_lip_below_nose_anim', 'l_lip_nasolabial_crease_anim',
                'l_jaw_clench_anim', 'l_lid_inner_anim', 'chin_anim',
                'l_lid_outer_anim', 'l_cheek_upper_inner_anim', 'l_cheek_upper_outer_anim', 'l_jawline_anim',
                'l_nostril_anim', 'l_nasolabial_mouth_corner_anim',
                'l_lip_lower_outer_anim', 'l_nasolabial_lower_anim', 'l_nasolabial_upper_anim', 'l_squint_outer_anim',
                'l_chin_anim', 'head_anim')
    cmds.parent('r_lid_above_inner_anim', 'r_lid_above_outer_anim', 'r_nose_crease_anim', 'r_lip_corner_anim',
                'r_lip_upper_outer_anim', 'r_squint_inner_anim',
                'r_lip_lower_inner_anim', 'r_nasolabial_mid_anim', 'r_squint_mid_anim', 'r_cheek_bone_outer_anim',
                'r_lip_upper_inner_anim',
                'r_cheek_lower_inner_anim', 'r_lip_below_nose_anim', 'r_lip_nasolabial_crease_anim',
                'r_jaw_clench_anim', 'r_lid_inner_anim',
                'r_lid_outer_anim', 'r_cheek_upper_inner_anim', 'r_cheek_upper_outer_anim', 'r_jawline_anim',
                'r_nostril_anim', 'r_nasolabial_mouth_corner_anim',
                'r_lip_lower_outer_anim', 'r_nasolabial_lower_anim', 'r_nasolabial_upper_anim', 'r_squint_outer_anim',
                'lip_above_anim', 'lip_mid_lower_anim',
                'nose_bridge_crease_anim', 'lip_mid_upper_anim', 'nose_anim', 'r_chin_anim', 'head_anim')

    cmds.parent('l_eyeball_anim_end', 'l_eyeball_anim')
    cmds.parent('r_eyeball_anim_end', 'r_eyeball_anim')
    cmds.select(clear=True)


def create_ctrl_from_anim():
    """从骨骼创建控制器"""
    cmds.headsUpMessage("Tip:head_anim Joint drawStyle is None")
    cmds.setAttr("head_anim.drawStyle", 2)
    sl = cmds.ls(type='joint')

    for s in sl:
        if s in ['l_lid_upper_inner_anim', 'l_lid_upper_mid_anim', 'l_lid_upper_outer_anim', 'l_lid_lower_inner_anim',
                 'l_lid_lower_mid_anim', 'l_lid_lower_outer_anim',
                 'l_ear_anim', 'l_ear_anim_end',
                 'r_lid_upper_inner_anim', 'r_lid_upper_mid_anim', 'r_lid_upper_outer_anim', 'r_lid_lower_inner_anim',
                 'r_lid_lower_mid_anim', 'r_lid_lower_outer_anim',
                 'r_ear_anim', 'r_ear_anim_end',
                 'jaw_bone_a_anim_end', 'jaw_bone_b_anim_end',
                 'root_anim', 'neck_a_anim', 'neck_b_anim', 'head_anim', 'head_anim_end',
                 'l_eyeball_anim', 'l_eyeball_anim_end', 'r_eyeball_anim', 'r_eyeball_anim_end']:
            continue  # 跳过这些骨骼

        locName = s.replace("_anim", "_ctrl")
        loc = cmds.spaceLocator(n=locName)[0]
        group = cmds.group(loc, n=loc + "_grp")
        cmds.delete(cmds.pointConstraint(s, group))
        cmds.delete(cmds.orientConstraint(s, group))
        cmds.makeIdentity(group, a=1, t=1, r=1)
        cmds.parentConstraint(loc, s, mo=1)
        cmds.scaleConstraint(loc, s)
        cmds.select(clear=True)


def set_locs_const_grp():
    """设置控制器组"""
    # 获取要打组的控制器组
    head_ctrl_grp_names = ["brow_mid_upper_ctrl_grp", "brow_mid_ctrl_grp", "nose_bridge_crease_ctrl_grp",
                           "nose_ctrl_grp", "lip_above_ctrl_grp", "lip_mid_upper_ctrl_grp", "jaw_ctrl_grp",
                           "l_lid_above_inner_ctrl_grp", "l_lid_outer_ctrl_grp", "l_lid_inner_ctrl_grp",
                           "l_brow_inner_ctrl_grp", "l_brow_inner_upper_ctrl_grp", "l_brow_bone_ctrl_grp",
                           "l_brow_outer_upper_ctrl_grp", "l_cheek_bone_outer_ctrl_grp", "l_cheek_upper_inner_ctrl_grp",
                           "l_brow_mid_upper_ctrl_grp", "l_brow_outer_ctrl_grp", "l_squint_outer_ctrl_grp",
                           "l_squint_mid_ctrl_grp", "l_squint_inner_ctrl_grp", "l_nostril_ctrl_grp",
                           "l_nose_crease_ctrl_grp", "l_lid_lower_inner_pivot_ctrl_grp", "l_lid_inner_ctrl_grp",
                           "l_lid_above_outer_ctrl_grp", "l_lid_above_inner_ctrl_grp", "l_cheek_upper_outer_ctrl_grp",
                           "l_nasolabial_upper_ctrl_grp",
                           "l_nasolabial_mid_ctrl_grp", "l_lip_upper_outer_ctrl_grp", 'l_lip_upper_inner_ctrl_grp',
                           'l_lip_nasolabial_crease_ctrl_grp', 'l_lip_below_nose_ctrl_grp',
                           'l_lid_upper_outer_pivot_ctrl_grp', 'l_lid_upper_mid_pivot_ctrl_grp',
                           'l_lid_upper_inner_pivot_ctrl_grp', 'l_lid_outer_ctrl_grp',
                           'l_lid_lower_outer_pivot_ctrl_grp', 'l_lid_lower_mid_pivot_ctrl_grp', 'l_brow_mid_ctrl_grp',
                           "r_squint_outer_ctrl_grp", "r_squint_mid_ctrl_grp", "r_squint_inner_ctrl_grp",
                           "r_nostril_ctrl_grp", "r_nose_crease_ctrl_grp", "r_lid_lower_outer_pivot_ctrl_grp",
                           "r_lid_lower_mid_pivot_ctrl_grp",
                           "r_lid_lower_inner_pivot_ctrl_grp", "r_lid_inner_ctrl_grp", "r_lid_above_outer_ctrl_grp",
                           "r_lid_above_inner_ctrl_grp",
                           "r_cheek_upper_outer_ctrl_grp", "r_nasolabial_upper_ctrl_grp", "r_nasolabial_mid_ctrl_grp",
                           "r_lip_upper_outer_ctrl_grp", "r_lip_upper_inner_ctrl_grp",
                           "r_lip_nasolabial_crease_ctrl_grp",
                           "r_lip_below_nose_ctrl_grp", "r_lid_upper_outer_pivot_ctrl_grp",
                           "r_lid_upper_mid_pivot_ctrl_grp", "r_lid_upper_inner_pivot_ctrl_grp", "r_lid_outer_ctrl_grp",
                           "r_brow_bone_ctrl_grp", "r_cheek_upper_inner_ctrl_grp", "r_cheek_bone_outer_ctrl_grp",
                           "r_brow_outer_upper_ctrl_grp", "r_brow_outer_ctrl_grp",
                           "r_brow_mid_upper_ctrl_grp", "r_brow_mid_ctrl_grp", "r_brow_inner_upper_ctrl_grp",
                           "r_brow_inner_ctrl_grp"
                           ]
    jaw_ctrl_grp_names = ["l_jawline_ctrl_grp", "l_jaw_clench_ctrl_grp", "l_chin_ctrl_grp",
                          "l_nasolabial_mouth_corner_ctrl_grp",
                          "l_nasolabial_lower_ctrl_grp", "l_lip_lower_outer_ctrl_grp", "l_lip_lower_inner_ctrl_grp",
                          "l_lip_corner_ctrl_grp", "l_cheek_lower_inner_ctrl_grp",
                          "r_jaw_clench_ctrl_grp", "r_chin_ctrl_grp", "r_nasolabial_mouth_corner_ctrl_grp",
                          "r_nasolabial_lower_ctrl_grp",
                          "r_lip_lower_outer_ctrl_grp", "r_lip_lower_inner_ctrl_grp", "r_lip_corner_ctrl_grp",
                          "r_cheek_lower_inner_ctrl_grp",
                          "r_jawline_ctrl_grp", "chin_ctrl_grp", "lip_mid_lower_ctrl_grp", "lip_below_ctrl_grp"]
    chin_ctrl_grp_names = ["l_neck_muscle_upper_ctrl_grp", "l_below_jaw_ctrl_grp", "below_jaw_ctrl_grp",
                           "r_below_jaw_ctrl_grp", "r_neck_muscle_upper_ctrl_grp"]
    neck_ctrl_grp_names = ["l_neck_muscle_mid_ctrl_grp", "r_neck_muscle_mid_ctrl_grp"]
    throat_ctrl_grp_names = ["throat_ctrl_grp"]
    neck_lower_ctrl_grp_names = ["l_neck_muscle_lower_ctrl_grp", "r_neck_muscle_lower_ctrl_grp"]

    # 创建头部组
    head_locs_const_grp = "head_locs_const_grp"
    if not cmds.objExists(head_locs_const_grp):
        head_locs_const_grp = cmds.group(head_ctrl_grp_names, n=head_locs_const_grp)
        # 获取head_anim骨骼的坐标
        head_anim = "head_anim"
        head_pos = cmds.xform(head_anim, q=True, ws=True, t=True)
        # 将head_locs_const_grp的轴心点移动到head_anim的坐标
        cmds.move(head_pos[0], head_pos[1], head_pos[2], head_locs_const_grp + ".scalePivot",
                  head_locs_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        cmds.parentConstraint(head_anim, head_locs_const_grp, mo=True)
    else:
        print("group %s already exists" % head_locs_const_grp)

    # 创建下颌组
    jaw_locs_const_grp = "jaw_locs_const_grp"
    if not cmds.objExists(jaw_locs_const_grp):
        jaw_locs_const_grp = cmds.group(jaw_ctrl_grp_names, n=jaw_locs_const_grp)
        # 获取jaw_anim骨骼的坐标
        jaw_anim = "jaw_anim"
        jaw_pos = cmds.xform(jaw_anim, q=True, ws=True, t=True)
        # 将jaw_locs_const_grp的轴心点移动到jaw_anim的坐标
        cmds.move(jaw_pos[0], jaw_pos[1], jaw_pos[2], jaw_locs_const_grp + ".scalePivot",
                  jaw_locs_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        cmds.parentConstraint(jaw_anim, jaw_locs_const_grp, mo=True)
    else:
        print("group %s already exists" % jaw_locs_const_grp)

    # 创建下巴组
    under_neck_locator_const_grp = "under_neck_locator_const_grp"
    if not cmds.objExists(under_neck_locator_const_grp):
        under_neck_locator_const_grp = cmds.group(chin_ctrl_grp_names, n=under_neck_locator_const_grp)
        # 获取neck_b_anim骨骼的坐标
        neck_b_anim = "neck_b_anim"
        neck_b_pos = cmds.xform(neck_b_anim, q=True, ws=True, t=True)
        # 将under_neck_locator_const_grp的轴心点移动到neck_b_anim的坐标
        cmds.move(neck_b_pos[0], neck_b_pos[1], neck_b_pos[2], under_neck_locator_const_grp + ".scalePivot",
                  under_neck_locator_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        cmds.parentConstraint(neck_b_anim, under_neck_locator_const_grp, mo=True)
    else:
        print("group %s already exists" % under_neck_locator_const_grp)

    # 创建颈部组
    neck_locator_const_grp = "neck_locator_const_grp"
    if not cmds.objExists(neck_locator_const_grp):
        neck_locator_const_grp = cmds.group(neck_ctrl_grp_names, n=neck_locator_const_grp)
        # 获取neck_a_anim骨骼的坐标
        neck_a_anim = "neck_a_anim"
        neck_a_pos = cmds.xform(neck_a_anim, q=True, ws=True, t=True)
        # 将neck_locator_const_grp的轴心点移动到neck_a_anim的坐标
        cmds.move(neck_a_pos[0], neck_a_pos[1], neck_a_pos[2], neck_locator_const_grp + ".scalePivot",
                  neck_locator_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        cmds.parentConstraint(neck_a_anim, neck_locator_const_grp, mo=True)
    else:
        print("group %s already exists" % neck_locator_const_grp)

    # 创建喉咙颈部组
    throat_neck_const_grp = "throat_neck_const_grp"
    if not cmds.objExists(throat_neck_const_grp):
        throat_neck_const_grp = cmds.group(throat_ctrl_grp_names, n=throat_neck_const_grp)
        # 获取neck_a_anim骨骼的坐标
        neck_a_anim = "neck_a_anim"
        neck_a_pos = cmds.xform(neck_a_anim, q=True, ws=True, t=True)
        # 将throat_neck_const_grp的轴心点移动到neck_a_anim的坐标
        cmds.move(neck_a_pos[0], neck_a_pos[1], neck_a_pos[2], throat_neck_const_grp + ".scalePivot",
                  throat_neck_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        cmds.parentConstraint(neck_a_anim, throat_neck_const_grp, mo=True)
        cmds.parentConstraint(neck_a_anim, neck_b_anim, throat_neck_const_grp, mo=True)
    else:
        print("group %s already exists" % throat_neck_const_grp)

    # 创建下颈部组
    lower_neck_locator_const_grp = "lower_neck_locator_const_grp"
    if not cmds.objExists(lower_neck_locator_const_grp):
        lower_neck_locator_const_grp = cmds.group(neck_lower_ctrl_grp_names, n=lower_neck_locator_const_grp)
        # 获取root_anim和neck_a_anim骨骼的坐标
        root_anim = "root_anim"
        neck_a_anim = "neck_a_anim"
        root_pos = cmds.xform(root_anim, q=True, ws=True, t=True)
        # 将lower_neck_locator_const_grp的轴心点移动到root_anim的坐标
        cmds.move(root_pos[0], root_pos[1], root_pos[2], lower_neck_locator_const_grp + ".scalePivot",
                  lower_neck_locator_const_grp + ".rotatePivot", absolute=True)
        # 添加父子约束
        parent_constraint = cmds.parentConstraint(root_anim, neck_a_anim, lower_neck_locator_const_grp, mo=True)
        # 设置neck_a_anim的权重值为0.5
        cmds.setAttr(parent_constraint[0] + '.' + neck_a_anim + 'W1', 0.5)
    else:
        print("group %s already exists" % lower_neck_locator_const_grp)

    cmds.select(clear=True)


def create_eyeball_locator():
    """为眼球创建定位器"""
    for side in ['l', 'r']:
        # 创建locator并命名
        name = '%s_eyeball_ctr_loc' % side
        loc = cmds.spaceLocator(name=name)[0]

        # 获取eyeball_anim的位置
        eyeball_anim = '%s_eyeball_anim' % side
        eyeball_pos = cmds.xform(eyeball_anim, query=True, translation=True, worldSpace=True)

        # 将locator移动到eyeball_pos
        cmds.move(eyeball_pos[0], eyeball_pos[1], eyeball_pos[2], loc, absolute=True, worldSpace=True)

        # 重置locator的坐标变换
        cmds.makeIdentity(loc, apply=True, translate=True, rotate=True, scale=True)

        # 创建三个组，并对locator进行分组
        sdk_grp = cmds.group(empty=True, name='%s_sdk_grp' % name)
        aim_grp = cmds.group(empty=True, name='%s_aim_grp' % name)
        const_grp = cmds.group(empty=True, name='%s_const_grp' % name)

        cmds.parent(loc, sdk_grp)
        cmds.parent(sdk_grp, aim_grp)
        cmds.parent(aim_grp, const_grp)

        # 执行center pivot操作
        cmds.xform(sdk_grp, centerPivots=True)
        cmds.xform(aim_grp, centerPivots=True)
        cmds.xform(const_grp, centerPivots=True)

    # 清除选择状态
    cmds.select(clear=True)


def eyeball_constraints():
    """设置眼球约束"""
    # 父子约束左侧眼球控制器和骨骼
    cmds.pointConstraint('l_eyeball_ctr_loc', 'l_eyeball_anim')

    # 父子约束右侧眼球控制器和骨骼
    cmds.pointConstraint('r_eyeball_ctr_loc', 'r_eyeball_anim')

    # 连接左右侧眼球控制器的 const_grp 到骨骼
    cmds.parent('l_eyeball_ctr_loc_const_grp', 'r_eyeball_ctr_loc_const_grp', 'head_anim')


def add_brow_attributes():
    """为眉弓控制器添加属性"""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['brow_inner_up_down', 'brow_mid_up_down', 'brow_outer_up_down', 'brow_squeeze_in_out']
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)


def add_Mid_brow_attributes():
    """为眉心控制器添加属性"""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['brow_up_down', 'brow_in_out']
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)


def add_eyelid_attributes():
    """为眼睑控制器添加属性"""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['upper_inner_up_down', 'upper_mid_up_down', 'upper_outer_up_down',
             'lower_inner_up_down', 'lower_mid_up_down', 'lower_outer_up_down',
             'outer_corner_up_down', 'inner_corner_up_down', 'eyeball_up_down', 'eyeball_left_right']
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)


def add_nose_attributes():
    """为鼻子控制器添加属性"""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['l_nostril_flare', 'r_nostril_flare', 'l_sneer', 'r_sneer', 'l_nostril_widen', 'r_nostril_widen',
             'l_smile_cheek_puff', 'r_smile_cheek_puff', 'l_cheek_suck_puff', 'r_cheek_suck_puff']
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)


def add_mouth_attributes():
    """为嘴部控制器添加属性"""
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['jaw_open_close', 'l_mouth_corner_narrow_wide', 'r_mouth_corner_narrow_wide', 'l_mouth_corner_up_down',
             'r_mouth_corner_up_down', 'mouth_up_down', 'mouth_left_right', 'upper_lip_roll_in_out',
             'lower_lip_roll_in_out',
             'upper_lip_up_down', 'lower_lip_up_down', 'upper_lip_in_out', 'lower_lip_in_out',
             'face_aquash_stretch'
             ]
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)


def mirror_driven_key():
    """镜像驱动关键帧"""
    print('mirror_driven_key')


# ========================
# UI相关函数
# ========================
def maya_main_window():
    """获取Maya主窗口"""
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class ClickableLabel(QtWidgets.QLabel):
    """可点击的标签"""
    clicked = QtCore.Signal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()


class FacialRiggingUI(QtWidgets.QDialog):
    """面部绑定工具UI"""

    def __init__(self, parent=maya_main_window()):
        super(FacialRiggingUI, self).__init__(parent)
        self.setWindowTitle(f"Facial Rigging Tools v{CURRENT_VERSION}")
        self.setFixedWidth(400)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """创建UI组件"""
        self.btn_style = """
            QPushButton { 
                background-color: #3498db; 
                color: white; 
                border-radius: 6px; 
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1c5980; }
        """

        self.banner_label = ClickableLabel()
        self.banner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.banner_label.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            req = urllib.request.Request(GITHUB_BANNER_URL, headers={"User-Agent": "Maya-Facial-Rigging"})
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=TIMEOUT) as resp:
                if resp.getcode() == 200:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(resp.read())
                    pixmap = pixmap.scaledToWidth(380, QtCore.Qt.SmoothTransformation)
                    self.banner_label.setPixmap(pixmap)
        except Exception as e:
            cmds.warning(f"Failed to load banner: {str(e)}")

        # 创建按钮
        self.btn_create_joints = QtWidgets.QPushButton("Create Facial Joints")
        self.btn_mirror_joints = QtWidgets.QPushButton("Mirror Joints")
        self.btn_connect_joints = QtWidgets.QPushButton("Connect Joints")
        self.btn_create_ctrls = QtWidgets.QPushButton("Create LOC on Joints")
        self.btn_parent_ctrls = QtWidgets.QPushButton("Parenting Locators")
        self.btn_create_eyeball_loc = QtWidgets.QPushButton("Create Eyeballs Locator")
        self.btn_eyeball_constraints = QtWidgets.QPushButton("Eyeballs Constraints")

        # 属性按钮
        self.btn_add_brow_attrs = QtWidgets.QPushButton("Add Brow Attributes")
        self.btn_add_mid_brow_attrs = QtWidgets.QPushButton("Add Mid Brow Attributes")
        self.btn_add_eyelid_attrs = QtWidgets.QPushButton("Add Eyelid Attributes")
        self.btn_add_nose_attrs = QtWidgets.QPushButton("Add Nose Attributes")
        self.btn_add_mouth_attrs = QtWidgets.QPushButton("Add Mouth Attributes")
        self.btn_mirror_keys = QtWidgets.QPushButton("Mirror Driven Key")

        # 更新按钮
        self.btn_check_updates = QtWidgets.QPushButton("Check for Updates")
        self.btn_update = QtWidgets.QPushButton("Update")
        self.label_footer = QtWidgets.QLabel(f"Facial Rigging Tools v{CURRENT_VERSION}")
        self.label_footer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_footer.setStyleSheet("color: gray;")

    def create_layout(self):
        """布局UI组件"""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.banner_label)

        # 骨骼部分
        joints_group = QtWidgets.QGroupBox("Joints Setup")
        joints_layout = QtWidgets.QVBoxLayout(joints_group)
        joints_layout.addWidget(self.btn_create_joints)
        joints_layout.addWidget(self.btn_mirror_joints)
        joints_layout.addWidget(self.btn_connect_joints)
        main_layout.addWidget(joints_group)

        # 控制器部分
        ctrls_group = QtWidgets.QGroupBox("Controllers")
        ctrls_layout = QtWidgets.QVBoxLayout(ctrls_group)
        ctrls_layout.addWidget(self.btn_create_ctrls)
        ctrls_layout.addWidget(self.btn_parent_ctrls)
        ctrls_layout.addWidget(self.btn_create_eyeball_loc)
        ctrls_layout.addWidget(self.btn_eyeball_constraints)
        main_layout.addWidget(ctrls_group)

        # 属性部分
        attrs_group = QtWidgets.QGroupBox("Attributes")
        attrs_layout = QtWidgets.QVBoxLayout(attrs_group)
        attrs_layout.addWidget(self.btn_add_brow_attrs)
        attrs_layout.addWidget(self.btn_add_mid_brow_attrs)
        attrs_layout.addWidget(self.btn_add_eyelid_attrs)
        attrs_layout.addWidget(self.btn_add_nose_attrs)
        attrs_layout.addWidget(self.btn_add_mouth_attrs)
        attrs_layout.addWidget(self.btn_mirror_keys)
        main_layout.addWidget(attrs_group)

        # 更新部分
        update_layout = QtWidgets.QHBoxLayout()
        update_layout.addWidget(self.btn_check_updates)
        update_layout.addWidget(self.btn_update)
        main_layout.addLayout(update_layout)
        main_layout.addWidget(self.label_footer)

    def create_connections(self):
        """连接信号和槽"""
        # 骨骼功能连接
        self.btn_create_joints.clicked.connect(create_face_joints)
        self.btn_mirror_joints.clicked.connect(mirror_left_joints)
        self.btn_connect_joints.clicked.connect(connect_joints)

        # 控制器功能连接
        self.btn_create_ctrls.clicked.connect(create_ctrl_from_anim)
        self.btn_parent_ctrls.clicked.connect(set_locs_const_grp)
        self.btn_create_eyeball_loc.clicked.connect(create_eyeball_locator)
        self.btn_eyeball_constraints.clicked.connect(eyeball_constraints)

        # 属性功能连接
        self.btn_add_brow_attrs.clicked.connect(add_brow_attributes)
        self.btn_add_mid_brow_attrs.clicked.connect(add_Mid_brow_attributes)
        self.btn_add_eyelid_attrs.clicked.connect(add_eyelid_attributes)
        self.btn_add_nose_attrs.clicked.connect(add_nose_attributes)
        self.btn_add_mouth_attrs.clicked.connect(add_mouth_attributes)
        self.btn_mirror_keys.clicked.connect(mirror_driven_key)

        # 更新功能连接
        self.btn_check_updates.clicked.connect(self.check_for_updates)
        self.btn_update.clicked.connect(self.update_tool)
        self.banner_label.clicked.connect(lambda: webbrowser.open(GITHUB_PAGE_URL))

    def check_for_updates(self):
        """检查更新"""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(GITHUB_VERSION_URL, headers={"User-Agent": "Maya-Facial-Rigging"})
            with urllib.request.urlopen(req, context=ctx, timeout=TIMEOUT) as resp:
                if resp.getcode() == 200:
                    latest_version = resp.read().decode("utf-8").strip()
                    cmds.warning(f"Current version: {CURRENT_VERSION}, Latest version: {latest_version}")

                    if latest_version != CURRENT_VERSION:
                        cmds.confirmDialog(
                            title="Update Available",
                            message=f"New version {latest_version} available!\nCurrent version: {CURRENT_VERSION}",
                            button=["OK"]
                        )
                        self.btn_update.setEnabled(True)
                        self.btn_update.setStyleSheet(self.btn_style.replace("#3498db", "#2ecc71"))
                        return True
                    else:
                        cmds.confirmDialog(
                            title="Up to Date",
                            message="You are using the latest version.",
                            button=["OK"]
                        )
            return False
        except Exception as e:
            cmds.warning(f"Check update failed: {str(e)}")
            cmds.confirmDialog(
                title="Update Check Failed",
                message=f"Failed to check for updates: {str(e)}",
                button=["OK"]
            )
            return False

    def update_tool(self):
        """更新工具"""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(GITHUB_SCRIPT_URL, headers={"User-Agent": "Maya-Facial-Rigging"})
            with urllib.request.urlopen(req, context=ctx, timeout=TIMEOUT) as resp:
                if resp.getcode() == 200:
                    script_path = os.path.abspath(__file__)
                    tmp_path = script_path + ".tmp"
                    with open(tmp_path, "wb") as f:
                        f.write(resp.read())

                    shutil.move(tmp_path, script_path)

                    cmds.confirmDialog(
                        title="Update Complete",
                        message="Tool updated successfully. Please restart Maya to apply changes.",
                        button=["OK"]
                    )
                    return True
        except Exception as e:
            cmds.warning(f"Error updating tool: {str(e)}")
            cmds.confirmDialog(
                title="Update Failed",
                message=f"Error updating tool: {str(e)}",
                button=["OK"]
            )
            return False


# ========================
# 主函数
# ========================
def showUI():
    global modeling_tools_dialog
    try:
        modeling_tools_dialog.close()
        modeling_tools_dialog.deleteLater()
    except:
        pass

    modeling_tools_dialog = FacialRiggingUI()
    modeling_tools_dialog.show()

showUI()