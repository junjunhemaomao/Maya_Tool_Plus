import pymel.core as pm
from CPLib.CPDGLib.Matrix import constraint

sel = pm.selected()

con_mode = pm.PyNode("eye_con_mode")

main_grp = pm.PyNode("loc_grp")

for i in sel:
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, i.name() + "_con")
    pm.select(cl = True)
    grp = pm.group(n = i.name() + "_con_grp")
    pm.parent(con, grp)
    pm.delete(pm.parentConstraint(i, grp))
    pm.parent(grp, main_grp)
    grp.r.set((0, 0, 0))
    ma_con_cls = constraint(n = "_" + i.name())
    ma_con_cls.point(con, i)