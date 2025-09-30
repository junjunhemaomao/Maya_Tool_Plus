#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间：2019.7.20
#最近修改时间：无
#曲线操作功能集
'''
变量：
无
函数：
CvReplace 用一个曲线的形态替换其他曲线
CvNearestPoint 查找曲线最近点：：输入（物体：str|PyNode，被找到最近点曲线：str|PyNode）
CvNearestPointFast CvReplace的快捷方式：：选择物体和曲线物体在第一个
Intersection 找到曲线2到曲线1的最近cv点的最近点
AdditionalCurve 物体附加到曲线：：输入（物体，曲线，u值）
访问示例：
CvReplace(原曲线,被替换曲线列表)
'''
import pymel.core as pm
def CvReplace(curve_i,curve_o):
	curve_i = pm.general.PyNode(curve_i)
	curve_o = [pm.general.PyNode(i) for i in curve_o]
	[[pm.delete(pm.listRelatives(t,s=1)),[pm.parent(i,t,add=1,r=1,s=1) for i in pm.listRelatives(curve_i,s=1)]] for t in curve_o]
	return 0
def CvNearestPoint(obj,cv):
	obj = pm.general.PyNode(obj)
	cv = pm.general.PyNode(cv)
	cv_Shape = pm.listRelatives(cv,s=1)[0]
	cv_NP = pm.createNode('nearestPointOnCurve',n=cv+'_nearestPoint')
	cv_Shape.worldSpace.connect(cv_NP.inputCurve)
	obj_pos=pm.xform(obj,q=1,ws=1,t=1)
	cv_NP.ip.set(obj_pos)
	out = [cv_NP.p.get(),cv_NP.pr.get()]
	pm.delete (cv_NP)
	return out
def CvNearestPointFast():
	sel = pm.selected()
	if len(sel)<2:
		pm.error('应该选择两个只选择了'+str(len(sel))+'一个物体')
	sel2_Shape=pm.listRelatives(sel[1],s=1)
	if sel2_Shape==[]:
		pm.error('本应该是曲线的对象没有形态节点')
	if pm.mel.nodeType(sel2_Shape)!=u'nurbsCurve':
		pm.error('本应该是曲线的对象不是曲线')
	out = NP(sel[0],sel[1])
	pm.select(sel,r=1)
	return out
def Intersection(cv_A,cv_B):
	cv_A = pm.general.PyNode(cv_A)
	cv_B = pm.general.PyNode(cv_B)
	cv_A_Shape = pm.listRelatives(cv_A,s=1)[0]
	cv_B_Shape = pm.listRelatives(cv_B,s=1)[0]
	cv_A_NP = pm.createNode('nearestPointOnCurve',n=cv_A+'_nearestPoint')
	mag = pm.createNode('distanceBetween',n=cv_B+'_dis_mag')
	cv_A_Shape.worldSpace.connect(cv_A_NP.inputCurve)
	out = min([[[cv_A_NP.ip.set(i.getPosition('world')),mag.p1.set(i.getPosition('world')),mag.p2.set(cv_A_NP.p.get()),mag.d.get()][3],i,cv_A_NP.p.get()] for i in list(cv_B.cv)])
	pm.delete(cv_A_NP)
	pm.delete(mag)
	return out;
def AdditionalCurve(obj,Curve,U):
	CurveShape = pm.listRelatives(Curve,s=1)[0]
	Cvpath = pm.createNode('motionPath',n=obj.split('|')[-1]+'_motionPath')
	Cvpath.uValue.set(U)
	CurveShape.worldSpace.connect(Cvpath.geometryPath)
	Cvpath.allCoordinates.connect(obj.t)
	return Cvpath
