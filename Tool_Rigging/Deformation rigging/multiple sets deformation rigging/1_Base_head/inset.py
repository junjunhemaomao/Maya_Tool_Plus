# -*- coding: utf-8 -*-

# 定义全局变量

attr_name = None
attr_name1 = None

def ChadJointInsert():
    global attr_name, attr_name1  # 声明为全局变量
    chlist = cmds.ls(sl=True)
    mygui = "Chad_insert_joint"
    if cmds.window(mygui, ex=True):
        cmds.deleteUI(mygui)
    cmds.window(mygui, title="insert the joints", widthHeight=(400, 200))
    cmds.frameLayout(label="get the root joint")
    cmds.columnLayout(adj=True)
    attr_name = cmds.textFieldButtonGrp(label="get the root joint", text="", buttonLabel="root joint",
                                        cw3=(100, 100, 20), ct3=("left", "both", "left"),
                                        buttonCommand="get_org()")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.frameLayout(label="get the end joint")
    cmds.columnLayout(adj=True)
    attr_name1 = cmds.textFieldButtonGrp(label="get the end joint", text="", buttonLabel="end joint",
                                         cw3=(100, 100, 20), ct3=("left", "both", "left"),
                                         buttonCommand="get_tgr()")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.frameLayout(label="insert the joints")
    joint_number = cmds.textFieldButtonGrp(label="joint account:", text="", cw3=(100, 100, 20),
                                           ct3=("left", "both", "left"), buttonLabel="insert joints",
                                           buttonCommand="insertMidJoints(cmds.textFieldButtonGrp(attr_name, q=True, text=True), \
                                                                    cmds.textFieldButtonGrp(attr_name1, q=True, text=True), \
                                                                    cmds.textFieldButtonGrp(joint_number, q=True, text=True))")
    cmds.separator(visible=False)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.showWindow(mygui)
    cmds.window(mygui, e=True, width=250)

def get_org():
    orglist = cmds.ls(sl=True)
    orgobjname = orglist[0]
    orgbuffer = orgobjname.split("|")
    org_arraysize = len(orgbuffer)
    if org_arraysize > 1:
        cmds.textFieldButtonGrp(attr_name, e=True, text=orgbuffer[1])
    else:
        cmds.textFieldButtonGrp(attr_name, e=True, text=orgbuffer[0])
def get_tgr():
    tgrlist = cmds.ls(sl=True)
    tgrobjname = tgrlist[0]
    tgrbuffer = tgrobjname.split("|")
    tgr_arraysize = len(tgrbuffer)
    if tgr_arraysize > 1:
        cmds.textFieldButtonGrp(attr_name1, e=True, text=tgrbuffer[1])
    else:
        cmds.textFieldButtonGrp(attr_name1, e=True, text=tgrbuffer[0])
def insertMidJoints(rotJnt, endJnt, JNum):
    born = cmds.ls(sl=True)
    n = int(JNum)
    max = n + 1
    for i in range(n):
        new = rotJnt.replace("joint", "")
        cmds.duplicate(rotJnt, rc=True, n=(new+str(i+1)+"_sub_joint"))
        cmds.delete(cmds.listRelatives((new+str(i+1)+"_sub_joint"), c=True))
        cmds.pointConstraint(rotJnt, endJnt, (new+str(i+1)+"_sub_joint"), n=(new+str(i+1)+"_sub_jointPcont"))
        cmds.setAttr((new+str(i+1)+"_sub_jointPcont."+rotJnt+"W0"), (max-i-1))
        cmds.setAttr((new+str(i+1)+"_sub_jointPcont."+endJnt+"W1"), (i+1))
        cmds.delete("*_sub_jointPcont")  # 删除约束节点
        if i == 0:
            cmds.parent((new+"1_sub_joint"), rotJnt)
        if i > 0:
            cmds.parent((new+str(i+1)+"_sub_joint"), (new+str(i)+"_sub_joint"))
        if i == (n-1):
            cmds.parent(endJnt, (new+str(i+1)+"_sub_joint"))

ChadJointInsert()