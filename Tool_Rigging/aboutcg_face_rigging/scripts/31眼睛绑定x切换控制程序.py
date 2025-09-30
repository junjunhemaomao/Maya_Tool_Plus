import pymel.core as pm
import CPLib.CPFnGetClosestPoint as getclose

# 定位曲线
curve = pm.PyNode("curve_up_r")
# 控制曲线
con_curve_shape = pm.PyNode("con_curve_up_rShape")

# 放控制目标约束定位器的组
loc_grp = pm.PyNode("curve_aim_r_up_con_loc_grp")
# 放目标约束定位器的组
up_loc_grp = pm.PyNode("curve_aim_r_up_loc_grp")

main_con = pm.PyNode("main_r_con")
#切换控制属性
x_switch_con_attr = main_con.X_Switch_Up
#X_Switch_Up X_Switch_Lowe
maincon_multiplyDivide = pm.createNode("multiplyDivide", n = main_con.name() + "x_switch_multiplyDivide_")
x_switch_con_attr >> maincon_multiplyDivide.input1X
maincon_multiplyDivide.input2X.set(0.1)

for i,ID in zip(curve.cv, range(len(curve.cv))):
    u = getclose.getPathClosestPoint(i, con_curve_shape)
    con_aim_loc = pm.spaceLocator(n = "curve_aim_con_loc_" + str(ID))
    pm.parent(con_aim_loc, loc_grp)
    
    path_node = pm.createNode("motionPath")
    con_curve_shape.worldSpace[0] >> path_node.geometryPath
    path_node.fractionMode.set(True)
    path_node.allCoordinates >> con_aim_loc.translate
    path_node.uValue.set(u)
    
    aim_loc = pm.spaceLocator(n = "curve_aim_loc_" + str(ID))
    pm.parent(aim_loc, up_loc_grp)
    aim_loc.t.set((0, 0, 0))
    aim_loc.r.set((0, 0, 0))
    aim_loc.s.set((1, 1, 1))
    pm.aimConstraint(con_aim_loc, aim_loc, worldUpType = "objectrotation", worldUpVector= (0, 1, 0), worldUpObject = up_loc_grp)
    
    x_switch = pm.spaceLocator(n = "curve_x_switch_" + str(ID))
    pm.parent(x_switch, aim_loc)
    x_switch.t.set((0, 0, 0))
    x_switch.r.set((0, 0, 0))
    x_switch.s.set((1, 1, 1))

    
    multMatrix=pm.createNode('multMatrix',n='multMatrix_' + str(ID))
    decomposeMatrix=pm.createNode('decomposeMatrix',n='decomposeMatrix_' + str(ID))
    blendColors = pm.createNode("blendColors", n = "x_switch_blendColors_" + str(ID))
    
    multMatrix.matrixSum >> decomposeMatrix.inputMatrix
    decomposeMatrix.outputTranslate >> blendColors.color1
    maincon_multiplyDivide.outputX >> blendColors.blender
    con_aim_loc.worldMatrix[0] >> multMatrix.matrixIn[0]
    x_switch.parentInverseMatrix[0] >> multMatrix.matrixIn[1]
    
    blendColors.color2.set(blendColors.color1.get())

    blendColors.output >> x_switch.translate
    
    pm.select(cl = True)
    joint = pm.joint(n = "curve_aim_skin_joint_" + str(ID))
    pm.parent(joint, x_switch)
    pm.xform(joint, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    joint.r.set((0, 0, 0))
