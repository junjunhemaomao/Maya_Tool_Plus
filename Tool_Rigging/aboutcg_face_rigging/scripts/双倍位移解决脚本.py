sel = pm.selected()
for i in sel:
    pm.select(cl = True)
    grp = pm.group(n = i.nodeName() + "reverse_grp")
    pm.parent(grp, i.getParent())
    grp.t.set((0,0,0))
    grp.r.set((0,0,0))
    grp.s.set((1,1,1))
    pm.parent(i, grp)
    multiplyDivide = pm.createNode("multiplyDivide", n = "multiplyDivide_" + i.nodeName())
    i.t >> multiplyDivide.i1
    multiplyDivide.i2.set((-1,-1,-1))
    multiplyDivide.o >> grp.t