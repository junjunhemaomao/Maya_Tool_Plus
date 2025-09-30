sel = pm.selected()
con_mode = pm.PyNode("nurbsCircle1")
con_grp = pm.PyNode("m_con_grp")

for i in sel:
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, i.nodeName() + "_con")
    grp = pm.group(con, n = i.nodeName() + "_con_grp")
    pm.parent(grp, con_grp)
    pm.delete(pm.parentConstraint(i, grp))
    grp.s.set((1,1,1))
    con.t >> i.t
    con.r >> i.r
    con.s >> i.s
    con.ro >> i.ro
    con.sh >> i.sh