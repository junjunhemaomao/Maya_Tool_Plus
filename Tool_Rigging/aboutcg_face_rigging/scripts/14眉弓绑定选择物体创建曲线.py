sel = pm.selected()
curve = pm.curve(d = 3, p = [pm.xform(i, q = True,t = True,ws = True) for i in sel])