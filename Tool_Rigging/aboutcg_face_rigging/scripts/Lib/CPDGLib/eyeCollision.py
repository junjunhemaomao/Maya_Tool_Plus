#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.9.22
#最近修改时间:
#本模块提供了眼睛碰撞节点连接的快速创建
'''
eyeCollision.collisionSwitching
提供了碰撞切换的接口0为上碰撞下10为下碰撞上
eyeCollision.collisionLess
提供了碰撞中间距离减去功能将关节中间距离输入即可减去已生成正常的碰撞
eyeCollision.UPAdd
提供了上旋转叠加的数组输入
eyeCollision.LOWEAdd
提供了下旋转叠加的数组输入
eyeCollision.UPOut
提供了上旋转输出
eyeCollision.LOWEOut
提供了下旋转输出
注意使用本模块的关节需要旋转下是-Z向上是Z+
'''
import pymel.core as pm
class eyeCollision:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__LOWECollisionSwitchingBlendColors=pm.createNode('blendColors',n='LOWECollisionSwitchingBlendColors'+N)
		self.__UPCollisionSwitchingBlendColors=pm.createNode('blendColors',n='UPCollisionSwitchingBlendColors'+N)
		self.__UPSwitchingLess=pm.createNode('plusMinusAverage',n='UPSwitchingLess'+N)
		self.__LOWESwitchingLess=pm.createNode('plusMinusAverage',n='LOWESwitchingLess'+N)
		self.__UPClamp=pm.createNode('clamp',n='UPClamp'+N)
		self.__UPAdd=pm.createNode('plusMinusAverage',n='UPAdd'+N)
		self.__LOWEAdd=pm.createNode('plusMinusAverage',n='LOWEAdd'+N)
		self.__LOWEClamp=pm.createNode('clamp',n='LOWEClamp'+N)
		self.__SwitchingMd=pm.createNode('multiplyDivide',n='SwitchingMd'+N)
		self.__collisionReverse=pm.createNode('reverse',n='collisionReverse'+N)
		
		
		self.__LOWECollisionSwitchingBlendColors.caching.set(False)
		self.__LOWECollisionSwitchingBlendColors.frozen.set(False)
		self.__LOWECollisionSwitchingBlendColors.nodeState.set(0)
		self.__LOWECollisionSwitchingBlendColors.renderPassMode.set(1)
		self.__LOWECollisionSwitchingBlendColors.outputR.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.outputG.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.outputB.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.aiBlender.set(0.5)
		self.__LOWECollisionSwitchingBlendColors.aiColor1R.set(1.0)
		self.__LOWECollisionSwitchingBlendColors.aiColor1G.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.aiColor1B.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.aiColor2R.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.aiColor2G.set(0.0)
		self.__LOWECollisionSwitchingBlendColors.aiColor2B.set(1.0)
		self.__UPCollisionSwitchingBlendColors.caching.set(False)
		self.__UPCollisionSwitchingBlendColors.frozen.set(False)
		self.__UPCollisionSwitchingBlendColors.nodeState.set(0)
		self.__UPCollisionSwitchingBlendColors.renderPassMode.set(1)
		self.__UPCollisionSwitchingBlendColors.outputR.set(0.0)
		self.__UPCollisionSwitchingBlendColors.outputG.set(0.0)
		self.__UPCollisionSwitchingBlendColors.outputB.set(0.0)
		self.__UPCollisionSwitchingBlendColors.aiBlender.set(0.5)
		self.__UPCollisionSwitchingBlendColors.aiColor1R.set(1.0)
		self.__UPCollisionSwitchingBlendColors.aiColor1G.set(0.0)
		self.__UPCollisionSwitchingBlendColors.aiColor1B.set(0.0)
		self.__UPCollisionSwitchingBlendColors.aiColor2R.set(0.0)
		self.__UPCollisionSwitchingBlendColors.aiColor2G.set(0.0)
		self.__UPCollisionSwitchingBlendColors.aiColor2B.set(1.0)
		self.__UPSwitchingLess.caching.set(False)
		self.__UPSwitchingLess.frozen.set(False)
		self.__UPSwitchingLess.nodeState.set(0)
		self.__UPSwitchingLess.operation.set(1)
		self.__UPSwitchingLess.output1D.set(0.0)
		self.__UPSwitchingLess.output2Dx.set(0.0)
		self.__UPSwitchingLess.output2Dy.set(0.0)
		self.__UPSwitchingLess.output3Dx.set(0.0)
		self.__UPSwitchingLess.output3Dy.set(0.0)
		self.__UPSwitchingLess.output3Dz.set(0.0)
		self.__LOWESwitchingLess.caching.set(False)
		self.__LOWESwitchingLess.frozen.set(False)
		self.__LOWESwitchingLess.nodeState.set(0)
		self.__LOWESwitchingLess.operation.set(1)
		self.__LOWESwitchingLess.output1D.set(0.0)
		self.__LOWESwitchingLess.output2Dx.set(0.0)
		self.__LOWESwitchingLess.output2Dy.set(0.0)
		self.__LOWESwitchingLess.output3Dx.set(0.0)
		self.__LOWESwitchingLess.output3Dy.set(0.0)
		self.__LOWESwitchingLess.output3Dz.set(0.0)
		self.__UPClamp.caching.set(False)
		self.__UPClamp.frozen.set(False)
		self.__UPClamp.nodeState.set(0)
		self.__UPClamp.minR.set(-100000.0)
		self.__UPClamp.minG.set(-100000.0)
		self.__UPClamp.maxR.set(100000.0)
		self.__UPClamp.maxG.set(100000.0)
		self.__UPClamp.maxB.set(100000.0)
		self.__UPClamp.renderPassMode.set(1)
		self.__UPClamp.outputR.set(0.0)
		self.__UPClamp.outputG.set(0.0)
		self.__UPClamp.outputB.set(0.0)
		self.__UPClamp.aiMinR.set(0.0)
		self.__UPClamp.aiMinG.set(0.0)
		self.__UPClamp.aiMinB.set(0.0)
		self.__UPClamp.aiMaxR.set(1.0)
		self.__UPClamp.aiMaxG.set(1.0)
		self.__UPClamp.aiMaxB.set(1.0)
		self.__UPClamp.aiInputR.set(0.0)
		self.__UPClamp.aiInputG.set(0.0)
		self.__UPClamp.aiInputB.set(0.0)
		self.__UPAdd.caching.set(False)
		self.__UPAdd.frozen.set(False)
		self.__UPAdd.nodeState.set(0)
		self.__UPAdd.operation.set(1)
		self.__UPAdd.output1D.set(0.0)
		self.__UPAdd.output2Dx.set(0.0)
		self.__UPAdd.output2Dy.set(0.0)
		self.__UPAdd.output3Dx.set(0.0)
		self.__UPAdd.output3Dy.set(0.0)
		self.__UPAdd.output3Dz.set(0.0)
		self.__LOWEAdd.caching.set(False)
		self.__LOWEAdd.frozen.set(False)
		self.__LOWEAdd.nodeState.set(0)
		self.__LOWEAdd.operation.set(1)
		self.__LOWEAdd.output1D.set(0.0)
		self.__LOWEAdd.output2Dx.set(0.0)
		self.__LOWEAdd.output2Dy.set(0.0)
		self.__LOWEAdd.output3Dx.set(0.0)
		self.__LOWEAdd.output3Dy.set(0.0)
		self.__LOWEAdd.output3Dz.set(0.0)
		self.__LOWEClamp.caching.set(False)
		self.__LOWEClamp.frozen.set(False)
		self.__LOWEClamp.nodeState.set(0)
		self.__LOWEClamp.minR.set(-100000.0)
		self.__LOWEClamp.minG.set(-100000.0)
		self.__LOWEClamp.minB.set(-100000.0)
		self.__LOWEClamp.maxR.set(100000.0)
		self.__LOWEClamp.maxG.set(100000.0)
		self.__LOWEClamp.inputR.set(0.0)
		self.__LOWEClamp.inputG.set(0.0)
		self.__LOWEClamp.inputB.set(0.0)
		self.__LOWEClamp.renderPassMode.set(1)
		self.__LOWEClamp.outputR.set(0.0)
		self.__LOWEClamp.outputG.set(0.0)
		self.__LOWEClamp.outputB.set(0.0)
		self.__LOWEClamp.aiMinR.set(0.0)
		self.__LOWEClamp.aiMinG.set(0.0)
		self.__LOWEClamp.aiMinB.set(0.0)
		self.__LOWEClamp.aiMaxR.set(1.0)
		self.__LOWEClamp.aiMaxG.set(1.0)
		self.__LOWEClamp.aiMaxB.set(1.0)
		self.__LOWEClamp.aiInputR.set(0.0)
		self.__LOWEClamp.aiInputG.set(0.0)
		self.__LOWEClamp.aiInputB.set(0.0)
		self.__SwitchingMd.caching.set(False)
		self.__SwitchingMd.frozen.set(False)
		self.__SwitchingMd.nodeState.set(0)
		self.__SwitchingMd.operation.set(1)
		self.__SwitchingMd.input1X.set(0.0)
		self.__SwitchingMd.input1Y.set(0.0)
		self.__SwitchingMd.input1Z.set(0.0)
		self.__SwitchingMd.input2X.set(0.10000000149)
		self.__SwitchingMd.input2Y.set(-1.0)
		self.__SwitchingMd.input2Z.set(0.10000000149)
		self.__SwitchingMd.outputX.set(0.0)
		self.__SwitchingMd.outputY.set(-0.0)
		self.__SwitchingMd.outputZ.set(0.0)
		self.__SwitchingMd.aiInput1X.set(0.0)
		self.__SwitchingMd.aiInput1Y.set(0.0)
		self.__SwitchingMd.aiInput1Z.set(0.0)
		self.__SwitchingMd.aiInput2X.set(0.0)
		self.__SwitchingMd.aiInput2Y.set(0.0)
		self.__SwitchingMd.aiInput2Z.set(0.0)
		self.__SwitchingMd.aiOperation.set(0)
		self.__collisionReverse.caching.set(False)
		self.__collisionReverse.frozen.set(False)
		self.__collisionReverse.nodeState.set(0)
		self.__collisionReverse.inputY.set(0.0)
		self.__collisionReverse.inputZ.set(0.0)
		self.__collisionReverse.outputX.set(1.0)
		self.__collisionReverse.outputY.set(1.0)
		self.__collisionReverse.outputZ.set(1.0)
		self.__collisionReverse.aiInputR.set(0.0)
		self.__collisionReverse.aiInputG.set(0.0)
		self.__collisionReverse.aiInputB.set(0.0)
		
		self.__collisionReverse.outputX >> self.__LOWECollisionSwitchingBlendColors.blender
		self.__LOWEClamp.output >> self.__LOWECollisionSwitchingBlendColors.color1
		self.__LOWEAdd.output3D >> self.__LOWECollisionSwitchingBlendColors.color2
		self.__collisionReverse.inputX >> self.__UPCollisionSwitchingBlendColors.blender
		self.__UPClamp.output >> self.__UPCollisionSwitchingBlendColors.color1
		self.__UPAdd.output3D >> self.__UPCollisionSwitchingBlendColors.color2
		self.__LOWEAdd.output3Dz >> self.__UPSwitchingLess.input1D[0]
		self.__SwitchingMd.outputY >> self.__UPSwitchingLess.input1D[1]
		self.__UPAdd.output3Dz >> self.__LOWESwitchingLess.input1D[0]
		self.__SwitchingMd.input1Y >> self.__LOWESwitchingLess.input1D[1]
		self.__UPSwitchingLess.output1D >> self.__UPClamp.minB
		self.__UPAdd.output3D >> self.__UPClamp.input
		self.__LOWESwitchingLess.output1D >> self.__LOWEClamp.maxB
		self.__SwitchingMd.outputX >> self.__collisionReverse.inputX
		
		self.collisionSwitching = self.__SwitchingMd.i1x
		self.collisionLess = self.__SwitchingMd.i1y
		self.LOWEOut = self.__LOWECollisionSwitchingBlendColors.op
		self.UPAdd = self.__UPAdd.i3
		self.LOWEAdd = self.__LOWEAdd.i3
		self.UPOut = self.__UPCollisionSwitchingBlendColors.op
		
		pm.refresh()
