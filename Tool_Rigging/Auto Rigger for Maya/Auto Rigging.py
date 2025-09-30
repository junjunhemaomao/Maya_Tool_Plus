# -*- coding: utf-8 -*-

import maya.cmds as cmds

def creatLocators():
    if cmds.objExists('Loc_Master'):
        print'Loc_Master is exists!'
    else:
        cmds.group(empty=True,name='Loc_Master')
        root = cmds.spaceLocator(name='Loc_ROOT')
        cmds.move(0, 1, 0, root)
        cmds.parent(root, 'Loc_Master')

def deleteLocators():
    nodes=cmds.ls('Loc_*')
    cmds.delete(nodes)

def creatSpine():
    for i in range(0,spineCount):
        print()


###################################   UI   #################################

cmds.window("Auto Rigging")
cmds.rowColumnLayout(nc=2)
cmds.button(label='Creat Locators', width=200,command="creatLocators()")
cmds.button(label='Delete Locators', width=200,command="deleteLocators()")

cmds.text(label='Spine Count')
spineCount=cmds.intField(minValue=1,maxValue=10,value=4)







cmds.showWindow()
