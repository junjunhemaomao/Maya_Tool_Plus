#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.8.5
#最近修改时间:
#本模块为关节操作函数集
import pymel.core as pm
import pymel
#修改关节标签
def label(objList,int):
	if int<29:
		int = int
	if int<0:
		int = 0
	if int>29:
		int = 29
	if type(objList)!=list:
		objList=[objList]
	[[i.drawLabel.set(1),pm.setAttr(i+'''.type''',int)] for i in objList if type(i) == pymel.core.nodetypes.Joint]
	return 0
#反转关节链
def JointReverse(Jin):
	dup = pm.duplicate(Jin)
	pra = pm.listRelatives(Jin,p=1)
	renList = pm.ls(Jin,dag=1)
	JinList = pm.ls(dup,dag=1)
	
	pm.parent(JinList,w=1)
	[pm.parent(JinList[i-1],JinList[i]) for i in range(1,len(JinList))[::-1]]
	[pm.rename(JinList[i],renList[i].split('|')[-1]+"Reverse") for i in range(len(renList))]
	if len(pra)==1:
		pm.parent(JinList[-1],pra[0])
	return JinList
#层级穿插：输入多个物体自动为它们和它们下方的物体进行穿插层级关系绑定
def levelInterspersed(obj):
	objlist = [pm.ls(i,dag = 1) for i in obj]
	Parent = None
	for i in range(min([len(i) for i in objlist])):
		for t in range(len(objlist)):
			if Parent != None:
				pm.parent(objlist[t][i],Parent)
			Parent = objlist[t][i]
	return 0
#两点之间创建关节Number=中间关节数Start=是否创建开始关节End=是否创建结束关节，Name=名称
def Create_joints_at_two_points(objA,objB,Number=0,Start = True,End = True,Name = 'Name'):
	size = 0
	
	posA = pm.dt.Point(pm.xform(objA,q=1,t=1,ws=1))
	posB = pm.dt.Point(pm.xform(objB,q=1,t=1,ws=1))
	
	pm.select(cl=True)
	
	outJoint = list()
	append=outJoint.append
	if Start:
		append(pm.joint(p=posA,n=Name+str(size)))
		size+=1
	Step_size=1.0/(Number+1)
	for i in range(1,Number+1):
		pos = posA*(1-(Step_size*i))+posB*(Step_size*i)
		append(pm.joint(p=pos,n=Name+str(size)))
		size+=1
	
	if End:
		append(pm.joint(p=posB,n=Name+str(size)))
		size+=1
	return outJoint
