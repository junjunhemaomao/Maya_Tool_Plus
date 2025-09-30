# coding=utf-8
#
# Soft IK like XSI for maya
#
# (c) Andrew Nicholas 2006
# www.andynicholas.com
#
# Naoki Ohta 2019
# MIT license
####################################
import sys
import pymel.core as pm
import maya.cmds as cmds


def soft_ik_maya():
    node_name = cmds.textField("SoftIK_TextField", query=True, text=True)

    sel_list = pm.ls(sl=True)

    # Exit if nothing in sellection.
    if len(sel_list) != 2:
        print u"---"
        print u"Select a ikHandle and a object that is going to point-constrain the ikHandle."
        cmds.confirmDialog(
            message=u"Select a ikHandle and a object that is going to point-constrain the ikHandle.",
            button="OK", title="conform")
        sys.exit()

    # Exit if no ik-handle in sellection.
    a_sel_0 = sel_list[0]
    a_sel_1 = sel_list[1]
    bool_sel_0 = pm.ikHandle(exists=a_sel_0)
    bool_sel_1 = pm.ikHandle(exists=a_sel_1)

    if bool_sel_0 == False and bool_sel_1 == False:
        print u"Select IK handle."
        cmds.confirmDialog(
            message=u"Select IK handle.", button="OK", title="conform")
        sys.exit()

    # Exit if ik-handle has constraint.
    if bool_sel_0 == True:
        a_ik_handle = sel_list[0]
        a_controller = sel_list[1]
    else:
        a_ik_handle = sel_list[1]
        a_controller = sel_list[0]

    pointCon = pm.pointConstraint(a_ik_handle, q=True)
    parentCon = pm.parentConstraint(a_ik_handle, q=True)

    if pointCon != None or parentCon != None:
        print u"Remove point-constraint or parent-constraint from ik-handle."
        cmds.confirmDialog(
            message=u"Remove point-constraint or parent-constraint from ik-handle.",
            button="OK", title="conform")
        sys.exit()

    # main
    joints = pm.ikHandle(a_ik_handle, q=True, jointList=True)
    a_joint1 = joints[0]  # root joint
    a_joint2 = joints[1]  # 2nd joint

    a_endEff = pm.ikHandle(a_ik_handle, q=True, endEffector=True)  # End eff

    jnt2TransXYZ = pm.xform(a_joint2, q=True, translation=True)
    effTransXYZ = pm.xform(a_endEff, q=True, translation=True)
    jntsLen = jnt2TransXYZ[0] + effTransXYZ[0]  # Joints length

    # create locaters.
    joint_top = pm.listRelatives(a_joint1, parent=True)

    if len(joint_top) == 0:
        SIK_Aim = pm.spaceLocator(name=node_name + "_SoftIK_Aim")

    else:
        SIK_Aim = pm.spaceLocator(name=node_name + "_SoftIK_Aim")
        pm.parent(SIK_Aim, joint_top[0])

    pm.pointConstraint(a_joint1, SIK_Aim, maintainOffset=False)
    pm.aimConstraint(a_controller, SIK_Aim)

    SIK_Handle = pm.spaceLocator(name=node_name + "_SoftIK_Handle")
    pm.parent(SIK_Handle, SIK_Aim)
    pm.setAttr(SIK_Handle.rotateX, 0)
    pm.setAttr(SIK_Handle.rotateY, 0)
    pm.setAttr(SIK_Handle.rotateZ, 0)
    pm.setAttr(SIK_Handle.translateY, 0)
    pm.setAttr(SIK_Handle.translateZ, 0)

    SIK_Far = pm.spaceLocator(name=node_name + "_SoftIK_Far")
    pm.parent(SIK_Far, SIK_Aim)
    pm.setAttr(SIK_Far.rotateX, 0)
    pm.setAttr(SIK_Far.rotateY, 0)
    pm.setAttr(SIK_Far.rotateZ, 0)

    pm.pointConstraint(a_controller, SIK_Far, maintainOffset=False)

    # Connect nodes backwards one by one
    n_condition_a = pm.createNode('condition', name="condition_a")
    pm.setAttr(n_condition_a.operation, 5)  # less or equal
    pm.setAttr(n_condition_a.secondTerm, 0)
    pm.connectAttr(n_condition_a.outColor.outColorR,
                   SIK_Handle.translate.translateX)

    n_diff = pm.createNode('plusMinusAverage', name="diff")
    pm.setAttr(n_diff.operation, 2)  # substact
    pm.connectAttr(n_diff.output1D, n_condition_a.firstTerm)

    pm.connectAttr(SIK_Far.translateX, n_diff.input1D[0])

    n_jntLen_m_softD = pm.createNode(
        'plusMinusAverage', name="jointsLen_minus_softD")
    pm.setAttr(n_jntLen_m_softD.operation, 2)  # substact
    pm.connectAttr(n_jntLen_m_softD.output1D, n_diff.input1D[1])

    n_jntsLen = pm.createNode('plusMinusAverage', name="jointsLen")
    pm.setAttr(n_jntsLen.operation, 1)  # add
    pm.connectAttr(n_jntsLen.output1D, n_jntLen_m_softD.input1D[0])

    pm.connectAttr(a_joint2.translateX, n_jntsLen.input1D[0])
    pm.connectAttr(a_endEff.translateX, n_jntsLen.input1D[1])

    pm.addAttr(  # create attribute on a node selected.
        a_controller,
        longName="softIK_distance",
        niceName="Soft_IK_dist",
        keyable=True,
        minValue=0.0001,
        defaultValue=0.0001,
        attributeType="float")

    pm.connectAttr(a_controller.softIK_distance, n_jntLen_m_softD.input1D[1])

    pm.connectAttr(SIK_Far.translateX, n_condition_a.colorIfTrueR)

    n_plusMinusAverage_a = pm.createNode(
        'plusMinusAverage', name="plusMinusAverage_a")
    pm.setAttr(n_plusMinusAverage_a.operation, 1)  # add
    pm.connectAttr(n_plusMinusAverage_a.output1D, n_condition_a.colorIfFalseR)

    n_multiplyDivide_a = pm.createNode(
        'multiplyDivide', name="multiplyDivide_a")
    pm.setAttr(n_multiplyDivide_a.operation, 1)  # multiply
    pm.connectAttr(n_multiplyDivide_a.outputX, n_plusMinusAverage_a.input1D[0])

    pm.connectAttr(a_controller.softIK_distance, n_multiplyDivide_a.input1X)

    n_plusMinusAverage_b = pm.createNode(
        'plusMinusAverage', name="plusMinusAverage_b")
    pm.setAttr(n_plusMinusAverage_b.operation, 2)  # substract
    pm.setAttr(n_plusMinusAverage_b.input1D[0], 1)
    pm.connectAttr(n_plusMinusAverage_b.output1D, n_multiplyDivide_a.input2X)

    n_substttExp_a = pm.createNode('multiplyDivide', name="substttExp_a")
    pm.setAttr(n_substttExp_a.operation, 3)  # pow
    pm.setAttr(n_substttExp_a.input1X, 2.71828)  # Set appro for Napier
    pm.connectAttr(n_substttExp_a.outputX, n_plusMinusAverage_b.input1D[1])

    n_multiplyDivide_b = pm.createNode(
        'multiplyDivide', name="multiplyDivide_b")
    pm.setAttr(n_multiplyDivide_b.operation, 1)  # multiply
    pm.setAttr(n_multiplyDivide_b.input2X, -1)
    pm.connectAttr(n_multiplyDivide_b.outputX, n_substttExp_a.input2X)

    n_multiplyDivide_c = pm.createNode(
        'multiplyDivide', name="multiplyDivide_c")
    pm.setAttr(n_multiplyDivide_c.operation, 2)  # divide
    pm.connectAttr(n_multiplyDivide_c.outputX, n_multiplyDivide_b.input1X)

    pm.connectAttr(n_diff.output1D, n_multiplyDivide_c.input1X)
    pm.connectAttr(a_controller.softIK_distance, n_multiplyDivide_c.input2X)

    pm.connectAttr(n_jntLen_m_softD.output1D, n_plusMinusAverage_a.input1D[1])

    # constrain
    pm.pointConstraint(SIK_Handle, a_ik_handle)

    print u"---"
    print u"Done!"
    cmds.confirmDialog(
        message=u"Done!",
        button="OK", title="conform")


"""
UI
"""


def btn_soft_ik_maya(self):  # button
    soft_ik_maya()


# If UI exists already, delete UI.
if (cmds.window("no_rig_scripts_ui", q=True, exists=True)):
    cmds.deleteUI("no_rig_scripts_ui", window=True)
# Create UI.
this_window = cmds.window(
    "no_rig_scripts_ui",  # identifier
    title=u'Script for Rigging',
    width=350,
    height=100)
#
# cmds.columnLayout()
cmds.frameLayout(label="Soft IK", collapsable=True,)
cmds.rowLayout('soft_ik_column', numberOfColumns=3, adjustableColumn=2)
cmds.text(label='String for nodes : ')
cmds.textField("SoftIK_TextField", tx="ie_Rig_Leg_Left")
cmds.button(
    label="Do it",
    width=70,
    height=40,
    align="center",
    command=btn_soft_ik_maya,
    annotation=u"Select a ikHandle and a object that is going to point-constrain the ikHandle.\
    IK-handleとIK-handleをコンストレインするオブジェクトを選択して実行して下さい。")

# Show UI.
cmds.showWindow(this_window)
