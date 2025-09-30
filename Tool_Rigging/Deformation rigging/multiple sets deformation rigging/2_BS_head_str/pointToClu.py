# -*- coding: utf-8 -*-

#####step2######
#选择样条线的前提下，执行此命令，可以在样条线的控制点上创建一个簇，并把簇打组
#移动簇的话，骨骼链条就会移动。但目前只能横向变化，纵向还不能拉伸挤压变形


import maya.cmds as cmds

born = cmds.ls(sl=True)

for i in range(len(born)):
    ctrl_name = born[i] + "_ctrl"
    sub_ctrl_name = born[i] + "_sub_ctrl"
    ctrl_offset_name = born[i] + "_ctrl_offset"

    cmds.curve(n=ctrl_name, d=1,
               p=[(-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                  (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),
                  (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                  (-0.5, 0.5, 0.5)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    cmds.rename(cmds.listRelatives(ctrl_name, c=True, type="shape"), ctrl_name + "Shape")
    cmds.group(n=ctrl_offset_name, em=True)
    cmds.delete(cmds.parentConstraint(ctrl_name, ctrl_offset_name))
    cmds.parent(ctrl_name, ctrl_offset_name)
    cmds.delete(cmds.parentConstraint(born[i], ctrl_offset_name))

    cmds.duplicate(ctrl_name, rc=True, n=sub_ctrl_name)
    cmds.rename(cmds.listRelatives(sub_ctrl_name, c=True, type="shape"), sub_ctrl_name + "Shape")
    degree = cmds.getAttr(sub_ctrl_name + ".degree")
    spans = cmds.getAttr(sub_ctrl_name + ".spans")
    max_val = degree + spans - 1
    cmds.select(sub_ctrl_name + ".cv[0:" + str(max_val) + "]", r=True, sym=True)
    cmds.scale(0.8, 0.8, 0.8, r=True, ocp=True)
    cmds.select(cl=True)
    cmds.parent(sub_ctrl_name, ctrl_name)
    cmds.addAttr(ctrl_name, ln="subCtrl", nn="Sub Ctrl", at="long", min=0, max=1, dv=0, k=True)
    cmds.connectAttr(ctrl_name + ".subCtrl", sub_ctrl_name + "Shape.v")
    cmds.setAttr(ctrl_name + ".subCtrl", k=False, cb=True)
    cmds.parentConstraint(sub_ctrl_name, born[i])
