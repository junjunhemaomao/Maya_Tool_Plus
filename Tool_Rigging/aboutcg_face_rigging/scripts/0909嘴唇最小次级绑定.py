import pymel.core as pm

sel = pm.selected()

con_mode = pm.PyNode("min_con_mode")

main_grp = pm.PyNode("min_con_lowe")

for ID,i in enumerate(sel):
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, main_grp.nodeName() + "_con_" + str(ID))
    pm.select(cl = True)
    grp = pm.group(n = main_grp.nodeName() + "_con_" + str(ID) + "_grp")
    pm.parent(con, grp)
    pm.delete(pm.parentConstraint(i, grp))
    pm.parent(grp, main_grp)
    
    con.t >> i.t
    con.r >> i.r
    con.s >> i.s
    con.ro >> i.ro
