import pymel.core as pm

main_grp = pm.PyNode("curve_r_up_con_loc_grp")
curve = pm.PyNode("con_curve_up_r")
curve_shape = curve.getShape()



for i,ID in zip(curve.cv, range(len(curve.cv))):
    loc = pm.spaceLocator(n = curve.name() + "_con_loc_" + str(ID))
    #locator3.translate con_curve_up_lShape.controlPoints[0];
    pm.parent(loc, main_grp)
    loc.r.set((0, 0, 0))
    pm.xform(loc, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    loc.t >> curve_shape.controlPoints[ID]
    