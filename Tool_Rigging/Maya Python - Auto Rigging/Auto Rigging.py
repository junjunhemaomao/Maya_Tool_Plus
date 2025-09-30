# -*- coding: utf-8 -*-
# [YouTube 地址](https://www.youtube.com/watch?v=4rcDrbgD1zI&list=PLUug4IT0YMuEQw4yTyWt6n80QMcHd71kf)
import maya.cmds as cmds
################################    fuction   ####################################

def createLocators():
    if cmds.objExists('Loc_Master'):
        print "Loc_Master already exists."
    else:
        cmds.group(empty=True, name="Loc_Master")
        root = cmds.spaceLocator(name="Loc_ROOT")
        cmds.parent(root, "Loc_Master")
        cmds.move(0,10,0,root)

    createSpine()
    createArms(-1)
    createArms(1)



def createSpine():
    for i in range(0,cmds.intField(spineCount,query=True,value=True)):
        spine=cmds.spaceLocator(name='Loc_SPINE_'+str(i))
        if i == 0:
            cmds.parent(spine, 'Loc_ROOT')
        else:
            cmds.parent(spine, "Loc_SPINE_" + str(i-1))
        cmds.move(0,11+(2.5*i),0,spine)


def createArms(side):
    if side == 1:
        if cmds.objExists('Loc_L_Arm_GRP'):
            print "Loc_L_Arm_GRP already exists!"
        else:
            cmds.group(empty=True, name="Loc_L_Arm_GRP")
    else:
        if cmds.objExists('Loc_R_Arm_GRP'):
            print "Loc_R_Arm_GRP already exists!"
        else:
            cmds.group(empty=True, name="Loc_R_Arm_GRP")





def deleteLocators():
    nodes = cmds.ls("Loc_*")
    cmds.delete(nodes)

###################################   UI   #################################

cmds.window("Auto Rigging")
cmds.rowColumnLayout(nc = 2)
cmds.button(label = "Create Locators",width = 200,height=30,command = "createLocators()")
cmds.button(label = "Delete Locators",width = 200,height=30,command = "deleteLocators()")

cmds.text("Spine Count",label="Spine Count")
spineCount = cmds.intField(minValue=1, maxValue=10, value=4)


cmds.showWindow()

