import pymel.core as pm


import CPLib.CPFnGetClosestPoint as getclose


curve = pm.PyNode("up_pos_curve")
con_curve_shape = pm.PyNode("up_con_curveShape")

con_loc_grp = pm.PyNode("up_con_loc_grp")


for i,ID in zip(curve.cv, range(len(curve.cv))):
    u = getclose.getPathClosestPoint(i, con_curve_shape)
    con_loc = pm.spaceLocator(n = "con_loc_" + str(ID))
    pm.parent(con_loc, con_loc_grp)
    path_node = pm.createNode("motionPath")
    con_curve_shape.worldSpace[0] >> path_node.geometryPath
    path_node.fractionMode.set(True)
    path_node.allCoordinates >> con_loc.translate
    path_node.uValue.set(u)
    
    pm.select(cl = True)
    jin = pm.joint(n = "con_joint_" + str(ID))
    pm.parent(jin, con_loc)
    pm.xform(jin , t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    
    
    