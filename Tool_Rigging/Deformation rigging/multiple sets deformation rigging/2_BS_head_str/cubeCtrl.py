import maya.cmds as cmds

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

create_cube_ctl()