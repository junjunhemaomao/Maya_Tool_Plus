# -*- coding: utf-8 -*-
import maya.cmds as cmds

# 函数1：删除冗余关键帧
def clearRedundantKeys(objectList):
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.000001):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    for o in objectList:
        cmds.select(o, replace=True)
        wholeKeyframe = cmds.keyframe(query=True)
        keyDelete = []
        for i in wholeKeyframe:
            if i not in keyDelete:
                keyDelete.append(i)

        if len(keyDelete) > 1:
            for t in range(1, len(keyDelete)):
                oAttributes = cmds.listAttr(o, keyable=True)
                attrListInit = []
                attrListNext = []

                for a in oAttributes:
                    attrListInit.append(cmds.getAttr(o + '.' + a, time=keyDelete[t]))
                    attrListNext.append(cmds.getAttr(o + '.' + a, time=keyDelete[t - 1]))

                isValid = True
                for i in range(0, len(oAttributes)):
                    if not isclose(attrListInit[i], attrListNext[i]):
                        isValid = False

                if isValid:
                    cmds.cutKey(cl=True, time=(keyDelete[t], keyDelete[t]))

    cmds.select(objectList)

# 函数2：删除选中的关键帧
def ack_delete_key():
    connection = cmds.editor(q=True, mainListConnection='graphEditor1GraphEd')
    curve_sel = cmds.expandSelectionConnectionAsArray(connection)
    key_count = cmds.keyframe(an='keys', q=True, kc=True)

    if key_count == 0:
        cmds.timeSlider(clearKey=True)
    else:
        cmds.cutKey(animation='keys', clear=True)

# UI框架
def createUI():
    if cmds.window("keyCleanerWindow", exists=True):
        cmds.deleteUI("keyCleanerWindow")

    cmds.window("keyCleanerWindow", title="关键帧清理工具", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.button(label="删除冗余关键帧", command=lambda x: clearRedundantKeys(cmds.ls(orderedSelection=True)))
    cmds.button(label="删除选中关键帧", command=lambda x: ack_delete_key())

    cmds.showWindow("keyCleanerWindow")

# 运行UI
createUI()
