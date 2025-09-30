#!/usr/bin/python
#encoding:gbk
#本模块实现了矩阵效果的类
import pymel.core as pm

'''
point点约束
orient方向约束
scale缩放约束
parent父对象约束
shear斜切约束
complete完全约束
delete删除
'''
class constraint:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__multMatrix=pm.createNode('multMatrix',n='multMatrix'+N)
		self.__decomposeMatrix=pm.createNode('decomposeMatrix',n='decomposeMatrix'+N)
		
		
		pm.setAttr(self.__multMatrix+'.caching',False)
		pm.setAttr(self.__multMatrix+'.nodeState',0)
		pm.setAttr(self.__multMatrix+'.frozen',False)
		pm.setAttr(self.__decomposeMatrix+'.caching',False)
		pm.setAttr(self.__decomposeMatrix+'.nodeState',0)
		pm.setAttr(self.__decomposeMatrix+'.frozen',False)
		pm.setAttr(self.__decomposeMatrix+'.inputRotateOrder',0)
		pm.setAttr(self.__decomposeMatrix+'.outputTranslateX',0.0)
		pm.setAttr(self.__decomposeMatrix+'.outputTranslateY',0.0)
		pm.setAttr(self.__decomposeMatrix+'.outputTranslateZ',0.0)
		pm.setAttr(self.__decomposeMatrix+'.outputRotateX',0.0)
		pm.setAttr(self.__decomposeMatrix+'.outputRotateY',-0.0)
		pm.setAttr(self.__decomposeMatrix+'.outputRotateZ',0.0)
		
		pm.connectAttr(self.__multMatrix+'.matrixSum',self.__decomposeMatrix+'.inputMatrix',f=True)
		
		
		pm.refresh()
		
	def delete(self):
		pm.delete(self.__multMatrix)
		pm.delete(self.__decomposeMatrix)
	def point(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputTranslate',outObj+'.translate',f=True)
	def orient(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputRotate',outObj+'.rotate',f=True)
	def scale(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputScale',outObj+'.scale',f=True)
	def parent(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputTranslate',outObj+'.translate',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputRotate',outObj+'.rotate',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputShear',outObj+'.shear',f=True)
	def shear(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputShear',outObj+'.shear',f=True)
	def complete(self,inObj,outObj):
		pm.connectAttr(inObj+'.worldMatrix[0]',self.__multMatrix+'.matrixIn[0]',f=True)
		pm.connectAttr(outObj+'.parentInverseMatrix[0]',self.__multMatrix+'.matrixIn[1]',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputTranslate',outObj+'.translate',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputRotate',outObj+'.rotate',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputScale',outObj+'.scale',f=True)
		pm.connectAttr(self.__decomposeMatrix+'.outputShear',outObj+'.shear',f=True)
class getWorldMatrix:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__decomposeMatrixWorld=pm.createNode('decomposeMatrix',n='decomposeMatrixWorld'+N)
		
		
		pm.setAttr(self.__decomposeMatrixWorld+'.caching',False)
		pm.setAttr(self.__decomposeMatrixWorld+'.nodeState',0)
		pm.setAttr(self.__decomposeMatrixWorld+'.frozen',False)
		pm.setAttr(self.__decomposeMatrixWorld+'.inputRotateOrder',0)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputTranslateX',3.0)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputTranslateY',0.0)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputTranslateZ',-1.0)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputRotateX',0.0)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputRotateY',-18.4349488229)
		pm.setAttr(self.__decomposeMatrixWorld+'.outputRotateZ',0.0)
		
		
		
		pm.refresh()
		
	def delete(self):
		pm.delete(self.__decomposeMatrixWorld)
	def inplus(self,joint2):
		pm.connectAttr(joint2+'.worldMatrix[0]',self.__decomposeMatrixWorld+'.inputMatrix',f=True)
	def outplus(self,outWorldTranslate):
		pm.connectAttr(self.__decomposeMatrixWorld+'.outputTranslate',outWorldTranslate+'.translate',f=True)
	def getWorldPos(self,outWorldTranslate):
		pm.getAttr(self.__decomposeMatrixWorld+'.outputTranslate')
