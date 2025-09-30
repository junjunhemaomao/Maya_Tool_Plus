# -*- coding: utf-8 -*-

#整合这部分的代码功能

import maya.cmds as cmds

def renameTool(nam, typ):
    born = cmds.ls(sl=True)
    for i in range(len(born)):
        n = i+1
        if n<=9:
            cmds.rename(born[i], nam+"_0"+str(n)+"_"+typ)
        if n>9:
            cmds.rename(born[i], nam+"_"+str(n)+"_"+typ)
def renameGUI():
    mygui = "IKOnCurve"
    if cmds.window(mygui, exists=True):
        cmds.deleteUI(mygui)
    cmds.window(mygui, title="rename the objects that you selected", widthHeight=(200, 50))

    cmds.frameLayout(label="rename the objects that you selected", collapsable=1)
    cmds.text(label="Please type in object name that you want.")
    cmds.columnLayout()
    attr_name = cmds.textFieldGrp(label="object name:", text="")
    cmds.setParent("..")

    cmds.text(label="Please type in object type.")
    cmds.columnLayout()
    attr_name1 = cmds.textFieldGrp(label="object type:", text="")
    cmds.setParent("..")

    cmds.button(label="rename", bgc=[0, 0.5, 1], command=lambda *args: renameTool(cmds.textFieldGrp(attr_name, q=True, text=True), cmds.textFieldGrp(attr_name1, q=True, text=True)))
    cmds.setParent("..")

    cmds.setParent("..")
    cmds.showWindow(mygui)
    cmds.window(mygui, edit=True, width=250)

def create_cube_ctl():
    born = cmds.ls(sl=True)

    for i in range(len(born)):
        cmds.curve(n=born[i] + "_ctrl", d=1,
                   p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5),
                      (0.5, 0.5, 0.5),(0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                      (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),(-0.5, 0.5, -0.5),(-0.5, -0.5, -0.5),
                      (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5)])

        cmds.rename(cmds.listRelatives(c=True, type="shape"), born[i] + "_ctrlShape")

        offset_grp = cmds.group(em=True, n=born[i] + "_ctrl_offset")
        cmds.delete(cmds.parentConstraint(born[i] + "_ctrl", offset_grp))
        cmds.makeIdentity(offset_grp, apply=True, t=1, r=1, s=1, n=0)

        cmds.parent(born[i] + "_ctrl", offset_grp)

        cmds.delete(cmds.parentConstraint(born[i], born[i] + "_ctrl_offset"))

        sub_ctrl = cmds.duplicate(born[i] + "_ctrl", n=born[i] + "_sub_ctrl", rc=True)[0]
        cmds.rename(cmds.listRelatives(sub_ctrl, c=True, type="shape"), born[i] + "_sub_ctrlShape")

        degree = cmds.getAttr(sub_ctrl + ".degree")
        spans = cmds.getAttr(sub_ctrl + ".spans")
        max_val = degree + spans - 1

        cmds.select(sub_ctrl + ".cv[0:" + str(max_val) + "]", r=True)
        cmds.scale(0.8, 0.8, 0.8, r=True, ocp=True)
        cmds.select(cl=True)

        cmds.parent(sub_ctrl, born[i] + "_ctrl")
        cmds.addAttr(born[i] + "_ctrl", ln="subCtrl", nn="Sub Ctrl", at="long", min=0, max=1, dv=0, k=True)
        cmds.connectAttr(born[i] + "_ctrl.subCtrl", born[i] + "_sub_ctrlShape.v")
        cmds.setAttr(born[i] + "_ctrl.subCtrl", k=False, cb=True)

        cmds.parentConstraint(born[i] + "_sub_ctrl", born[i])
def create_circular_ctl():
    born = cmds.ls(sl=True)

    for i in range(len(born)):
        cmds.circle(n=born[i] + "_ctrl", c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1)

        cmds.rename(cmds.listRelatives(c=True, type="shape"), born[i] + "_ctrlShape")

        offset_grp = cmds.group(em=True, n=born[i] + "_ctrl_offset")
        cmds.delete(cmds.parentConstraint(born[i] + "_ctrl", offset_grp))
        cmds.makeIdentity(offset_grp, apply=True, t=1, r=1, s=1, n=0)

        cmds.parent(born[i] + "_ctrl", offset_grp)

        cmds.delete(cmds.parentConstraint(born[i], born[i] + "_ctrl_offset"))

        sub_ctrl = cmds.duplicate(born[i] + "_ctrl", n=born[i] + "_sub_ctrl", rc=True)[0]
        cmds.rename(cmds.listRelatives(sub_ctrl, c=True, type="shape"), born[i] + "_sub_ctrlShape")

        degree = cmds.getAttr(sub_ctrl + ".degree")
        spans = cmds.getAttr(sub_ctrl + ".spans")
        max_val = degree + spans - 1

        cmds.select(sub_ctrl + ".cv[0:" + str(max_val) + "]", r=True)
        cmds.scale(0.8, 0.8, 0.8, r=True, ocp=True)
        cmds.select(cl=True)

        cmds.parent(sub_ctrl, born[i] + "_ctrl")
        cmds.addAttr(born[i] + "_ctrl", ln="subCtrl", nn="Sub Ctrl", at="long", min=0, max=1, dv=0, k=True)
        cmds.connectAttr(born[i] + "_ctrl.subCtrl", born[i] + "_sub_ctrlShape.v")
        cmds.setAttr(born[i] + "_ctrl.subCtrl", k=False, cb=True)

        cmds.parentConstraint(born[i] + "_sub_ctrl", born[i])

def create_offset_group():
    pcon = cmds.ls(sl=True)

    for item in pcon:
        offset_grp = cmds.group(em=True, n=item + "_offset")
        cmds.delete(cmds.parentConstraint(item, offset_grp))
        cmds.parent(item, offset_grp)

#####################################################
def create_rotate_joint_chain():
    born = cmds.ls(sl=True)

    for i in range(len(born)):
        rot_geo = cmds.polyPlane(w=1, h=1, sx=1, sy=1, n=born[i] + "_rot_geo")[0]
        cmds.move(-0.5, 0, 0, rot_geo + ".scalePivot", rot_geo + ".rotatePivot", rpr=True)
        cmds.delete(cmds.parentConstraint(born[i], rot_geo))

        rot_loc = cmds.spaceLocator(n=born[i] + "_rot_loc")[0]
        cmds.delete(cmds.parentConstraint(born[i], rot_loc))

        dist = cmds.shadingNode('distanceBetween', asUtility=True, n=born[i] + "_dist")
        if i > 0:
            cmds.connectAttr(rot_loc + ".translate", dist + ".point1")
            cmds.connectAttr(prev_rot_loc + ".translate", dist + ".point2")
            cmds.connectAttr(dist + ".distance", prev_rot_geo + ".scaleX")
            cmds.connectAttr(dist + ".distance", prev_rot_geo + ".scaleY")
            cmds.connectAttr(dist + ".distance", prev_rot_geo + ".scaleZ")
            cmds.disconnectAttr(dist + ".distance", prev_rot_geo + ".scaleX")
            cmds.disconnectAttr(dist + ".distance", prev_rot_geo + ".scaleY")
            cmds.disconnectAttr(dist + ".distance", prev_rot_geo + ".scaleZ")
            cmds.select("*_rot_geo")
            cmds.makeIdentity(apply=True, t=0, r=0, s=1, n=0, pn=True)
            cmds.parent(rot_geo, prev_rot_geo)

        if i == len(born) - 1:
            cmds.setAttr(rot_geo + ".rotateX", 0)
            cmds.setAttr(rot_geo + ".rotateY", 0)
            cmds.setAttr(rot_geo + ".rotateZ", 0)

        rot_ptcon = cmds.pointConstraint(rot_geo, born[i], n=born[i] + "_rotptcon")
        cmds.connectAttr(rot_geo + ".rotate", born[i] + ".jointOrient")

        prev_rot_loc = rot_loc
        prev_rot_geo = rot_geo
def delete_rotate_joint_chain():
    cmds.delete("*_rotptcon*")
    cmds.delete("*_rot_geo*")
    cmds.delete("*_rot_loc*")
def rotateJointGUI():
    mygui = "IKOnCurve"
    if cmds.window(mygui, exists=True):
        cmds.deleteUI(mygui)
    cmds.window(mygui, title="rotate joint chain", widthHeight=(200, 50))

    cmds.frameLayout(label="Settings", collapsable=True)

    cmds.text(label="Use the skin to assist bone positioning orientation.")

    cmds.button(label="create_rotate_joint_chain", bgc=[0, 0.5, 1], command="create_rotate_joint_chain()")
    cmds.button(label="delete_rotate_joint_chain", bgc=[0, 0.5, 1], command="delete_rotate_joint_chain()")

    cmds.setParent("..")
    cmds.showWindow(mygui)
    cmds.window(mygui, edit=True, width=250)
############################################################

#恢复链接，这个还要环境验证下，函数执行结果不对
def connect_ctrls():
    sel = cmds.ls(sl=True)
    for obj in sel:
        grp_name = obj.replace("ctrl", "Lctrl")
        cmds.connectAttr(obj+".translate", grp_name+".translate")
        cmds.connectAttr(obj+".rotate", grp_name+".rotate")
#给选定的offest组批量创建一个nubrs面片
def create_planes():
    sel = cmds.ls(sl=True)
    for obj in sel:
        plane_name = obj + "_pgeo"
        cmds.nurbsPlane(n=plane_name, p=[0, 0, 0], ax=[0, 0, 1], w=0.1, lr=1, d=3, u=1, v=1, ch=1)
        cmds.delete(cmds.parentConstraint(obj, plane_name))

        # Freeze transformations
        cmds.makeIdentity(plane_name, apply=True, t=1, r=1, s=1, n=0, pn=True)


def parent_constraint_to_fol():
    # 获取选择的对象列表
    born = cmds.ls(sl=True)

    # 遍历对象列表，添加 parentConstraint 到相应 follicle
    for obj in born:
        fol = obj + "_fol"
        cmds.parentConstraint(fol, obj, mo=True)

def connect_subctrl():
    born = cmds.ls(selection=True)

    for i in range(len(born)):
        octrl = born[i].replace("_ctrl", "_sub_ctrl")
        cmds.connectAttr(born[i] + ".subCtrl", octrl + "Shape.v")


################################################################################
cmds.window("Multiple Sets Deformation Rigging v1")
cmds.rowColumnLayout(nc=1)
cmds.button(label = "Rename Tool",width = 400,height=30,command = "renameGUI()")
cmds.button(label = "create_cube_ctl",width = 400,height=30,command = "create_cube_ctl()")
cmds.button(label = "create_offset_group",width = 400,height=30,command = "create_offset_group()")
cmds.button(label = "assist Joint orientation",width = 400,height=30,command = "rotateJointGUI()")
cmds.button(label = "create_circular_ctl",width = 400,height=30,command = "create_circular_ctl()")
cmds.button(label = "connectT&RAttrs",width = 400,height=30,command = "connect_ctrls()")
cmds.text(label="           select offest grp            ")
cmds.button(label = "create Follow Geos",width = 200,height=30,command = "create_planes()")
cmds.button(label = "parent_constraint_to_fol",width = 200,height=30,command = "parent_constraint_to_fol()")
cmds.text(label="           select sub curve            ")
cmds.button(label = "connect_subctrl_to_shape",width = 200,height=30,command = "connect_subctrl()")


cmds.showWindow()