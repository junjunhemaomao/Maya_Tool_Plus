# -*- coding: utf-8 -*-

import maya.cmds as cmds


def jointControl():
    # Find selection.
    selObjs = cmds.ls(selection=True)

    # Execute FOR loop.
    for obj in selObjs:
        # Create locator and group it. Create nurbs curve.
        loc = cmds.spaceLocator()[0]
        grpLoc = cmds.group(empty=True)
        circleCurve = cmds.circle()[0]

        # Match transforms of group to selected joint or object.
        parentConstraint = cmds.parentConstraint(obj, grpLoc)[0]
        cmds.delete(parentConstraint)

        # Match transforms of curve to selected joint or object.
        parentConstraint = cmds.parentConstraint(obj, circleCurve)[0]
        cmds.delete(parentConstraint)

        # Parent curve to locator.
        cmds.parent(circleCurve, loc)

        # Parent joint or object to curve.
        cmds.parent(obj, circleCurve)
        cmds.makeIdentity(obj, apply=True, translate=True, rotate=True, scale=True, normal=False)

        # Rename locator, group, and curve.
        renameGrp = cmds.rename(grpLoc, obj + "_GRP")
        renameLoc = cmds.rename(loc, obj + "_LOC")
        renameCir = cmds.rename(circleCurve, obj + "_CON")

        # Delete the history of the curves.
        cmds.select(renameCir)
        cmds.DeleteHistory()


#########__________________   UI    __________________#############

cmds.window("Expressive Facial Rigging3")
cmds.columnLayout()
cmds.button(label="jointControl", width=350, height=30, command="jointControl()")
cmds.showWindow()

