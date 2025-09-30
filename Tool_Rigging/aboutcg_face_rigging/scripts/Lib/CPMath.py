from math import *
def dis(start,End):
	outDis = 0
	for i,t in zip(start,End):
		outDis+=pow(abs(i-t),2)
	return sqrt(outDis)
def Bessel(cv_pt,curve_size):
	lamDef = lambda cv_pt,U:[[a*(1.0-U)+b*U for a,b in zip(cv_pt[i],cv_pt[i+1])] for i in range(len(cv_pt[0:-1]))]
	draw_size = len(cv_pt)-1
	
	out_list = list()
	for i in range(curve_size):
		draw_list = cv_pt
		U = i/float(curve_size-1)
		t = 0
		while t<draw_size:
			draw_list = lamDef(draw_list,U)
			t+=1
		out_list.append(draw_list[0])
	return out_list
