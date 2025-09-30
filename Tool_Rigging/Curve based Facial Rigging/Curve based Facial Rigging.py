# -*- coding: utf-8 -*-

import maya.cmds as cmds

def create_box_curve():
    box_crv = cmds.curve(d=1, p=[
        (3.537353, 2.190347, 0.5),(3.537353, 2.190347, -0.5),(4.537353, 2.190347, -0.5),(4.537353, 2.190347, 0.5),
        (3.537353, 2.190347, 0.5),(4.537353, 2.190347, 0.5),(4.537353, 1.190347, 0.5),(3.537353, 1.190347, 0.5),
        (3.537353, 2.190347, 0.5),(3.537353, 1.190347, 0.5),(3.537353, 1.190347, -0.5),(3.537353, 2.190347, -0.5),
        (3.537353, 1.190347, -0.5),(4.537353, 1.190347, -0.5),(4.537353, 2.190347, -0.5),(4.537353, 1.190347, -0.5),
        (4.537353, 1.190347, 0.5)])
    cmds.select(box_crv)
    cmds.CenterPivot()

    cmds.rename(box_crv, "boxCrv01")
#_____________________________________________________________________________________________________
'''
这个Python函数的功能是在Maya中将一个控制器的所有变换属性（translate、rotate、scale）和可见性属性与另一个选择的控制器连接起来。
在函数中，首先选择两个控制器，然后将它们的属性连接起来。在连接属性之前，函数还会向用户发出提示，以确保正确的选择顺序。
'''
def channelConnectionTool():
    selCtrls = cmds.ls(selection=True)

    cmds.headsUpMessage("First select Target, then Source")

    cmds.connectAttr(selCtrls[0] + ".translate", selCtrls[1] + ".translate")
    cmds.connectAttr(selCtrls[0] + ".rotate", selCtrls[1] + ".rotate")
    cmds.connectAttr(selCtrls[0] + ".scale", selCtrls[1] + ".scale")
    cmds.connectAttr(selCtrls[0] + ".visibility", selCtrls[1] + ".visibility")
#_____________________________________________________________________________________________________
def create_diamond_curve():
    dmdCrv = cmds.curve(d=1, p=[
        (6.817404, 1, 0), (6.817404, 0, 1), (6.817404, -1, 0), (6.817404, 0, -1),
        (6.817404, 1, 0), (5.817404, 0, 0), (6.817404, -1, 0), (7.817404, 0, 0),
        (6.817404, 1, 0), (5.817404, 0, 0), (6.817404, 0, 1), (7.817404, 0, 0),
        (6.817404, 0, -1), (5.817404, 0, 0)])
    cmds.select(dmdCrv)
    cmds.CenterPivot()
    rnmDC = cmds.rename(dmdCrv, "dmdCrv01")
#_____________________________________________________________________________________________________
'''
这个Python函数的功能是在Maya中创建一个关节曲线工具。函数使用Maya Python命令创建三个环形曲线，并将它们旋转和缩放，以使它们看起来像一个关节。
然后，它将曲线2和曲线3的形状(parent shapes)连接到曲线1，以便它们的形状成为一个单独的曲线。最后，它将曲线重命名为"jntCrv"并删除它的历史记录。
'''
def create_joint_curve_tool():
    # Create curves
    cv1 = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, ch=1)
    cv2 = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, ch=1)
    cv3 = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, ch=1)

    # Rotate curves to look like a joint
    cmds.rotate(90, 0, 0, cv2[0], r=True, os=True)
    cmds.rotate(0, 0, 90, cv3[0], r=True, os=True)

    # Freeze the rotated curves
    cmds.select(cv2[0])
    cmds.select(cv3[0], add=True)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)

    # Parent shapes of curves 2 and 3 to curve 1
    relCrv2 = cmds.listRelatives(cv2[0], shapes=True)
    relCrv3 = cmds.listRelatives(cv3[0], shapes=True)
    cmds.parent(relCrv2[0], cv1[0], r=True, s=True)
    cmds.parent(relCrv3[0], cv1[0], r=True, s=True)

    # Delete the trns node of curves 2 and 3
    cmds.select(cv2[0])
    cmds.select(cv3[0], add=True)
    cmds.delete()

    # Rename the joint curve
    rnmCrv = cmds.rename(cv1[0], "jntCrv")

    # Delete history on joint curve
    cmds.select(rnmCrv)
    cmds.delete(ch=True)

#_____________________________________________________________________________________________________
'''
这个Python函数的功能是在Maya中创建一个下唇控制器的组，并将其重命名为"grpSDK_{下唇控制器名称}jaw01"。
函数首先找到当前选中的下唇控制器的名称，然后使用空的组命令创建一个新组，并将其变换匹配到所选的控制器。
接着，函数将新组重命名为"grpSDK{下唇控制器名称}_jaw01"。
在重命名组名之前，函数使用searchReplace()命令来确保任何名称中的"_01"都被替换为"_jaw01"，以满足命名约定。
'''

def create_jaw_lower_lip_groups():
    # Find the selection
    sel = cmds.ls(selection=True)

    # Create a group with pivot centered at selected object
    jwGrp = cmds.group(empty=True)
    cmds.matchTransform(jwGrp, sel[0])

    # Rename the group
    jwGrp = cmds.rename(jwGrp, "grpSDK_" + sel[0])

    # Give the group's name a suffix of "_jaw01"
    cmds.searchReplace("_01", "_jaw01", "hierarchy", jwGrp)

    return jwGrp


#############################################    UI      ####################################################
cmds.window("Curve based Facial Rigging")
cmds.columnLayout()
cmds.button(label="Box Curve", width=350, height=30, command="create_boxCurve()")
cmds.button(label="Biamond Curve", width=350, height=30, command="create_diamond_curve()")
cmds.button(label="Channel Connection Tool", width=350, height=30, command="channelConnectionTool()")
cmds.button(label="Joint Curve", width=350, height=30, command="create_joint_curve_tool()")
cmds.button(label="lip roup Jaw", width=350, height=30, command="create_jaw_lower_lip_groups()")
cmds.showWindow()