import pymel.core as pm
pos_curve = pm.PyNode("polyToCurve4")
con_curve = pm.PyNode("eyeball_con_curve_r")
mid_obj = pm.PyNode("joint2")
up_obj = pm.PyNode("eyeball_up_loc_r")


con_curve_shape = con_curve.getShape()

nearestPointOnCurve = pm.createNode("nearestPointOnCurve")
con_curve_shape.worldSpace >> nearestPointOnCurve.inputCurve

for ID,i in enumerate(pos_curve.cv):
    nearestPointOnCurve.inPosition.set(pm.xform(i, q = True, t = True, ws = True))
    u = nearestPointOnCurve.parameter.get()
    pointOnCurveInfo = pm.createNode("pointOnCurveInfo")
    
    con_curve_shape.worldSpace >> pointOnCurveInfo.inputCurve
    pointOnCurveInfo.pr.set(u)
    
    con_aim_loc = pm.spaceLocator(n = "eyeball_con_aim_loc" + str(ID))
    pm.xform(con_aim_loc, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    pointOnCurveInfo.p >> con_aim_loc.t
    
    
    aim_loc = pm.spaceLocator(n = "eyeball_aim_loc" + str(ID))
    pm.parent(aim_loc, mid_obj)
    aim_loc.t.set((0, 0, 0))
    aim_loc.r.set((0, 0, 0))
    aim_loc.s.set((1, 1, 1))
    #aimConstraint -offset 0 0 0 -weight 1 -aimVector 1 0 0 -upVector 0 1 0 -worldUpType "object" -worldUpObject eyeball_up_loc_l;
    pm.aimConstraint(con_aim_loc, aim_loc, aimVector = (1,0,0), upVector = (0,1,0), worldUpType = "object", worldUpObject = up_obj)
    
    pm.select(cl = True)
    jin = pm.joint(n = "eyeball_joint" + str(ID))
    pm.xform(jin, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    pm.delete(pm.orientConstraint(aim_loc, jin))
    pm.select(jin)
    pm.makeIdentity(apply = True, t = 0, r = 1, s = 0, n = 0, pn = 1)
    pm.parent(jin, aim_loc)
    
    
    
pm.delete(nearestPointOnCurve)