#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.9.22
#最近修改时间:
#本模块提供了绝对值节点集的快速创建
import pymel.core as pm
#绝对值
class ABS:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		self.__absRemapValue=pm.createNode('remapValue',n='absRemapValue'+N)
		
		
		self.__absRemapValue.caching.set(False)
		self.__absRemapValue.frozen.set(False)
		self.__absRemapValue.nodeState.set(0)
		self.__absRemapValue.inputValue.set(0.0)
		self.__absRemapValue.inputMin.set(-100000.0)
		self.__absRemapValue.inputMax.set(100000.0)
		self.__absRemapValue.outputMin.set(-100000.0)
		self.__absRemapValue.outputMax.set(100000.0)
		self.__absRemapValue.value[0].value_Position.set(0.0)
		self.__absRemapValue.value[0].value_FloatValue.set(1.0)
		self.__absRemapValue.value[0].value_Interp.set(1)
		self.__absRemapValue.value[1].value_Position.set(1.0)
		self.__absRemapValue.value[1].value_FloatValue.set(1.0)
		self.__absRemapValue.value[1].value_Interp.set(1)
		self.__absRemapValue.value[2].value_Position.set(0.5)
		self.__absRemapValue.value[2].value_FloatValue.set(0.0)
		self.__absRemapValue.value[2].value_Interp.set(1)
		
		self.input = self.__absRemapValue.i
		self.out = self.__absRemapValue.ov
		
		pm.refresh()
#三元绝对值
class absDouble3:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		self.__absMd=pm.createNode('multiplyDivide',n='absMd'+N)
		self.__conditionZ=pm.createNode('condition',n='conditionZ'+N)
		self.__conditionY=pm.createNode('condition',n='conditionY'+N)
		self.__conditionX=pm.createNode('condition',n='conditionX'+N)
		
		
		self.__absMd.caching.set(False)
		self.__absMd.frozen.set(False)
		self.__absMd.nodeState.set(0)
		self.__absMd.operation.set(1)
		self.__absMd.input1X.set(0.0)
		self.__absMd.input1Y.set(0.0)
		self.__absMd.input1Z.set(0.0)
		self.__absMd.input2X.set(-1.0)
		self.__absMd.input2Y.set(-1.0)
		self.__absMd.input2Z.set(-1.0)
		self.__absMd.outputX.set(-0.0)
		self.__absMd.outputY.set(-0.0)
		self.__absMd.outputZ.set(-0.0)
		self.__absMd.aiInput1X.set(0.0)
		self.__absMd.aiInput1Y.set(0.0)
		self.__absMd.aiInput1Z.set(0.0)
		self.__absMd.aiInput2X.set(0.0)
		self.__absMd.aiInput2Y.set(0.0)
		self.__absMd.aiInput2Z.set(0.0)
		self.__absMd.aiOperation.set(0)
		self.__conditionZ.caching.set(False)
		self.__conditionZ.frozen.set(False)
		self.__conditionZ.nodeState.set(0)
		self.__conditionZ.operation.set(4)
		self.__conditionZ.secondTerm.set(0.0)
		self.__conditionZ.colorIfTrueG.set(0.0)
		self.__conditionZ.colorIfTrueB.set(0.0)
		self.__conditionZ.colorIfFalseG.set(1.0)
		self.__conditionZ.colorIfFalseB.set(1.0)
		self.__conditionZ.outColorR.set(0.0)
		self.__conditionZ.outColorG.set(1.0)
		self.__conditionZ.outColorB.set(1.0)
		self.__conditionZ.aiOperation.set(0)
		self.__conditionZ.aiFirstTerm.set(0.0)
		self.__conditionZ.aiSecondTerm.set(0.0)
		self.__conditionZ.aiColorIfTrueR.set(0.0)
		self.__conditionZ.aiColorIfTrueG.set(0.0)
		self.__conditionZ.aiColorIfTrueB.set(0.0)
		self.__conditionZ.aiColorIfFalseR.set(1.0)
		self.__conditionZ.aiColorIfFalseG.set(1.0)
		self.__conditionZ.aiColorIfFalseB.set(1.0)
		self.__conditionY.caching.set(False)
		self.__conditionY.frozen.set(False)
		self.__conditionY.nodeState.set(0)
		self.__conditionY.operation.set(4)
		self.__conditionY.secondTerm.set(0.0)
		self.__conditionY.colorIfTrueG.set(0.0)
		self.__conditionY.colorIfTrueB.set(0.0)
		self.__conditionY.colorIfFalseG.set(1.0)
		self.__conditionY.colorIfFalseB.set(1.0)
		self.__conditionY.outColorR.set(0.0)
		self.__conditionY.outColorG.set(1.0)
		self.__conditionY.outColorB.set(1.0)
		self.__conditionY.aiOperation.set(0)
		self.__conditionY.aiFirstTerm.set(0.0)
		self.__conditionY.aiSecondTerm.set(0.0)
		self.__conditionY.aiColorIfTrueR.set(0.0)
		self.__conditionY.aiColorIfTrueG.set(0.0)
		self.__conditionY.aiColorIfTrueB.set(0.0)
		self.__conditionY.aiColorIfFalseR.set(1.0)
		self.__conditionY.aiColorIfFalseG.set(1.0)
		self.__conditionY.aiColorIfFalseB.set(1.0)
		self.__conditionX.caching.set(False)
		self.__conditionX.frozen.set(False)
		self.__conditionX.nodeState.set(0)
		self.__conditionX.operation.set(4)
		self.__conditionX.secondTerm.set(0.0)
		self.__conditionX.colorIfTrueG.set(0.0)
		self.__conditionX.colorIfTrueB.set(0.0)
		self.__conditionX.colorIfFalseG.set(1.0)
		self.__conditionX.colorIfFalseB.set(1.0)
		self.__conditionX.outColorR.set(0.0)
		self.__conditionX.outColorG.set(1.0)
		self.__conditionX.outColorB.set(1.0)
		self.__conditionX.aiOperation.set(0)
		self.__conditionX.aiFirstTerm.set(0.0)
		self.__conditionX.aiSecondTerm.set(0.0)
		self.__conditionX.aiColorIfTrueR.set(0.0)
		self.__conditionX.aiColorIfTrueG.set(0.0)
		self.__conditionX.aiColorIfTrueB.set(0.0)
		self.__conditionX.aiColorIfFalseR.set(1.0)
		self.__conditionX.aiColorIfFalseG.set(1.0)
		self.__conditionX.aiColorIfFalseB.set(1.0)
		
		self.__absMd.input1Z >> self.__conditionZ.firstTerm
		self.__absMd.outputZ >> self.__conditionZ.colorIfTrueR
		self.__absMd.input1Z >> self.__conditionZ.colorIfFalseR
		self.__absMd.input1Y >> self.__conditionY.firstTerm
		self.__absMd.outputY >> self.__conditionY.colorIfTrueR
		self.__absMd.input1Y >> self.__conditionY.colorIfFalseR
		self.__absMd.input1X >> self.__conditionX.firstTerm
		self.__absMd.outputX >> self.__conditionX.colorIfTrueR
		self.__absMd.input1X >> self.__conditionX.colorIfFalseR
		
		self.inz = self.__absMd.i1z
		self.inx = self.__absMd.i1x
		self.iny = self.__absMd.i1y
		self.ox = self.__conditionX.ocr
		self.oy = self.__conditionY.ocr
		self.oz = self.__conditionZ.ocr
		
		pm.refresh()
