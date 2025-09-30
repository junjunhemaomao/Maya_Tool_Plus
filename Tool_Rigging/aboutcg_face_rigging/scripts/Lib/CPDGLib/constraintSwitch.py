#!/usr/bin/python
#encoding:gbk
#本模块实现了约束切换
import pymel.core as pm
class Switch:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__SwitchMultiplyDivide=pm.createNode('multiplyDivide',n='SwitchMultiplyDivide'+N)
		self.__SwitchReverse=pm.createNode('reverse',n='SwitchReverse'+N)
		
		
		pm.setAttr(self.__SwitchMultiplyDivide+'.caching',False)
		pm.setAttr(self.__SwitchMultiplyDivide+'.nodeState',0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.frozen',False)
		pm.setAttr(self.__SwitchMultiplyDivide+'.operation',1)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input1X',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input1Y',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input1Z',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input2X',0.10000000149)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input2Y',0.10000000149)
		pm.setAttr(self.__SwitchMultiplyDivide+'.input2Z',0.10000000149)
		pm.setAttr(self.__SwitchMultiplyDivide+'.outputX',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.outputY',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.outputZ',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput1X',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput1Y',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput1Z',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput2X',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput2Y',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiInput2Z',0.0)
		pm.setAttr(self.__SwitchMultiplyDivide+'.aiOperation',0)
		pm.setAttr(self.__SwitchReverse+'.caching',False)
		pm.setAttr(self.__SwitchReverse+'.nodeState',0)
		pm.setAttr(self.__SwitchReverse+'.frozen',False)
		pm.setAttr(self.__SwitchReverse+'.inputY',0.0)
		pm.setAttr(self.__SwitchReverse+'.inputZ',0.0)
		pm.setAttr(self.__SwitchReverse+'.outputX',1.0)
		pm.setAttr(self.__SwitchReverse+'.outputY',1.0)
		pm.setAttr(self.__SwitchReverse+'.outputZ',1.0)
		pm.setAttr(self.__SwitchReverse+'.aiInputR',0.0)
		pm.setAttr(self.__SwitchReverse+'.aiInputG',0.0)
		pm.setAttr(self.__SwitchReverse+'.aiInputB',0.0)
		
		pm.connectAttr(self.__SwitchMultiplyDivide+'.outputX',self.__SwitchReverse+'.inputX',f=True)
		
		self.outA = self.__SwitchReverse.ox
		self.inPlus = self.__SwitchMultiplyDivide.i1x
		self.outB = self.__SwitchMultiplyDivide.ox
		
		pm.refresh()
		
	def delete(self):
		pm.delete(self.__SwitchMultiplyDivide)
		pm.delete(self.__SwitchReverse)
def parSwitch(con,conObjA,conObjB,obj,dv=5,rootIf=False,translate=True,mo=True):
	pm.addAttr(con,ln='Switch',sn='Switch',at=float,min=0.0,max=10.0,dv=dv,k=1)
	#pm.pointConstraint(conObjA,obj,mo=1)
	#ptCon = pm.pointConstraint(conObjB,obj,mo=1)
	#ptCon = pm.pointConstraint((conObjA,conObjB),obj,mo=1)
	skipRotate=[]
	skipTranslate=[]
	if rootIf==False:
		skipRotate=['x','y','z']
	if translate == False:
		skipTranslate=['x','y','z']
	prCon=pm.parentConstraint((conObjA,conObjB),obj,mo=mo,skipRotate=skipRotate,skipTranslate=skipTranslate)
	prAttr = pm.parentConstraint(prCon,q=1,wal=1)
	SwitchCon = Switch()
	con.Switch >> SwitchCon.inPlus
	SwitchCon.outA >> prAttr[0]
	SwitchCon.outB >> prAttr[1]
def Polar_vector_switch(con,conObjA,conObjB,obj,dv=5,rootIf=False,translate=True,mo=True):
	pm.addAttr(con,ln='follow',sn='follow',at=float,min=0.0,max=10.0,dv=dv,k=1)
	#pm.pointConstraint(conObjA,obj,mo=1)
	#ptCon = pm.pointConstraint(conObjB,obj,mo=1)
	#ptCon = pm.pointConstraint((conObjA,conObjB),obj,mo=1)
	skipRotate=[]
	skipTranslate=[]
	if rootIf==False:
		skipRotate=['x','y','z']
	if translate == False:
		skipTranslate=['x','y','z']
	prCon=pm.parentConstraint((conObjA,conObjB),obj,mo=mo,skipRotate=skipRotate,skipTranslate=skipTranslate)
	prAttr = pm.parentConstraint(prCon,q=1,wal=1)
	SwitchCon = Switch()
	con.follow >> SwitchCon.inPlus
	SwitchCon.outA >> prAttr[0]
	SwitchCon.outB >> prAttr[1]
