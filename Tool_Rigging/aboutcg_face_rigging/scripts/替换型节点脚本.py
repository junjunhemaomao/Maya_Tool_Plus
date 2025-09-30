import pymel.core as pm

sel = pm.selected()

con_mode = pm.PyNode("Outer_ring_con_mode")

for i in sel:
    pm.delete(i.getShapes())
    con = pm.duplicate(con_mode)[0]
    for t in con.getShapes():
        pm.parent(t, i, r = True, s = True)
        pm.rename(t, i.nodeName() + "Shape")
    pm.delete(con)