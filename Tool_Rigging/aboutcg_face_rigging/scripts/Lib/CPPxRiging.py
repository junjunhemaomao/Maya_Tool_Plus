#!/usr/bin/python
#encoding:gbk
#本模块提供了riging的基类和一些方法以及导入了一些常用模块
'''
	以下对original类进行介绍
		original作为绑定实现的基类本身无法使用之后的类需要继承它实现功能
			在doIt中需要实现绑定的实现并输出操作字典{进行绑定的关节:(输出控制器，输出关节)}
			会在全局操作列表中减去进行绑定的关节并在全局层级字典中添加(输出控制器，输出关节)
			mirrorIf实现了镜像的判断如果不进行镜像就无需重写这个方法如果需要进行镜像则需要镜像判断是否为自己需要的关节使用属性进行判断如果是返回1
			settingIf需要实现是否是需要的设置关节的判断返回0等于不是返回1等于是返回None等于这个设置器不进行绑定
			level方法实现了层级的构建自动输入父输出控制器和父输出关节内部需要实现层级的建立
			ps:level这个方法在基类中已经实现如果不是必要无需重写
			mainAfterRunning这个会在主函数中执行功能已经实现无需重写
			addAfterRunning向mainAfterRunning添加一个执行的函数至少需要输入一个函数指针如果有必要需要可以添加预参数
			这些并不会直接执行会在mainAfterRunning中被调用
			addattr和getName需要同时实现一个实现为对象添加需要的属性一个返回你指定的名称
		original属性
			DoMoveGrp = None#不移动组
			Main = None#总组
			Con = None#给父对象的控制器
			Joint = None#给父关节的关节
			afterRunning = None#后处理属性
			globalScale = None#全局缩放
	以下对face类进行解释
		face类继承于original拥有它的所有方法和属性
		重写了level方法将父输出关节P给不移动组
        #验证对象是否镜像mirrorIf(obj)
        #批连接 BatchConnection(inobj,outobj,inattr,outattr)
        #测试物体是否有是否有一个属性ifAttrPresence(obj,attr)
        #检查关节标签JointLabelTypIf(obj,int)
        #检查其他关节标签JointLabelOtherTypIf(obj,str)
        #检查所有关节标签JointLabelIf(obj,int,str)
'''
import pymel.core as pm
from functools import partial
from Cangphantom.Lib.CPFnCreateCon import *
class original(object):
	DoMoveGrp = None#不移动组
	Main = None#总组
	Con = None#给父对象的控制器
	Joint = None#给父关节的关节
	afterRunning = list()#后处理属性
	globalScale = None#全局缩放
	def mirrorIf(self,obj):
		return 0
	def settingIf(self,obj):
		return 0
	def mainAfterRunning(self):
		[i() for i in self.afterRunning]
		return 1
	def addAfterRunning(self,Def,*List,**Dict):
		self.afterRunning.append(partial(Def,*List,**Dict))
	def doIt(self,obj):
		pass
	def level(self,fatherCon,fatherJoint):
		try:
			pm.parent(self.Con,fatherCon)
			pm.parent(self.Joint,fatherJoint)
			return 1
		except:
			return 0
	def addattr(self,sel=pm.selected()):
		pass
	def getName(self):
		return None
class face(original):
	def level(self,fatherCon,fatherJoint):
		try:
			pm.parent(self.Con,fatherCon)
			pm.parent(self.Joint,self.DoMoveGrp)
			return 1
		except:
			return 0
#验证对象是否镜像
def mirrorIf(obj):
	for i in pm.listAttr(obj,ud=1):
		if str(i)==str('Mirror'):
			if obj.Mirror.get()==True:
				return 1
	return 0
#测试物体是否有是否有一个属性
def ifAttrPresence(obj,attr):
	for i in pm.listAttr(obj,ud=1):
		if str(i)==str(attr):
			return 1
	return 0
#批连接
def BatchConnection(inobj,outobj,inattr,outattr):
	inobj = general.PyNode(inobj+'.'+inattr)
	outobj = [general.PyNode(i+'.'+outattr) for i in outobj]
	[inobj.connect(i) for i in outobj]
	return 0
#检查关节标签JointLabelTypIf(obj,int)
def JointLabelTypIf(obj,typ=0):
	return int(typ)==int(pm.getAttr(obj+'.type'))
#检查其他关节标签JointLabelOtherTypIf(obj,str)
def JointLabelOtherTypIf(obj,otherType=''):
	return str(otherType)==str(pm.getAttr(obj+'.otherType'))
#检查所有关节标签JointLabelIf(obj,int,str)
def JointLabelIf(obj,typ=0,otherType=''):
	return JointLabelTypIf(obj,typ)&JointLabelOtherTypIf(obj,otherType)
#获得所有子类
def get_offspring(cls):
	cls_list = cls.__subclasses__()
	for i in cls_list:
		[cls_list.append(t) for t in i.__subclasses__()]
	return set(cls_list)
def help():
	out = '''
	以下对original类进行介绍
		original作为绑定实现的基类本身无法使用之后的类需要继承它实现功能
			在doIt中需要实现绑定的实现并输出操作字典{进行绑定的关节:(输出控制器，输出关节)}
			会在全局操作列表中减去进行绑定的关节并在全局层级字典中添加(输出控制器，输出关节)
			mirrorIf实现了镜像的判断如果不进行镜像就无需重写这个方法如果需要进行镜像则需要镜像判断是否为自己需要的关节使用属性进行判断如果是返回1
			settingIf需要实现是否是需要的设置关节的判断返回0等于不是返回1等于是返回None等于这个设置器不进行绑定
			level方法实现了层级的构建自动输入父输出控制器和父输出关节内部需要实现层级的建立
			ps:level这个方法在基类中已经实现如果不是必要无需重写
			mainAfterRunning这个会在主函数中执行功能已经实现无需重写
			addAfterRunning向mainAfterRunning添加一个执行的函数至少需要输入一个函数指针如果有必要需要可以添加预参数
			这些并不会直接执行会在mainAfterRunning中被调用
			addattr和getName需要同时实现一个实现为对象添加需要的属性一个返回你指定的名称
		original属性
			DoMoveGrp = None#不移动组
			Main = None#总组
			Con = None#给父对象的控制器
			Joint = None#给父关节的关节
			afterRunning = None#后处理属性
			globalScale = None#全局缩放
	以下对face类进行解释
		face类继承于original拥有它的所有方法和属性
		重写了level方法将父输出关节P给不移动组
        #验证对象是否镜像mirrorIf(obj)
        #批连接 BatchConnection(inobj,outobj,inattr,outattr)
        #测试物体是否有是否有一个属性ifAttrPresence(obj,attr)
        #检查关节标签JointLabelTypIf(obj,int)
        #检查其他关节标签JointLabelOtherTypIf(obj,str)
        #检查所有关节标签JointLabelIf(obj,int,str)
	'''
	print out
