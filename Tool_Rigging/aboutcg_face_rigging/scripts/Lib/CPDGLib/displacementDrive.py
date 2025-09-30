#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间：2019.10.15
#最近修改时间：无
import pymel.core as pm
#添加驱动属性(要添加的对象列表)
def addDriveAttr(objList):
	for i in objList:		
		pm.addAttr(i,ln='driveX',sn='driveX',at=float,dv=1.0,k=1)
		pm.addAttr(i,ln='driveY',sn='driveY',at=float,dv=1.0,k=1)
		pm.addAttr(i,ln='driveZ',sn='driveZ',at=float,dv=1.0,k=1)
		pm.setAttr(i+'.driveX',keyable=False,channelBox=True)
		pm.setAttr(i+'.driveY',keyable=False,channelBox=True)
		pm.setAttr(i+'.driveZ',keyable=False,channelBox=True)
#创建位移驱动类
'''
方法:
	__init__初始化(self，**NAME(名称默认为空))
	delete删除创建的节点(self)
	drivePlus建立驱动连接(self,Driver(驱动者),Driven(被驱动者))
'''
class create:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__driveMultiplyDivide=pm.createNode('multiplyDivide',n='driveMultiplyDivide'+N)
		
		
		pm.setAttr(self.__driveMultiplyDivide+'.caching',False)
		pm.setAttr(self.__driveMultiplyDivide+'.nodeState',0)
		pm.setAttr(self.__driveMultiplyDivide+'.frozen',False)
		pm.setAttr(self.__driveMultiplyDivide+'.operation',1)
		pm.setAttr(self.__driveMultiplyDivide+'.outputX',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.outputY',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.outputZ',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput1X',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput1Y',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput1Z',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput2X',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput2Y',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiInput2Z',0.0)
		pm.setAttr(self.__driveMultiplyDivide+'.aiOperation',0)
		
		
		
		pm.refresh()
		
	def delete(self):
		pm.delete(self.__driveMultiplyDivide)
	def drivePlus(self,Driver,Driven):
		pm.connectAttr(Driven+'.driveX',self.__driveMultiplyDivide+'.input2X',f=True)
		pm.connectAttr(Driven+'.driveY',self.__driveMultiplyDivide+'.input2Y',f=True)
		pm.connectAttr(Driven+'.driveZ',self.__driveMultiplyDivide+'.input2Z',f=True)
		pm.connectAttr(Driver+'.translateX',self.__driveMultiplyDivide+'.input1X',f=True)
		pm.connectAttr(Driver+'.translateY',self.__driveMultiplyDivide+'.input1Y',f=True)
		pm.connectAttr(Driver+'.translateZ',self.__driveMultiplyDivide+'.input1Z',f=True)
		pm.connectAttr(self.__driveMultiplyDivide+'.outputX',Driven+'.translateX',f=True)
		pm.connectAttr(self.__driveMultiplyDivide+'.outputY',Driven+'.translateY',f=True)
		pm.connectAttr(self.__driveMultiplyDivide+'.outputZ',Driven+'.translateZ',f=True)
