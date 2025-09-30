import pymel.core as pm
# 定位器控制曲线
con_curve = pm.PyNode("eyeball_con_curve_r")
con_curve_shape = con_curve.getShape()

for ID,i in enumerate(con_curve.cv):
    loc = pm.spaceLocator(n = "eyeball_con_loc_" + str(ID))
    pm.xform(loc, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    loc_shape =loc.getShape()
    loc_shape.worldPosition >> con_curve_shape.controlPoints[ID]
#定位器打组
for i in pm.selected():
    pm.select(cl = True)
    grp = pm.group(n = i.name() + "_grp")
    pm.delete(pm.parentConstraint(i, grp))
    pm.parent(grp, i.getParent())
    pm.parent(i, grp)
# 控制器制作
con_mode = pm.PyNode("curve5")

sel = pm.selected()
for i in sel:
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, i.nodeName() + "_con")
    pm.parent(con, w = True)
    pm.select(con, r = True)
    grp = pm.group(n = i.nodeName() + "_con_grp")
    pm.delete(pm.parentConstraint(i, grp))
    con.t >> i.t
    con.r >> i.r
    con.s >> i.s
    con.ro >> i.ro
    con.sh >> i.sh


