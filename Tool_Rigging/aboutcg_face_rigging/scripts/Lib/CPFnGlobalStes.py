#!/usr/bin/python
#encoding:gbk
#本模块实现了全局数据处理集的实现init函数为初始化函数应该仅在doIt里面调用
import pymel.core as pm
def init():
	global mainSets
	global skinStes
	global deleteStes
	mainSets = None
	skinStes = None
	deleteStes = None
	
	if pm.objExists('rigingMainStes')!=True:
		mainSets = pm.sets(n='rigingMainStes',em=1)
		skinStes = pm.sets(n='rigingSkinStes',em=1)
		deleteStes = pm.sets(n='rigingDeleteStes',em=1)
		mainSets.add(skinStes)
		mainSets.add(deleteStes)
	else:
		mainSets = pm.general.PyNode('rigingMainStes')
		skinStes = None
		deleteStes = None
		for i in pm.ls(set=1):
			if str(i.split('|')[-1])==str('rigingSkinStes'):
				skinStes = i
			if str(i.split('|')[-1])==str('rigingDeleteStes'):
				deleteStes = i
		if skinStes==None:
			skinStes = pm.sets(n='rigingSkinStes',em=1)
			mainSets.add(skinStes)
		if deleteStes==None:
			deleteStes = pm.sets(n='rigingDeleteStes',em=1)
			mainSets.add(deleteStes)
		else:
			pm.delete(pm.sets(deleteStes,q=True))
			pm.delete(deleteStes)
			deleteStes = pm.sets(n='rigingDeleteStes',em=1)
			mainSets.add(deleteStes)
class sets(object):
        '''
sets类实现了对数据处理的基类
        '''
	def __init__(self):
		global mainSets
		global skinStes
		global deleteStes
		self.mainSets=mainSets
		self.skinStes=skinStes
		self.deleteStes=deleteStes
class skinSets(sets):
        '''
skinSets类实现了对蒙皮关节集的添加
add函数(self,obj)
addList函数(self,objList)
        '''
	def add(self,obj):
		obj = pm.general.PyNode(obj)
		pm.sets(self.addSkin,add=obj)
	def addList(self,objList):
		objList = [self.addSkin(pm.general.PyNode(i)) for i in objList]
class deleteSets(sets):
        '''
deleteSets类实现了对节点清理集的添加
add函数(self,obj)
addList函数(self,objList)
        '''
	def add(self,obj):
		obj = pm.general.PyNode(obj)
		pm.sets(self.deleteStes,add=obj)
	def addList(self,objList):
		objList = [self.addDelete(pm.general.PyNode(i)) for i in objList]
#sets().addDeleteList(pm.selected())