# -*- coding: utf-8 -*-
# 适用于游戏的面部绑定
# 整合顽皮狗技术总监Judd Simantov的方案

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
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/junjunhemaomao/Maya_Tool_Plus/main/version.txt"
GITHUB_SCRIPT_URL = "https://raw.githubusercontent.com/junjunhemaomao/Maya_Tool_Plus/main/facial_rigging.py"
GITHUB_BANNER_URL = "https://raw.githubusercontent.com/junjunhemaomao/Maya_Tool_Plus/main/GameFaceRigTool.png"
GITHUB_PAGE_URL = "https://github.com/junjunhemaomao/Maya_Tool_Plus"
TIMEOUT = 60
SSL_CTX = ssl.create_default_context()

JOINT_TAG = "_anim"
END_TAG = "_end"
CTRL_TAG = "_ctrl"
CTRL_GRP_TAG = "_grp"

_JOINT_SPECS = [
    ("root", (0, 141.3, -6.88), False),
    ("neck_a", (0, 145.8, -4.98), False),
    ("neck_b", (0, 150.225, -3.85), False),
    ("head", (0, 154.3, -3.1), False),
    ("head", (0, 172, -3), True),
    ("jaw", (0, 157.6, -1.6), False),
    ("jaw_bone_a", (0, 154, -0.6), True),
    ("jaw_bone_b", (0, 149.6, 6.2), True),
    ("brow_mid", (0, 161.7, 8), False),
    ("brow_mid_upper", (0, 163.8, 8), False),
    ("l_brow_inner", (1.85, 162.5, 8), False),
    ("l_brow_mid", (3.78, 162.6, 7.48), False),
    ("l_brow_outer", (5.5, 162, 6), False),
    ("l_brow_inner_upper", (1.92, 164.66, 7.95), False),
    ("l_brow_mid_upper", (4.17, 164.94, 6.71), False),
    ("l_brow_outer_upper", (6.24, 163.6, 4.74), False),
    ("l_brow_bone", (3.95, 163.7, 7.1), False),
    ("l_lid_above_inner", (2.54, 160.92, 6.59), False),
    ("l_lid_above_outer", (4.2, 160.89, 6.56), False),
    ("l_lid_upper_inner_pivot", (3.415, 160.213, 5.126), False),
    ("l_lid_upper_mid_pivot", (3.415, 160.213, 5.126), False),
    ("l_lid_upper_outer_pivot", (3.415, 160.213, 5.126), False),
    ("l_lid_lower_inner_pivot", (3.415, 160.213, 5.126), False),
    ("l_lid_lower_mid_pivot", (3.415, 160.213, 5.126), False),
    ("l_lid_lower_outer_pivot", (3.415, 160.213, 5.126), False),
    ("l_eyeball", (3, 160, 5), False),
    ("l_eyeball", (3, 160, 8.3), True),
    ("l_lid_upper_inner", (2.384, 160.439, 6.503), False),
    ("l_lid_upper_mid", (3.441, 160.817, 6.742), False),
    ("l_lid_upper_outer", (4.341, 160.492, 6.418), False),
    ("l_lid_inner", (1.755, 159.844, 6.278), False),
    ("l_lid_lower_inner", (2.528, 159.569, 6.468), False),
    ("l_lid_lower_mid", (3.496, 159.334, 6.567), False),
    ("l_lid_lower_outer", (4.398, 159.514, 6.233), False),
    ("l_lid_outer", (4.842, 159.945, 5.764), False),
    ("l_squint_inner", (2, 158.7, 6.5), False),
    ("l_squint_mid", (3.8, 158.2, 6.4), False),
    ("l_squint_outer", (5.4, 158.7, 5.5), False),
    ("l_cheek_upper_inner", (6, 157.75, 5.2), False),
    ("l_cheek_lower_inner", (5.7, 154.4, 4.3), False),
    ("l_cheek_upper_outer", (7.2, 157, -2.35), False),
    ("l_cheek_bone_outer", (7.3, 159.9, 2), False),
    ("l_ear", (7.3, 157.9, 0), False),
    ("l_ear", (9.5, 158, -3.83), True),
    ("nose_bridge_crease", (0, 160, 7.7), False),
    ("nose", (0, 156.6, 9.7), False),
    ("l_nasolabial_upper", (1.23, 158.6, 7), False),
    ("l_nose_crease", (1.6, 156.6, 7.8), False),
    ("l_nostril", (0.6, 156.3, 8), False),
    ("l_nasolabial_mid", (3.1, 156.6, 6.87), False),
    ("lip_above", (0, 154.8, 8.2), False),
    ("l_lip_below_nose", (1.1, 155, 7.7), False),
    ("l_lip_nasolabial_crease", (2.6, 154.7, 7), False),
    ("l_nasolabial_mouth_corner", (3.5, 153.5, 6), False),
    ("lip_below", (0, 151.6, 7), False),
    ("chin", (0, 150, 7), False),
    ("l_nasolabial_lower", (2.5, 151, 6.1), False),
    ("l_chin", (3, 150, 5), False),
    ("l_jawline", (5, 151.7, 3), False),
    ("l_jaw_clench", (6.5, 154.3, 0.3), False),
    ("lip_mid_upper", (0, 153.8, 8.3), False),
    ("l_lip_upper_inner", (1.1, 153.8, 8), False),
    ("l_lip_upper_outer", (2, 153.5, 7.3), False),
    ("lip_mid_lower", (0, 152.8, 8), False),
    ("l_lip_lower_inner", (1, 153, 7.8), False),
    ("l_lip_lower_outer", (1.6, 153, 7), False),
    ("l_lip_corner", (2.4, 153.3, 6.6), False),
    ("below_jaw", (0, 148.8, 4.4), False),
    ("l_below_jaw", (2.7, 149.4, 1.96), False),
    ("throat", (0, 146.7, 0.6), False),
    ("l_neck_muscle_upper", (5.1, 151, -2.3), False),
    ("l_neck_muscle_mid", (3.9, 147, -1.5), False),
    ("l_neck_muscle_lower", (1.6, 142, -1), False),
]

_TOOL_BASES = set()
for _base, _pos, _is_end in _JOINT_SPECS:
    _TOOL_BASES.add(_base)
    if _base.startswith("l_"):
        _TOOL_BASES.add("r_" + _base[2:])


def _exists(name):
    return bool(name) and cmds.objExists(name)


def _replace_last(text, old, new):
    parts = text.rsplit(old, 1)
    if len(parts) == 2:
        return parts[0] + new + parts[1]
    return text


def _make_joint_name(base, end=False):
    if not base:
        return base
    name = base
    if JOINT_TAG and JOINT_TAG not in name:
        name = name + JOINT_TAG
    if end and not name.endswith(END_TAG):
        name = name + END_TAG
    return name


def _resolve_joint(base, end=False):
    if not base:
        return base
    candidates = []
    for tag in (JOINT_TAG, "_anim", "_jnt", "_joint", ""):
        if tag in candidates:
            continue
        candidates.append(tag)
    for tag in candidates:
        name = base + tag if tag else base
        if end and not name.endswith(END_TAG):
            name = name + END_TAG
        if _exists(name):
            return name
    return _make_joint_name(base, end=end)


def _joint_base_from_name(name):
    if not name:
        return name
    trimmed = name
    if trimmed.endswith(END_TAG):
        trimmed = trimmed[: -len(END_TAG)]
    if JOINT_TAG and JOINT_TAG in trimmed:
        return trimmed.rsplit(JOINT_TAG, 1)[0]
    for tag in ("_anim", "_jnt", "_joint"):
        if tag in trimmed:
            return trimmed.rsplit(tag, 1)[0]
    return trimmed


def _is_tool_joint(name):
    base = _joint_base_from_name(name)
    return base in _TOOL_BASES


def _ctrl_name_from_joint(joint_name):
    if not joint_name:
        return joint_name
    if JOINT_TAG and JOINT_TAG in joint_name:
        return _replace_last(joint_name, JOINT_TAG, CTRL_TAG).replace(END_TAG, "")
    if joint_name.endswith(END_TAG):
        joint_name = joint_name[: -len(END_TAG)]
    return joint_name + CTRL_TAG


def _ctrl_grp_name_from_ctrl(ctrl_name):
    return ctrl_name + CTRL_GRP_TAG


def _safe_parent(children, parent):
    if not _exists(parent):
        return
    if isinstance(children, (list, tuple)):
        existing_children = [c for c in children if _exists(c)]
    else:
        existing_children = [children] if _exists(children) else []
    if not existing_children:
        return
    try:
        cmds.parent(existing_children, parent)
    except Exception:
        return


def _safe_point_constraint(driver, driven):
    if not (_exists(driver) and _exists(driven)):
        return None
    try:
        return cmds.pointConstraint(driver, driven)
    except Exception:
        return None


def _safe_parent_constraint(drivers, driven, mo=True):
    if not _exists(driven):
        return None
    if isinstance(drivers, (list, tuple)):
        existing_drivers = [d for d in drivers if _exists(d)]
    else:
        existing_drivers = [drivers] if _exists(drivers) else []
    if not existing_drivers:
        return None
    try:
        return cmds.parentConstraint(existing_drivers, driven, mo=mo)
    except Exception:
        return None


def _set_pivot_to_joint(group, joint):
    if not (_exists(group) and _exists(joint)):
        return
    try:
        pos = cmds.xform(joint, q=True, ws=True, t=True)
        cmds.move(pos[0], pos[1], pos[2], group + ".scalePivot", group + ".rotatePivot", absolute=True)
    except Exception:
        return

# ========================
# 面部绑定功能函数
# ========================
def create_face_joints():
    """创建面部骨骼"""
    cmds.headsUpMessage("Face Data V1.0")
    cmds.currentUnit(linear='cm')
    unit = cmds.currentUnit(q=True, linear=True)
    print('Current linear unit: {}'.format(unit))

    cmds.select(clear=True)

    for base, pos, is_end in _JOINT_SPECS:
        name = _make_joint_name(base, end=is_end)
        if _exists(name):
            continue
        try:
            cmds.joint(p=pos, n=name, relative=True)
        except Exception:
            pass
        cmds.select(clear=True)


def mirror_left_joints():
    """镜像左侧骨骼到右侧"""
    selected = cmds.ls("l_*", type="joint") or []
    for s in selected:
        if not s.startswith("l_"):
            continue
        if not _is_tool_joint(s):
            continue
        target = "r_" + s[2:]
        if _exists(target):
            continue
        try:
            cmds.mirrorJoint(s, mirrorYZ=True, mirrorBehavior=True, searchReplace=("l_", "r_"))
        except Exception:
            continue
    cmds.select(clear=True)


def connect_joints():
    """连接骨骼层级关系"""
    cmds.headsUpMessage("Parent Joints")

    _safe_parent(_resolve_joint("l_ear", end=True), _resolve_joint("l_ear"))
    _safe_parent(_resolve_joint("r_ear", end=True), _resolve_joint("r_ear"))
    _safe_parent([_resolve_joint("l_ear"), _resolve_joint("r_ear")], _resolve_joint("head"))

    _safe_parent(_resolve_joint("l_lid_upper_inner"), _resolve_joint("l_lid_upper_inner_pivot"))
    _safe_parent(_resolve_joint("l_lid_upper_mid"), _resolve_joint("l_lid_upper_mid_pivot"))
    _safe_parent(_resolve_joint("l_lid_upper_outer"), _resolve_joint("l_lid_upper_outer_pivot"))
    _safe_parent(_resolve_joint("l_lid_lower_inner"), _resolve_joint("l_lid_lower_inner_pivot"))
    _safe_parent(_resolve_joint("l_lid_lower_mid"), _resolve_joint("l_lid_lower_mid_pivot"))
    _safe_parent(_resolve_joint("l_lid_lower_outer"), _resolve_joint("l_lid_lower_outer_pivot"))
    _safe_parent(
        [
            _resolve_joint("l_lid_upper_inner_pivot"),
            _resolve_joint("l_lid_upper_mid_pivot"),
            _resolve_joint("l_lid_upper_outer_pivot"),
            _resolve_joint("l_lid_lower_inner_pivot"),
            _resolve_joint("l_lid_lower_mid_pivot"),
            _resolve_joint("l_lid_lower_outer_pivot"),
        ],
        _resolve_joint("head"),
    )

    _safe_parent(_resolve_joint("r_lid_upper_inner"), _resolve_joint("r_lid_upper_inner_pivot"))
    _safe_parent(_resolve_joint("r_lid_upper_mid"), _resolve_joint("r_lid_upper_mid_pivot"))
    _safe_parent(_resolve_joint("r_lid_upper_outer"), _resolve_joint("r_lid_upper_outer_pivot"))
    _safe_parent(_resolve_joint("r_lid_lower_inner"), _resolve_joint("r_lid_lower_inner_pivot"))
    _safe_parent(_resolve_joint("r_lid_lower_mid"), _resolve_joint("r_lid_lower_mid_pivot"))
    _safe_parent(_resolve_joint("r_lid_lower_outer"), _resolve_joint("r_lid_lower_outer_pivot"))
    _safe_parent(
        [
            _resolve_joint("r_lid_upper_inner_pivot"),
            _resolve_joint("r_lid_upper_mid_pivot"),
            _resolve_joint("r_lid_upper_outer_pivot"),
            _resolve_joint("r_lid_lower_inner_pivot"),
            _resolve_joint("r_lid_lower_mid_pivot"),
            _resolve_joint("r_lid_lower_outer_pivot"),
        ],
        _resolve_joint("head"),
    )

    _safe_parent(_resolve_joint("jaw_bone_b", end=True), _resolve_joint("jaw_bone_a", end=True))
    _safe_parent(_resolve_joint("jaw_bone_a", end=True), _resolve_joint("jaw"))
    _safe_parent(_resolve_joint("jaw"), _resolve_joint("head"))

    _safe_parent(
        [
            _resolve_joint("l_neck_muscle_upper"),
            _resolve_joint("l_below_jaw"),
            _resolve_joint("r_neck_muscle_upper"),
            _resolve_joint("r_below_jaw"),
            _resolve_joint("below_jaw"),
        ],
        _resolve_joint("neck_b"),
    )
    _safe_parent(
        [
            _resolve_joint("l_neck_muscle_mid"),
            _resolve_joint("r_neck_muscle_mid"),
            _resolve_joint("throat"),
            _resolve_joint("l_neck_muscle_lower"),
            _resolve_joint("r_neck_muscle_lower"),
        ],
        _resolve_joint("neck_a"),
    )

    _safe_parent(_resolve_joint("head", end=True), _resolve_joint("head"))
    _safe_parent(_resolve_joint("head"), _resolve_joint("neck_b"))
    _safe_parent(_resolve_joint("neck_b"), _resolve_joint("neck_a"))
    _safe_parent(_resolve_joint("neck_a"), _resolve_joint("root"))

    _safe_parent(
        [
            _resolve_joint("brow_mid"),
            _resolve_joint("brow_mid_upper"),
            _resolve_joint("l_brow_inner"),
            _resolve_joint("l_brow_mid"),
            _resolve_joint("l_brow_outer"),
            _resolve_joint("l_brow_inner_upper"),
            _resolve_joint("l_brow_mid_upper"),
            _resolve_joint("l_brow_outer_upper"),
            _resolve_joint("l_brow_bone"),
            _resolve_joint("r_brow_inner"),
            _resolve_joint("r_brow_mid"),
            _resolve_joint("r_brow_outer"),
            _resolve_joint("r_brow_inner_upper"),
            _resolve_joint("r_brow_mid_upper"),
            _resolve_joint("r_brow_outer_upper"),
            _resolve_joint("r_brow_bone"),
        ],
        _resolve_joint("head"),
    )
    _safe_parent(
        [
            _resolve_joint("l_lid_above_inner"),
            _resolve_joint("l_lid_above_outer"),
            _resolve_joint("l_nose_crease"),
            _resolve_joint("l_lip_corner"),
            _resolve_joint("l_lip_upper_outer"),
            _resolve_joint("l_squint_inner"),
            _resolve_joint("l_lip_lower_inner"),
            _resolve_joint("l_nasolabial_mid"),
            _resolve_joint("lip_below"),
            _resolve_joint("l_squint_mid"),
            _resolve_joint("l_cheek_bone_outer"),
            _resolve_joint("l_lip_upper_inner"),
            _resolve_joint("l_cheek_lower_inner"),
            _resolve_joint("l_lip_below_nose"),
            _resolve_joint("l_lip_nasolabial_crease"),
            _resolve_joint("l_jaw_clench"),
            _resolve_joint("l_lid_inner"),
            _resolve_joint("chin"),
            _resolve_joint("l_lid_outer"),
            _resolve_joint("l_cheek_upper_inner"),
            _resolve_joint("l_cheek_upper_outer"),
            _resolve_joint("l_jawline"),
            _resolve_joint("l_nostril"),
            _resolve_joint("l_nasolabial_mouth_corner"),
            _resolve_joint("l_lip_lower_outer"),
            _resolve_joint("l_nasolabial_lower"),
            _resolve_joint("l_nasolabial_upper"),
            _resolve_joint("l_squint_outer"),
            _resolve_joint("l_chin"),
        ],
        _resolve_joint("head"),
    )
    _safe_parent(
        [
            _resolve_joint("r_lid_above_inner"),
            _resolve_joint("r_lid_above_outer"),
            _resolve_joint("r_nose_crease"),
            _resolve_joint("r_lip_corner"),
            _resolve_joint("r_lip_upper_outer"),
            _resolve_joint("r_squint_inner"),
            _resolve_joint("r_lip_lower_inner"),
            _resolve_joint("r_nasolabial_mid"),
            _resolve_joint("r_squint_mid"),
            _resolve_joint("r_cheek_bone_outer"),
            _resolve_joint("r_lip_upper_inner"),
            _resolve_joint("r_cheek_lower_inner"),
            _resolve_joint("r_lip_below_nose"),
            _resolve_joint("r_lip_nasolabial_crease"),
            _resolve_joint("r_jaw_clench"),
            _resolve_joint("r_lid_inner"),
            _resolve_joint("r_lid_outer"),
            _resolve_joint("r_cheek_upper_inner"),
            _resolve_joint("r_cheek_upper_outer"),
            _resolve_joint("r_jawline"),
            _resolve_joint("r_nostril"),
            _resolve_joint("r_nasolabial_mouth_corner"),
            _resolve_joint("r_lip_lower_outer"),
            _resolve_joint("r_nasolabial_lower"),
            _resolve_joint("r_nasolabial_upper"),
            _resolve_joint("r_squint_outer"),
            _resolve_joint("lip_above"),
            _resolve_joint("lip_mid_lower"),
            _resolve_joint("nose_bridge_crease"),
            _resolve_joint("lip_mid_upper"),
            _resolve_joint("nose"),
            _resolve_joint("r_chin"),
        ],
        _resolve_joint("head"),
    )

    _safe_parent(_resolve_joint("l_eyeball", end=True), _resolve_joint("l_eyeball"))
    _safe_parent(_resolve_joint("r_eyeball", end=True), _resolve_joint("r_eyeball"))
    cmds.select(clear=True)


def create_ctrl_from_anim():
    """从骨骼创建控制器"""
    cmds.headsUpMessage("Tip: head joint drawStyle is None")
    head_joint = _resolve_joint("head")
    if _exists(head_joint):
        try:
            cmds.setAttr(head_joint + ".drawStyle", 2)
        except Exception:
            pass

    excluded_bases = {
        "root",
        "neck_a",
        "neck_b",
        "head",
        "jaw_bone_a",
        "jaw_bone_b",
        "l_ear",
        "r_ear",
        "l_eyeball",
        "r_eyeball",
        "l_lid_upper_inner",
        "l_lid_upper_mid",
        "l_lid_upper_outer",
        "l_lid_lower_inner",
        "l_lid_lower_mid",
        "l_lid_lower_outer",
        "r_lid_upper_inner",
        "r_lid_upper_mid",
        "r_lid_upper_outer",
        "r_lid_lower_inner",
        "r_lid_lower_mid",
        "r_lid_lower_outer",
    }

    sl = cmds.ls(type="joint") or []
    for joint in sl:
        if not _is_tool_joint(joint):
            continue
        if joint.endswith(END_TAG):
            continue
        base = _joint_base_from_name(joint)
        if base in excluded_bases:
            continue

        ctrl = _ctrl_name_from_joint(joint)
        grp = _ctrl_grp_name_from_ctrl(ctrl)

        if _exists(ctrl) or _exists(grp):
            continue

        try:
            loc = cmds.spaceLocator(n=ctrl)[0]
            group = cmds.group(loc, n=grp)
            try:
                cmds.delete(cmds.pointConstraint(joint, group))
            except Exception:
                pass
            try:
                cmds.delete(cmds.orientConstraint(joint, group))
            except Exception:
                pass
            try:
                cmds.makeIdentity(group, a=1, t=1, r=1)
            except Exception:
                pass
            _safe_parent_constraint(loc, joint, mo=True)
            try:
                cmds.scaleConstraint(loc, joint)
            except Exception:
                pass
        except Exception:
            pass
        cmds.select(clear=True)


def set_locs_const_grp():
    """设置控制器组"""
    ctrl_grp_suffix = CTRL_TAG + CTRL_GRP_TAG
    all_ctrl_grps = cmds.ls("*" + ctrl_grp_suffix, type="transform") or []
    all_ctrl_grps = [g for g in all_ctrl_grps if g.endswith(ctrl_grp_suffix)]

    def classify(base):
        if base.startswith(("l_jaw", "r_jaw")):
            return "jaw"
        if base.startswith(("l_lip_lower", "r_lip_lower", "l_lip_corner", "r_lip_corner")):
            return "jaw"
        if base.startswith(("l_cheek_lower", "r_cheek_lower")):
            return "jaw"
        if base.startswith(("l_nasolabial_lower", "r_nasolabial_lower", "l_nasolabial_mouth_corner", "r_nasolabial_mouth_corner")):
            return "jaw"
        if base in {"chin", "lip_mid_lower", "lip_below"}:
            return "jaw"
        if base in {"l_neck_muscle_upper", "r_neck_muscle_upper", "l_below_jaw", "r_below_jaw", "below_jaw"}:
            return "under_neck"
        if base in {"l_neck_muscle_mid", "r_neck_muscle_mid"}:
            return "neck"
        if base == "throat":
            return "throat"
        if base in {"l_neck_muscle_lower", "r_neck_muscle_lower"}:
            return "lower_neck"
        return "head"

    buckets = {"head": [], "jaw": [], "under_neck": [], "neck": [], "throat": [], "lower_neck": []}
    for grp in all_ctrl_grps:
        base = grp[: -len(ctrl_grp_suffix)]
        buckets[classify(base)].append(grp)

    def ensure_group(group_name, children):
        existing_children = [c for c in children if _exists(c)]
        if not existing_children:
            return None
        if not _exists(group_name):
            try:
                cmds.group(existing_children, n=group_name)
            except Exception:
                try:
                    cmds.group(empty=True, name=group_name)
                except Exception:
                    return None
                _safe_parent(existing_children, group_name)
        else:
            _safe_parent(existing_children, group_name)
        return group_name

    head_grp = ensure_group("head_locs_const_grp", buckets["head"])
    jaw_grp = ensure_group("jaw_locs_const_grp", buckets["jaw"])
    under_neck_grp = ensure_group("under_neck_locator_const_grp", buckets["under_neck"])
    neck_grp = ensure_group("neck_locator_const_grp", buckets["neck"])
    throat_grp = ensure_group("throat_neck_const_grp", buckets["throat"])
    lower_neck_grp = ensure_group("lower_neck_locator_const_grp", buckets["lower_neck"])

    head_joint = _resolve_joint("head")
    jaw_joint = _resolve_joint("jaw")
    neck_a_joint = _resolve_joint("neck_a")
    neck_b_joint = _resolve_joint("neck_b")
    root_joint = _resolve_joint("root")

    if head_grp:
        _set_pivot_to_joint(head_grp, head_joint)
        _safe_parent_constraint(head_joint, head_grp, mo=True)

    if jaw_grp:
        _set_pivot_to_joint(jaw_grp, jaw_joint)
        _safe_parent_constraint(jaw_joint, jaw_grp, mo=True)

    if under_neck_grp:
        _set_pivot_to_joint(under_neck_grp, neck_b_joint)
        _safe_parent_constraint(neck_b_joint, under_neck_grp, mo=True)

    if neck_grp:
        _set_pivot_to_joint(neck_grp, neck_a_joint)
        _safe_parent_constraint(neck_a_joint, neck_grp, mo=True)

    if throat_grp:
        _set_pivot_to_joint(throat_grp, neck_a_joint)
        _safe_parent_constraint([neck_a_joint, neck_b_joint], throat_grp, mo=True)

    if lower_neck_grp:
        _set_pivot_to_joint(lower_neck_grp, root_joint)
        constraint = _safe_parent_constraint([root_joint, neck_a_joint], lower_neck_grp, mo=True)
        if constraint:
            try:
                targets = cmds.parentConstraint(constraint[0], q=True, tl=True) or []
                if len(targets) == 2:
                    for idx, t in enumerate(targets):
                        cmds.setAttr(constraint[0] + "." + t + "W" + str(idx), 0.5)
            except Exception:
                pass

    cmds.select(clear=True)


def create_eyeball_locator():
    """为眼球创建定位器"""
    for side in ['l', 'r']:
        name = '%s_eyeball_ctr_loc' % side
        sdk_grp = '%s_sdk_grp' % name
        aim_grp = '%s_aim_grp' % name
        const_grp = '%s_const_grp' % name
        eyeball_joint = _resolve_joint('%s_eyeball' % side)
        if not _exists(eyeball_joint):
            continue

        if _exists(name):
            loc = name
        else:
            loc = cmds.spaceLocator(name=name)[0]

        try:
            eyeball_pos = cmds.xform(eyeball_joint, query=True, translation=True, worldSpace=True)
            cmds.move(eyeball_pos[0], eyeball_pos[1], eyeball_pos[2], loc, absolute=True, worldSpace=True)
        except Exception:
            pass

        try:
            cmds.makeIdentity(loc, apply=True, translate=True, rotate=True, scale=True)
        except Exception:
            pass

        if not _exists(sdk_grp):
            try:
                cmds.group(empty=True, name=sdk_grp)
            except Exception:
                continue
        if not _exists(aim_grp):
            try:
                cmds.group(empty=True, name=aim_grp)
            except Exception:
                continue
        if not _exists(const_grp):
            try:
                cmds.group(empty=True, name=const_grp)
            except Exception:
                continue

        _safe_parent(loc, sdk_grp)
        _safe_parent(sdk_grp, aim_grp)
        _safe_parent(aim_grp, const_grp)

        try:
            cmds.xform(sdk_grp, centerPivots=True)
            cmds.xform(aim_grp, centerPivots=True)
            cmds.xform(const_grp, centerPivots=True)
        except Exception:
            pass

    # 清除选择状态
    cmds.select(clear=True)


def eyeball_constraints():
    """设置眼球约束"""
    _safe_point_constraint('l_eyeball_ctr_loc', _resolve_joint('l_eyeball'))
    _safe_point_constraint('r_eyeball_ctr_loc', _resolve_joint('r_eyeball'))
    _safe_parent(['l_eyeball_ctr_loc_const_grp', 'r_eyeball_ctr_loc_const_grp'], _resolve_joint('head'))


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

        self.input_joint_tag = QtWidgets.QLineEdit(JOINT_TAG)

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
        tag_row = QtWidgets.QHBoxLayout()
        tag_row.addWidget(QtWidgets.QLabel("Joint Tag"))
        tag_row.addWidget(self.input_joint_tag)
        joints_layout.addLayout(tag_row)
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
        self.btn_create_joints.clicked.connect(self.run_create_joints)
        self.btn_mirror_joints.clicked.connect(self.run_mirror_joints)
        self.btn_connect_joints.clicked.connect(self.run_connect_joints)

        self.btn_create_ctrls.clicked.connect(self.run_create_ctrls)
        self.btn_parent_ctrls.clicked.connect(self.run_parent_ctrls)
        self.btn_create_eyeball_loc.clicked.connect(self.run_create_eyeball_loc)
        self.btn_eyeball_constraints.clicked.connect(self.run_eyeball_constraints)

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

    def sync_settings(self):
        global JOINT_TAG
        JOINT_TAG = (self.input_joint_tag.text() or "").strip()

    def run_create_joints(self):
        self.sync_settings()
        create_face_joints()

    def run_mirror_joints(self):
        self.sync_settings()
        mirror_left_joints()

    def run_connect_joints(self):
        self.sync_settings()
        connect_joints()

    def run_create_ctrls(self):
        self.sync_settings()
        create_ctrl_from_anim()

    def run_parent_ctrls(self):
        self.sync_settings()
        set_locs_const_grp()

    def run_create_eyeball_loc(self):
        self.sync_settings()
        create_eyeball_locator()

    def run_eyeball_constraints(self):
        self.sync_settings()
        eyeball_constraints()

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
