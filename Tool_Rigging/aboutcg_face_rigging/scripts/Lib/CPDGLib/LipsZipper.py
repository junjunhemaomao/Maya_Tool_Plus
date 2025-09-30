#!/usr/bin/python
#encoding:gbk
import pymel.core as pm
'''
zipper拉链类
addZipperAttr添加拉链绑定属性
createZipper创建拉链绑定
'''
'''
拉链类
__init__(self,n|name=名称(默认无))#初始化
delete(self)#删除创建的节点
zipperPlus(self,zipperIn=控制器)
'''
class zipper:
	def __init__(self,**NAME):
		N = ''
		if 'n' in NAME:
			N = NAME['n']
		if 'name' in NAME:
			N = NAME['name']
		
		
		
		self.__zipperDriveR=pm.createNode('remapValue',n='zipperDriveR'+N)
		self.__zipperDriveL=pm.createNode('remapValue',n='zipperDriveL'+N)
		self.__zipperClamp=pm.createNode('clamp',n='zipperClamp'+N)
		self.__zipperSmoothRangeL=pm.createNode('remapValue',n='zipperSmoothRangeL'+N)
		self.__zipperPlusMinusAverage=pm.createNode('plusMinusAverage',n='zipperPlusMinusAverage'+N)
		self.__zipperSetRange=pm.createNode('setRange',n='zipperSetRange'+N)
		self.__zipperSmoothRangeR=pm.createNode('remapValue',n='zipperSmoothRangeR'+N)
		
		
		pm.setAttr(self.__zipperDriveR+'.caching',False)
		pm.setAttr(self.__zipperDriveR+'.nodeState',0)
		pm.setAttr(self.__zipperDriveR+'.frozen',False)
		pm.setAttr(self.__zipperDriveR+'.inputMin',0.0)
		pm.setAttr(self.__zipperDriveR+'.outputMin',0.0)
		pm.setAttr(self.__zipperDriveR+'.outputMax',1.0)
		pm.setAttr(self.__zipperDriveR+'.value[0].value_Position',0.0)
		pm.setAttr(self.__zipperDriveR+'.value[0].value_FloatValue',0.0)
		pm.setAttr(self.__zipperDriveR+'.value[0].value_Interp',2)
		pm.setAttr(self.__zipperDriveR+'.value[1].value_Position',1.0)
		pm.setAttr(self.__zipperDriveR+'.value[1].value_FloatValue',1.0)
		pm.setAttr(self.__zipperDriveR+'.value[1].value_Interp',2)
		pm.setAttr(self.__zipperDriveR+'.color[0].color_Position',0.0)
		pm.setAttr(self.__zipperDriveR+'.color[0].color_ColorR',0.0)
		pm.setAttr(self.__zipperDriveR+'.color[0].color_ColorG',0.0)
		pm.setAttr(self.__zipperDriveR+'.color[0].color_ColorB',0.0)
		pm.setAttr(self.__zipperDriveR+'.color[0].color_Interp',1)
		pm.setAttr(self.__zipperDriveR+'.color[1].color_Position',1.0)
		pm.setAttr(self.__zipperDriveR+'.color[1].color_ColorR',1.0)
		pm.setAttr(self.__zipperDriveR+'.color[1].color_ColorG',1.0)
		pm.setAttr(self.__zipperDriveR+'.color[1].color_ColorB',1.0)
		pm.setAttr(self.__zipperDriveR+'.color[1].color_Interp',1)
		pm.setAttr(self.__zipperDriveR+'.outValue',0.0)
		pm.setAttr(self.__zipperDriveR+'.outColorR',0.0)
		pm.setAttr(self.__zipperDriveR+'.outColorG',0.0)
		pm.setAttr(self.__zipperDriveR+'.outColorB',0.0)
		pm.setAttr(self.__zipperDriveL+'.caching',False)
		pm.setAttr(self.__zipperDriveL+'.nodeState',0)
		pm.setAttr(self.__zipperDriveL+'.frozen',False)
		pm.setAttr(self.__zipperDriveL+'.inputMin',0.0)
		pm.setAttr(self.__zipperDriveL+'.outputMin',0.0)
		pm.setAttr(self.__zipperDriveL+'.outputMax',1.0)
		pm.setAttr(self.__zipperDriveL+'.value[0].value_Position',0.0)
		pm.setAttr(self.__zipperDriveL+'.value[0].value_FloatValue',0.0)
		pm.setAttr(self.__zipperDriveL+'.value[0].value_Interp',2)
		pm.setAttr(self.__zipperDriveL+'.value[1].value_Position',1.0)
		pm.setAttr(self.__zipperDriveL+'.value[1].value_FloatValue',1.0)
		pm.setAttr(self.__zipperDriveL+'.value[1].value_Interp',2)
		pm.setAttr(self.__zipperDriveL+'.color[0].color_Position',0.0)
		pm.setAttr(self.__zipperDriveL+'.color[0].color_ColorR',0.0)
		pm.setAttr(self.__zipperDriveL+'.color[0].color_ColorG',0.0)
		pm.setAttr(self.__zipperDriveL+'.color[0].color_ColorB',0.0)
		pm.setAttr(self.__zipperDriveL+'.color[0].color_Interp',1)
		pm.setAttr(self.__zipperDriveL+'.color[1].color_Position',1.0)
		pm.setAttr(self.__zipperDriveL+'.color[1].color_ColorR',1.0)
		pm.setAttr(self.__zipperDriveL+'.color[1].color_ColorG',1.0)
		pm.setAttr(self.__zipperDriveL+'.color[1].color_ColorB',1.0)
		pm.setAttr(self.__zipperDriveL+'.color[1].color_Interp',1)
		pm.setAttr(self.__zipperDriveL+'.outValue',0.0)
		pm.setAttr(self.__zipperDriveL+'.outColorR',0.0)
		pm.setAttr(self.__zipperDriveL+'.outColorG',0.0)
		pm.setAttr(self.__zipperDriveL+'.outColorB',0.0)
		pm.setAttr(self.__zipperClamp+'.caching',False)
		pm.setAttr(self.__zipperClamp+'.nodeState',0)
		pm.setAttr(self.__zipperClamp+'.frozen',False)
		pm.setAttr(self.__zipperClamp+'.minR',0.0)
		pm.setAttr(self.__zipperClamp+'.minG',0.0)
		pm.setAttr(self.__zipperClamp+'.minB',0.0)
		pm.setAttr(self.__zipperClamp+'.maxR',1.0)
		pm.setAttr(self.__zipperClamp+'.maxG',1.0)
		pm.setAttr(self.__zipperClamp+'.maxB',1.0)
		pm.setAttr(self.__zipperClamp+'.inputG',0.0)
		pm.setAttr(self.__zipperClamp+'.inputB',0.0)
		pm.setAttr(self.__zipperClamp+'.renderPassMode',1)
		pm.setAttr(self.__zipperClamp+'.outputR',0.0)
		pm.setAttr(self.__zipperClamp+'.outputG',0.0)
		pm.setAttr(self.__zipperClamp+'.outputB',0.0)
		pm.setAttr(self.__zipperClamp+'.aiMinR',0.0)
		pm.setAttr(self.__zipperClamp+'.aiMinG',0.0)
		pm.setAttr(self.__zipperClamp+'.aiMinB',0.0)
		pm.setAttr(self.__zipperClamp+'.aiMaxR',1.0)
		pm.setAttr(self.__zipperClamp+'.aiMaxG',1.0)
		pm.setAttr(self.__zipperClamp+'.aiMaxB',1.0)
		pm.setAttr(self.__zipperClamp+'.aiInputR',0.0)
		pm.setAttr(self.__zipperClamp+'.aiInputG',0.0)
		pm.setAttr(self.__zipperClamp+'.aiInputB',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.caching',False)
		pm.setAttr(self.__zipperSmoothRangeL+'.nodeState',0)
		pm.setAttr(self.__zipperSmoothRangeL+'.frozen',False)
		pm.setAttr(self.__zipperSmoothRangeL+'.inputMin',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.inputMax',10.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.outputMin',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.outputMax',10.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[0].value_Position',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[0].value_FloatValue',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[0].value_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[1].value_Position',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[1].value_FloatValue',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.value[1].value_Interp',2)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[0].color_Position',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[0].color_ColorR',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[0].color_ColorG',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[0].color_ColorB',0.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[0].color_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[1].color_Position',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[1].color_ColorR',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[1].color_ColorG',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[1].color_ColorB',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.color[1].color_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeL+'.outValue',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.outColorR',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.outColorG',1.0)
		pm.setAttr(self.__zipperSmoothRangeL+'.outColorB',1.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.caching',False)
		pm.setAttr(self.__zipperPlusMinusAverage+'.nodeState',0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.frozen',False)
		pm.setAttr(self.__zipperPlusMinusAverage+'.operation',1)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output1D',0.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output2Dx',0.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output2Dy',0.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output3Dx',0.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output3Dy',0.0)
		pm.setAttr(self.__zipperPlusMinusAverage+'.output3Dz',0.0)
		pm.setAttr(self.__zipperSetRange+'.caching',False)
		pm.setAttr(self.__zipperSetRange+'.nodeState',0)
		pm.setAttr(self.__zipperSetRange+'.frozen',False)
		pm.setAttr(self.__zipperSetRange+'.valueZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.minX',0.0)
		pm.setAttr(self.__zipperSetRange+'.minY',1.0)
		pm.setAttr(self.__zipperSetRange+'.minZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.maxX',0.5)
		pm.setAttr(self.__zipperSetRange+'.maxY',0.5)
		pm.setAttr(self.__zipperSetRange+'.maxZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.oldMinX',0.0)
		pm.setAttr(self.__zipperSetRange+'.oldMinY',0.0)
		pm.setAttr(self.__zipperSetRange+'.oldMinZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.oldMaxX',1.0)
		pm.setAttr(self.__zipperSetRange+'.oldMaxY',1.0)
		pm.setAttr(self.__zipperSetRange+'.oldMaxZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.outValueX',0.0)
		pm.setAttr(self.__zipperSetRange+'.outValueY',1.0)
		pm.setAttr(self.__zipperSetRange+'.outValueZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiValueX',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiValueY',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiValueZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMinX',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMinY',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMinZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMaxX',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMaxY',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiMaxZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMinX',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMinY',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMinZ',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMaxX',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMaxY',0.0)
		pm.setAttr(self.__zipperSetRange+'.aiOldMaxZ',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.caching',False)
		pm.setAttr(self.__zipperSmoothRangeR+'.nodeState',0)
		pm.setAttr(self.__zipperSmoothRangeR+'.frozen',False)
		pm.setAttr(self.__zipperSmoothRangeR+'.inputMin',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.inputMax',10.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.outputMin',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.outputMax',10.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[0].value_Position',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[0].value_FloatValue',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[0].value_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[1].value_Position',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[1].value_FloatValue',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.value[1].value_Interp',2)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[0].color_Position',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[0].color_ColorR',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[0].color_ColorG',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[0].color_ColorB',0.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[0].color_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[1].color_Position',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[1].color_ColorR',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[1].color_ColorG',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[1].color_ColorB',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.color[1].color_Interp',1)
		pm.setAttr(self.__zipperSmoothRangeR+'.outValue',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.outColorR',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.outColorG',1.0)
		pm.setAttr(self.__zipperSmoothRangeR+'.outColorB',1.0)
		
		pm.connectAttr(self.__zipperSmoothRangeR+'.outValue',self.__zipperDriveR+'.inputMax',f=True)
		pm.connectAttr(self.__zipperSmoothRangeL+'.outValue',self.__zipperDriveL+'.inputMax',f=True)
		pm.connectAttr(self.__zipperPlusMinusAverage+'.output1D',self.__zipperClamp+'.inputR',f=True)
		pm.connectAttr(self.__zipperDriveL+'.outValue',self.__zipperPlusMinusAverage+'.input1D[0]',f=True)
		pm.connectAttr(self.__zipperDriveR+'.outValue',self.__zipperPlusMinusAverage+'.input1D[1]',f=True)
		pm.connectAttr(self.__zipperClamp+'.outputR',self.__zipperSetRange+'.valueX',f=True)
		pm.connectAttr(self.__zipperClamp+'.outputR',self.__zipperSetRange+'.valueY',f=True)
		pm.connectAttr(self.__zipperSmoothRangeL+'.inputValue',self.__zipperSmoothRangeR+'.inputValue',f=True)
		
		self.zipperRStart = self.__zipperDriveR.imn#R拉链开始
		self.zipperLMinEnd = self.__zipperSmoothRangeL.omn#L拉链最小结束
		self.inL = self.__zipperDriveL.i#L驱动输入
		self.outReverse = self.__zipperSetRange.oy#输出1-0.5
		self.out = self.__zipperSetRange.ox#输出0-0.5
		self.zipperRMinEnd = self.__zipperSmoothRangeR.omn#R拉链最小结束
		self.zipperLStart = self.__zipperDriveL.imn#L拉链开始
		self.smoothCon = self.__zipperSmoothRangeL.i#平滑控制输入
		self.inR = self.__zipperDriveR.i#R驱动输入
		
		pm.refresh()
		
	def delete(self):
		pm.delete(self.__zipperDriveR)
		pm.delete(self.__zipperDriveL)
		pm.delete(self.__zipperClamp)
		pm.delete(self.__zipperSmoothRangeL)
		pm.delete(self.__zipperPlusMinusAverage)
		pm.delete(self.__zipperSetRange)
		pm.delete(self.__zipperSmoothRangeR)
	def zipperPlus(self,zipperIn):
		pm.connectAttr(zipperIn+'.zipperR',self.__zipperDriveR+'.inputValue',f=True)
		pm.connectAttr(zipperIn+'.zipperL',self.__zipperDriveL+'.inputValue',f=True)
		pm.connectAttr(zipperIn+'.zipperSmooth',self.__zipperSmoothRangeL+'.inputValue',f=True)
#添加拉链绑定需要的属性（对象列表）
def addZipperAttr(objList):
	for i in objList:		
		pm.addAttr(i,ln='zipperL',sn='zipperL',at=float,min=0.0,max=10.0,dv=0.0,k=1)
		pm.addAttr(i,ln='zipperR',sn='zipperR',at=float,min=0.0,max=10.0,dv=0.0,k=1)
		pm.addAttr(i,ln='zipperSmooth',sn='zipperSmooth',at=float,min=0.0,max=10.0,dv=0.0,k=1)
#addZipperAttr([con])
'''
con = 拉链控制器（不会自动添加属性请使用addZipperAttr）
conObjA = 控制物体A
conObjB = 控制物体B
BeConObjA = 被控制物体A
BeConObjB = 被控制物体B
LToR = 从L到R的拉链开始和结束（L开始位置，结束位置，R开始位置（使用时自动10减去他））ps：大小顺序应该为（最小，中，最大）

con = pm.selected()[0]
conObjA = pm.selected()[0]
conObjB = pm.selected()[0]
BeConObjA = pm.selected()[0]
BeConObjB = pm.selected()[0]
LToR = (0,1,2)
'''
def createZipper(con,conObjA,conObjB,BeConObjA,BeConObjB,LToR):
	parA = pm.parentConstraint((conObjA,conObjB),BeConObjA,mo=1)
	parB = pm.parentConstraint((conObjA,conObjB),BeConObjB,mo=1)
	parAAttr = pm.parentConstraint(parA,q=1,wal=1)
	parBAttr = pm.parentConstraint(parB,q=1,wal=1)
	zipperclass = zipper()
	zipperclass.zipperPlus(con)
	
	zipperclass.out >> parAAttr[1]
	zipperclass.out >> parBAttr[0]
	zipperclass.outReverse >> parAAttr[0]
	zipperclass.outReverse >> parBAttr[1]
	
	zipperclass.zipperLStart.set(LToR[0])
	zipperclass.zipperRStart.set(10-LToR[2])
	
	zipperclass.zipperLMinEnd.set(LToR[1])
	zipperclass.zipperRMinEnd.set(10-LToR[1])
