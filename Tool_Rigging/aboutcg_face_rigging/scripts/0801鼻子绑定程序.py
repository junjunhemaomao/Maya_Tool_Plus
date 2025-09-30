import pymel.core as pm
import CPLib.CPDGLib.Matrix as matrix

con_mode = pm.PyNode("nurbsCircle2")
sel = pm.selected()

for i in sel:
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, i.nodeName() + "_con")
    pm.select(con)
    grp = pm.group(n = i.nodeName() + "_con_grp")
    pm.delete(pm.parentConstraint(i, grp))
    con_c = matrix.constraint(n = i.nodeName())
    loc = pm.spaceLocator()
    con_c.complete(con, loc)
    
    loc.t >> i.t
    loc.r >> i.r
    loc.ro >> i.ro
    loc.s >> i.s
