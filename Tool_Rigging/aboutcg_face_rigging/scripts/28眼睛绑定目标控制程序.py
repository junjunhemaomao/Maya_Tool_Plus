import pymel.core as pm


import CPLib.CPFnGetClosestPoint as getclose


curve = pm.PyNode("polyToCurve2")
con_curve_shape = pm.PyNode("up_con_curveShape")

loc_grp = pm.PyNode("curve_aim_con_loc_grp")
up_loc_grp = pm.PyNode("curve_aim_loc_grp")


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
