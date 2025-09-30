import pymel.core as pm
sel = pm.selected()
for i in sel:
    pm.transformLimits(i, tx = (i.tx.get(), i.tx.get() + 10), etx = (1, 0))
