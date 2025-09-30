import pymel.core as pm
sel = pm.selected()
org_obj = pm.PyNode("org_object")
con_mode = pm.PyNode("curve1")

for i in sel:
    con = pm.duplicate(con_mode)[0]
    pm.rename(con, i.name() + "_con")
    pm.select(cl = True)
    grp = pm.group(n = i.name() + "_con_grp")
    pm.parent(con, grp)
    pm.delete(pm.parentConstraint(i, grp))
    org_con = OrgCon(n = con.nodeName())
    org_con.inObject(con, org_obj)
    org_con.outObject(i)