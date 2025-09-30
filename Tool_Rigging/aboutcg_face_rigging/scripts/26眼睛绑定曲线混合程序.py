sel = pm.selected()
ptsa = [i.getPosition() for i in sel[0].cv]
ptsb = [i.getPosition() for i in sel[1].cv]
pm.curve(d = 3, p = [(a+b)*0.5 for a,b in zip(ptsa, ptsb)])