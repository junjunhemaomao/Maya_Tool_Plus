# -*- coding: utf-8 -*-

# 重命名工具

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

renameGUI()



