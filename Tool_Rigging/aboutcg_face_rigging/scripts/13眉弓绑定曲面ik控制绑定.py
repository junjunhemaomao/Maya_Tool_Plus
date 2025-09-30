sel = pm.selected()
mode_con = pm.PyNode("curve2")
for i in sel:
    con = pm.duplicate(mode_con)[0]
    pm.select(cl = True)
    grp = pm.group(n = i.name() + "_con_grp")
    pm.parent(con, grp)
    pm.rename(con, i.name() + "_con")
    pm.xform(grp, t = pm.xform(i, q = True, t = True, ws = True), ws = True)
    pm.parent(i, con)
