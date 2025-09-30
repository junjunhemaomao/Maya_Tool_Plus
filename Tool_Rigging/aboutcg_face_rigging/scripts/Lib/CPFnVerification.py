#!/usr/bin/python
#encoding:gbk
#本模块提供了对象验证功能函数
#验证对象是否镜像mirrorIf(obj)
#测试物体是否有是否有一个属性ifAttrPresence(obj,attr)
#检查关节标签JointLabelTypIf(obj,int)
#检查其他关节标签JointLabelOtherTypIf(obj,str)
#检查所有关节标签JointLabelIf(obj,int,str)
#子对象验证器cdVerification(obj , carry_on = lambda i:True , End = lambda i:True , Type = 'joint')
	#提供两个输入验证carry_on检查是否是需要的对象如果是返回True不是返回False如果是需要的对象则继续
	#End检查是否是需要的对象如果是返回True不是返回False如果是需要的对象则退出
	#如果为找到结束物体返回False
	#提供类型标识默认'joint'
	#获得子对象列表并按照绝对路径长度从小到大排序
#子对象结束验证器cdEndVerification(obj , End = lambda i:True , Type = 'joint')
	#End检查是否是需要的对象如果是返回True不是返回False
	#如果为找到结束物体返回False
	#提供类型标识默认'joint'
	#获得子对象列表并按照绝对路径长度从小到大排序
#添加分段数控制属性addNumber_of_segments(objList=pm.selected())
#检查分段数如果没有属性返回0如果有返回属性值IfNumber_of_segments(obj)
import pymel.core as pm
import maya.cmds as cm
def mirrorIf(obj):
	for i in pm.listAttr(obj,ud=1):
		if str(i)==str('Mirror'):
			if obj.Mirror.get()==True:
				return 1
	return 0
def ifAttrPresence(obj,attr):
	for i in pm.listAttr(obj,ud=1):
		if str(i)==str(attr):
			return 1
	return 0
def JointLabelTypIf(obj,typ=0):
	return int(typ)==int(pm.getAttr(obj+'.type'))
def JointLabelOtherTypIf(obj,otherType=''):
	return str(otherType)==str(pm.getAttr(obj+'.otherType'))
def JointLabelIf(obj,typ=0,otherType=''):
	return JointLabelTypIf(obj,typ)&JointLabelOtherTypIf(obj,otherType)
def cdVerification(obj , carry_on = lambda i:True , End = lambda i:True , Type = 'joint'):
	cdList = [i for i in pm.ls(obj,dag=1,type=Type) if i!=obj]
	cdList=[(len(i.split('|')),t) for i,t in zip(cm.ls([str(i) for i in cdList],l=True),cdList)]
	cdList.sort(key=lambda i:i[0])
	
	
	objList = [obj]
	errorIF = True
	for Id,i in cdList:
		if carry_on(i):
			objList.append(i)
		elif End(i):
			objList.append(i)
			errorIF = False
			break
		else:
			continue
	if errorIF:
		return False
	return objList
def cdEndVerification(obj , End = lambda i:True , Type = 'joint'):
	#obj=sel()[0]
	#End = lambda i:verification.JointLabelIf(i,6,'Chest')
	#Type = 'joint'
	errorIF = False
	cdList = [i for i in pm.ls(obj,dag=1,type=Type) if i!=obj]
	cdList = [i for i in cdList if bool(End(i))]
	cdList=[(len(i.split('|')),t) for i,t in zip(cm.ls([str(i) for i in cdList],l=True),cdList)]
	cdList.sort(key=lambda i:i[0])
	errorIF = bool(len(cdList))
	if errorIF!=True:
		return False
	End=cdList[0][1]
	StartPath = cm.ls(str(obj),l=True)[0]
	EndPath = [i for i in cm.ls(str(End),l=True)[0].split('|') if bool(len(i))]
	StartPathLen = len([i for i in StartPath.split('|') if bool(len(i))])
	EndPathLen = len(EndPath)
	EndPath = EndPath[StartPathLen:EndPathLen]
	objList = list()
	for i in EndPath:
	 	objList.append(StartPath)
	 	StartPath = '%s|%s'%(StartPath,i)
	objList.append(StartPath)
	return pm.ls(objList)

def addNumber_of_segments(objList=pm.selected()):
	for i in objList:		
		pm.addAttr(i,ln='Number_of_segments',sn='Number_of_segments',at=int,min=0.0,dv=0.0,k=1)
def IfNumber_of_segments(obj):
	try:
		if bool(ifAttrPresence(obj,'Number_of_segments')):
			if '%s'%pm.addAttr(obj.Number_of_segments,q=1,at=1)=='%s'%'long':
				return obj.Number_of_segments.get()
			else:
				return 0
		else:
			return 0
	except:
		return 0
