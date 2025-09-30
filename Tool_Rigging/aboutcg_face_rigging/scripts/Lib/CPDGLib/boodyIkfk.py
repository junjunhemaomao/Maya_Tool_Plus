#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.8.5
#最近修改时间:2019.10.25
"""
本模块为boody绑定提供ikfk功能函数集
"""
''' 
函数：
ikfkJoint 建立ikfk关节
ikfk 建立ikfk切换绑定
ikfkRig 建立ikfk切换绑定自动建立ikfk关节
ikStretchAddAttr 建立ik拉伸绑定需要的属性
ikStretch 完成ik拉伸绑定输入ik控制器，关节列表，拉伸控制属性，拉伸最小值控制属性，拉伸最大值控制属性返回拉伸定位器组，拉伸定位器开始拉伸定位器结束，关节缩放控制属性（函数中并没有链接上）
ikLockingAddAttr 添加肘部锁定绑定需要的属性
ikLocking 自动建立ik绑定输入ik控制器，极向量控制器，关节列表（3个），肘部锁定控制属性，拉伸控制属性，拉伸最小值控制属性，拉伸最大值控制属性，返回距离计算定位器组
ikStrtchRig 自动建立ik绑定输入关节列表（3个），ik控制器，极向量控制器，返回距离计算定位器组
访问示例：
ikfkJoint（关节列表）
ikfk（切换控制器，控制属性，控制属性乘以一个数值，ik关节列表，fk关节列表，sk关节列表）
ikfkRig（切换控制器，控制属性，控制属性乘以一个数值，关节列表）
'''
import pymel.core as pm
import Cangphantom.Lib.CPFnCreateCon as CreateCon
#ikfk切换
#ikfkJoint 建立ikfk关节，ikfkJoint（关节列表）
def ikfkAddAttr(con):
	pm.addAttr(con,ln = 'ikfk' , at = 'float' , min = 0 , max = 10 , dv = 0 , k = 1)
	return 0
#创建ikfk关节
def ikfkJoint(Jin):
	if type(Jin)!=list:
		Jin = [Jin]
	Jin = [pm.general.PyNode(i) for i in Jin]
	ik = pm.duplicate(Jin)
	fk = pm.duplicate(Jin)
	ik = [pm.rename(ik[i],'Ik_'+Jin[i].nodeName()) for i in range(len(Jin))]
	fk = [pm.rename(fk[i],'Fk_'+Jin[i].nodeName()) for i in range(len(Jin))]
	sk = [pm.rename(Jin[i],'Sk_'+Jin[i].nodeName()) for i in range(len(Jin))]
	return (ik,fk,sk)
#ikfk 建立ikfk切换绑定,ikfk（切换控制器，控制属性，控制属性乘以一个数值，ik关节列表，fk关节列表，sk关节列表）
def ikfk(con,attr,zoomCon,ik,fk,sk):
	if type(ik)!=list:
		ik = [ik]
	if type(fk)!=list:
		fk = [fk]
	if type(sk)!=list:
		sk = [sk]
	ik = [pm.general.PyNode(i) for i in ik]
	fk = [pm.general.PyNode(i) for i in fk]
	sk = [pm.general.PyNode(i) for i in sk]
	attr = pm.general.PyNode(con+'.'+attr)
	par = [pm.parentConstraint((ik[i],fk[i]),sk[i]) for i in range(len(ik))]
	wal = [pm.parentConstraint(i , q = 1 , wal = 1) for i in par]
	md = pm.createNode('multiplyDivide',n=sk[0].split('|')[-1]+'_multiplyDivide_Ikfk')
	attr.connect(md.input1X)
	md.input2X.set(zoomCon)
	reverse = pm.createNode('reverse',n=sk[0].split('|')[-1]+'_reverse_Ikfk')
	md.ox.connect(reverse.ix)
	[[md.ox.connect(wal[i][0]),reverse.ox.connect(wal[i][1])]for i in range(len(par))]
	return [ik,fk,sk,md.ox,reverse.ox]
#ikfkRig 建立ikfk切换绑定自动建立ikfk关节,ikfkRig（切换控制器，控制属性，控制属性乘以一个数值，关节列表）
def ikfkRig(con,attr,zoomCon,Jin):
	if type(Jin)!=list:
		Jin = [Jin]
	Jin = [pm.general.PyNode(i) for i in Jin]
	attr = pm.general.PyNode(con+'.'+attr)
	ik = pm.duplicate(Jin)
	fk = pm.duplicate(Jin)
	ik = [pm.rename(ik[i],'Ik_'+Jin[i].split('|')[-1]) for i in range(len(Jin))]
	fk = [pm.rename(fk[i],'Fk_'+Jin[i].split('|')[-1]) for i in range(len(Jin))]
	sk = [pm.rename(Jin[i],'Sk_'+Jin[i].split('|')[-1]) for i in range(len(Jin))]
	
	par = [pm.parentConstraint((ik[i],fk[i]),sk[i]) for i in range(len(ik))]
	wal = [pm.parentConstraint(i , q = 1 , wal = 1) for i in par]
	md = pm.createNode('multiplyDivide',n=sk[0]+'_multiplyDivide_Ikfk')
	attr.connect(md.input1X)
	md.input2X.set(zoomCon)
	reverse = pm.createNode('reverse',n=sk[0]+'_reverse_Ikfk')
	md.ox.connect(reverse.ix)
	[[md.ox.connect(wal[i][0]),reverse.ox.connect(wal[i][1])]for i in range(len(par))]
	return [ik,fk,sk,md.ox,reverse.ox]
#建立ik拉伸绑定需要的属性
def ikStretchAddAttr(con):
	pm.addAttr(con,ln = 'Stretch' , at = 'float' , min = 0 , max = 10 , dv = 0 , k = 1)
	pm.addAttr(con,ln = 'StretchMax' , at = 'float' , min = 1 , dv = 10 , k = 1)
	pm.addAttr(con,ln = 'StretchMin' , at = 'float' , min = 0.1  , dv = 1 , k = 1)
	return 0
#完成ik拉伸绑定输入ik控制器，关节列表，拉伸控制属性，拉伸最小值控制属性，拉伸最大值控制属性返回拉伸定位器组，拉伸定位器开始拉伸定位器结束，关节缩放控制属性（函数中并没有链接上）
def ikStretch(con,JointList,attr,attrMin,attrMax):
	if type(JointList)!=list:
		pm.error('错误输入的不是列表')
	con = pm.general.PyNode(con)
	JointList = [pm.general.PyNode(i) for i in JointList]
	attr = pm.general.PyNode(con+'.'+attr)
	attrMin = pm.general.PyNode(con+'.'+attrMin)
	attrMax = pm.general.PyNode(con+'.'+attrMax)
	
	length = 0
	for i in JointList[1:]:
		length=length+abs(i.tx.get())
	
	
	loc = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_Strtch')
	locEnd = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_StrtchEnd')
	pm.pointConstraint(JointList[0],loc)
	pm.pointConstraint(con,locEnd)
	grp = pm.group(em=1,n=JointList[0].split('|')[-1]+'_StrtchGrp')
	pm.parent((loc,locEnd),grp)
	#(loc,locEnd),
	dis = pm.createNode('distanceBetween',n=JointList[0].split('|')[-1]+'_dis')
	loc.t.connect(dis.p1)
	locEnd.t.connect(dis.p2)
	
	mD = pm.createNode('multiplyDivide',n=JointList[0].split('|')[-1]+'_multiplyDivide')
	mD.operation.set(2)
	mD.i1.set((1,1,1))
	mD.i2.set((1,10,1))
	dis.d.connect(mD.i1x)
	mD.i2x.set(length)
	
	Cmp = pm.createNode('clamp',n=JointList[0].split('|')[-1]+'_Cmp')
	
	mD.ox.connect(Cmp.ipr)
	
	attrMin.connect(Cmp.mnr)
	attrMax.connect(Cmp.mxr)
	
	
	bC = pm.createNode('blendColors',n=JointList[0].split('|')[-1]+'_BlendColors')
	bC.c2.set((1,1,1))
	Cmp.opr.connect(bC.c1r)
	attr.connect(mD.i1y)
	mD.oy.connect(bC.blender)
	return [grp,loc,locEnd,bC.opr]
#添加肘部锁定绑定需要的属性
def ikLockingAddAttr(con):
	pm.addAttr(con,ln = 'locking' , at = 'float' , min = 0 , max = 10 , dv = 0 , k = 1)
	return 0
#自动建立ik绑定输入ik控制器，极向量控制器，关节列表（3个），肘部锁定控制属性，拉伸控制属性，拉伸最小值控制属性，拉伸最大值控制属性，返回距离计算定位器组
def ikLocking(con,locking,JointList,attr,Stretch,Stretchmin,Stretchmax):
	if type(JointList)!=list:
		pm.error('错误输入的不是列表')
	if len(JointList)!=3:
		pm.error('输入的不是三个关节')
	con = pm.general.PyNode(con)
	locking = pm.general.PyNode(locking)
	JointList = [pm.general.PyNode(i) for i in JointList]
	attr = pm.general.PyNode(locking+'.'+attr)
		
	locToEnd = ikStretch(con,JointList,Stretch,Stretchmin,Stretchmax)
	StretchOut = locToEnd[3]
	
	loc = locToEnd[1]
	locLocking = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_StrtchLocking')
	locEnd = locToEnd[2]
	pm.pointConstraint(locking,locLocking)
	grp = locToEnd[0]
	pm.select(grp)
	pm.parent(locLocking,grp)
	
	dis1 = pm.createNode('distanceBetween',n=JointList[0].split('|')[-1]+'_dis1')
	loc.t.connect(dis1.p1)
	locLocking.t.connect(dis1.p2)
	dis2 = pm.createNode('distanceBetween',n=JointList[0].split('|')[-1]+'_dis2')
	locLocking.t.connect(dis2.p1)
	locEnd.t.connect(dis2.p2)
	
	mD = pm.createNode('multiplyDivide',n=JointList[0].split('|')[-1]+'_multiplyDivide')
	mD.operation.set(2)
	
	dis1.d.connect(mD.i1x)
	mD.i2x.set(abs(JointList[1].tx.get()))
	
	dis2.d.connect(mD.i1y)
	mD.i2y.set(abs(JointList[2].tx.get()))
	
	attr.connect(mD.i1z)
	mD.i2z.set(10)
	
	bC = pm.createNode('blendColors',n=JointList[0].split('|')[-1]+'_BlendColors')
	mD.ox.connect(bC.c1r)
	mD.oy.connect(bC.c1g)
	mD.oz.connect(bC.blender)
	StretchOut.connect(bC.c2r)
	StretchOut.connect(bC.c2g)
	
	bC.opr.connect(JointList[0].sx)
	bC.opg.connect(JointList[1].sx)
	return grp

#自动建立ik绑定输入关节列表（3个），ik控制器，极向量控制器，返回距离计算定位器组
def ikStrtchRig(JointList,con,locking):
	if type(JointList)!=list:
		pm.error('错误输入的不是列表')
	if len(JointList)!=3:
		pm.error('输入的不是三个关节')
	JointList = [pm.general.PyNode(i) for i in JointList]
	con = pm.general.PyNode(con)
	locking = pm.general.PyNode(locking)
	
	ikStretchAddAttr(con)
	ikLockingAddAttr(locking)
	
	return ikLocking(con,locking,JointList,'locking','Stretch','StretchMin','StretchMax')
#建立fk绑定输入关节列表输出最顶层绑定组提供标示符colour=颜色，Scale=大小
def fkRig(JointList,**S):
	print 1
	if type(JointList)!=list:
		JointList = [JointList]
	JointList = [pm.general.PyNode(i) for i in JointList]
	fkCon=[]
	fkGrp=[]
	fkKeyGrp=[]
	print 2
	for i in JointList:
		cir = pm.circle(ch=0,o=1,nr=(1,0,0),r=1,n=i.split('|')[-1]+'Con')[0]
		if 'colour' in S:
			CreateCon.CvColour(cir,S['colour'])
		if 'Scale' in S:
			CreateCon.scaleCon(cir,S['Scale'])
		grp = pm.group(cir,n=cir.split('|')[-1]+'Grp')
		keyGrp = pm.group(cir,n=cir.split('|')[-1]+'GrpKey')
		pm.delete(pm.parentConstraint(i,grp))
		pm.parentConstraint(cir,i)
		fkCon.append(cir)
		fkKeyGrp.append(keyGrp)
		fkGrp.append(grp)
	if len(JointList)>1:
		pm.addAttr(fkCon[-1],ln = 'rotx' , at = 'float'  , dv = 0 , k = 1)
		pm.addAttr(fkCon[-1],ln = 'roty' , at = 'float'  , dv = 0 , k = 1)
		pm.addAttr(fkCon[-1],ln = 'rotz' , at = 'float'  , dv = 0 , k = 1)
		for i in fkKeyGrp:
			fkCon[-1].rotx.connect(i.rx)
			fkCon[-1].roty.connect(i.ry)
			fkCon[-1].rotz.connect(i.rz)
		for i in range(len(fkCon))[1:]:
			pm.parent(fkGrp[i],fkCon[i-1])
	return [fkGrp[0],fkCon,fkKeyGrp,fkGrp]
#创建ik绑定需要的控制器和属性输入关节列表和是否为对象空间
def ikConAttr(JointList,w):
	#JointList = pm.selected()#关节列表
	#w = 0#ik控制器是否为对象空间
	if len(JointList)<3:
		pm.error('sr输入的关节不是三个')
	
	Scale = abs(JointList[1].tx.get())/10/2#控制器对象
	#创建ikfk切换控制器
	cir = pm.circle(ch=0,o=1,nr=(1,0,0),r=3,n=JointList[0].split('|')[-1]+'Ikfk')[0]
	CreateCon.CvColour(cir,4)
	pm.select(cir.cv[::2],r=1)
	pm.scale((0.5,0.5,0.5))
	pm.select(cir.cv,r=1)
	pm.scale((Scale,Scale,Scale))
	grp = pm.group(cir,n=cir.split('|')[-1]+'Grp')
	pm.delete(pm.parentConstraint(JointList[-1],grp))
	cir.ty.set(Scale*10)
	cir.tx.set(lock=1,channelBox=0,keyable=0)
	cir.ty.set(lock=1,channelBox=0,keyable=0)
	cir.tz.set(lock=1,channelBox=0,keyable=0)
	cir.rx.set(lock=1,channelBox=0,keyable=0)
	cir.ry.set(lock=1,channelBox=0,keyable=0)
	cir.rz.set(lock=1,channelBox=0,keyable=0)
	cir.sx.set(lock=1,channelBox=0,keyable=0)
	cir.sy.set(lock=1,channelBox=0,keyable=0)
	cir.sz.set(lock=1,channelBox=0,keyable=0)
	ikfkAddAttr(cir)
	#创建ik控制器
	ikCon = CreateCon.Con1(colour = 13 ,Scale = Scale*10,n=JointList[0].split('|')[-1]+'IkCon')
	ikgrp = pm.group(ikCon,n=ikCon.split('|')[-1]+'Grp')
	if w ==0:
		pm.delete(pm.pointConstraint(JointList[2],ikgrp))
	else:
		pm.delete(pm.parentConstraint(JointList[2],ikgrp))
	ikCon.sx.set(lock=1,channelBox=0,keyable=0)
	ikCon.sy.set(lock=1,channelBox=0,keyable=0)
	ikCon.sz.set(lock=1,channelBox=0,keyable=0)
	#创建极向量控制器位置
	loc = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_loc')
	loc1 = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_loc1')
	pm.delete(pm.pointConstraint((JointList[0],JointList[2]),loc))
	pm.delete(pm.pointConstraint(JointList[1],loc1))
	pm.delete(pm.aimConstraint(loc1,loc))
	pm.parent(loc1,loc)
	loc1.t.set(loc1.t.get()*2)
	polarVector = pm.xform(loc1,q=1,ws=1,t=1)
	pm.delete(loc)
	
	#创建极向量控制器
	poler = CreateCon.Con3(colour = 13 ,Scale = Scale*10,n=JointList[0].split('|')[-1]+'IkpolerCon')
	polergrp = pm.group(poler,n=poler.split('|')[-1]+'Grp')
	polergrp.t.set(polarVector)
	poler.rx.set(lock=1,channelBox=0,keyable=0)
	poler.ry.set(lock=1,channelBox=0,keyable=0)
	poler.rz.set(lock=1,channelBox=0,keyable=0)
	poler.sx.set(lock=1,channelBox=0,keyable=0)
	poler.sy.set(lock=1,channelBox=0,keyable=0)
	poler.sz.set(lock=1,channelBox=0,keyable=0)
	#
	ikStretchAddAttr(ikCon)
	ikLockingAddAttr(poler)
	return ((ikCon,poler,cir),(ikgrp,polergrp,grp))
#创建ikfk绑定输入关节列表，是否约束旋转，是否为对象空间
def ikfkSwitchRig(JointList,par,w):
	#JointList = pm.selected()#关节列表
	#w = 0#ik控制器是否为对象空间
	if len(JointList)<3:
		pm.error('sr输入的关节不是三个')
	
	Scale = abs(JointList[1].tx.get())/10/2#控制器对象
	#创建ikfk切换控制器
	cir = pm.circle(ch=0,o=1,nr=(1,0,0),r=3,n=JointList[0].split('|')[-1]+'Ikfk')[0]
	CreateCon.CvColour(cir,4)
	pm.select(cir.cv[::2],r=1)
	pm.scale((0.5,0.5,0.5))
	pm.select(cir.cv,r=1)
	pm.scale((Scale,Scale,Scale))
	grp = pm.group(cir,n=cir.split('|')[-1]+'Grp')
	pm.parentConstraint(JointList[-1],grp)
	cir.ty.set(Scale*10)
	cir.tx.set(lock=1,channelBox=0,keyable=0)
	cir.ty.set(lock=1,channelBox=0,keyable=0)
	cir.tz.set(lock=1,channelBox=0,keyable=0)
	cir.rx.set(lock=1,channelBox=0,keyable=0)
	cir.ry.set(lock=1,channelBox=0,keyable=0)
	cir.rz.set(lock=1,channelBox=0,keyable=0)
	cir.sx.set(lock=1,channelBox=0,keyable=0)
	cir.sy.set(lock=1,channelBox=0,keyable=0)
	cir.sz.set(lock=1,channelBox=0,keyable=0)
	ikfkAddAttr(cir)
	#创建ik控制器
	ikCon = CreateCon.Con1(colour = 13 ,Scale = Scale*10,n=JointList[0].split('|')[-1]+'IkCon')
	ikgrp = pm.group(ikCon,n=ikCon.split('|')[-1]+'Grp')
	if w ==0:
		pm.delete(pm.pointConstraint(JointList[2],ikgrp))
	else:
		pm.delete(pm.parentConstraint(JointList[2],ikgrp))
	ikCon.sx.set(lock=1,channelBox=0,keyable=0)
	ikCon.sy.set(lock=1,channelBox=0,keyable=0)
	ikCon.sz.set(lock=1,channelBox=0,keyable=0)
	#创建极向量控制器位置
	loc = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_loc')
	loc1 = pm.spaceLocator(n=JointList[0].split('|')[-1]+'_loc1')
	pm.delete(pm.pointConstraint((JointList[0],JointList[2]),loc))
	pm.delete(pm.pointConstraint(JointList[1],loc1))
	pm.delete(pm.aimConstraint(loc1,loc))
	pm.parent(loc1,loc)
	loc1.t.set(loc1.t.get()*2)
	polarVector = pm.xform(loc1,q=1,ws=1,t=1)
	pm.delete(loc)
	
	#创建极向量控制器
	poler = CreateCon.Con3(colour = 13 ,Scale = Scale*10,n=JointList[0].split('|')[-1]+'IkpolerCon')
	polergrp = pm.group(poler,n=poler.split('|')[-1]+'Grp')
	polergrp.t.set(polarVector)
	poler.rx.set(lock=1,channelBox=0,keyable=0)
	poler.ry.set(lock=1,channelBox=0,keyable=0)
	poler.rz.set(lock=1,channelBox=0,keyable=0)
	poler.sx.set(lock=1,channelBox=0,keyable=0)
	poler.sy.set(lock=1,channelBox=0,keyable=0)
	poler.sz.set(lock=1,channelBox=0,keyable=0)
	#为ik控制器极向量控制器打组
	ikConGrp = pm.group((ikgrp,polergrp),n=JointList[0].split('|')[-1]+'IkTotalConGrp')
	#创建ikfk关节和ikfk切换绑定
	ikfkJoint = ikfkRig(cir,'ikfk',0.1,JointList)
	#创建ik控制手柄
	pm.select((ikfkJoint[0][0],ikfkJoint[0][2]),r=1)
	ikHandle = pm.ikHandle(sol='ikRPsolver')[0]
	ikHandle.v.set(0)
	cir.v.set(lock=1,channelBox=0,keyable=0)
	#创建IkHandle和距离计算定位器组
	IkHandleDisGrp = pm.group(em=1,n=JointList[0].split('|')[-1]+'IkHandleDisGrp')
	#约束ik
	pm.parentConstraint(ikCon,ikHandle)
	pm.poleVectorConstraint(poler,ikHandle)
	#绑定ik
	ikStretchGrp = ikStrtchRig(ikfkJoint[0][0:3],ikCon,poler)
	ikStretchGrp.v.set(0)
	cir.v.set(lock=1,channelBox=0,keyable=0)
	#将ik距离计算定位器组和ikHandle给IkHandle和距离计算定位器组
	pm.parent((ikStretchGrp,ikHandle),IkHandleDisGrp)
	#绑定fk
	fkGrp = fkRig(ikfkJoint[1],colour=14,Scale=Scale*5)
	#隐藏显示控制器
	ikfkJoint[3].connect(ikConGrp.v)
	ikfkJoint[4].connect(fkGrp[0].v)
	#
	if par!=0:
		rotGrp = pm.group(em=1,n=ikCon.split('|')[-1]+'rotGrp')
		pm.parent(rotGrp,ikCon)
		pm.delete(pm.parentConstraint(ikfkJoint[0][2],rotGrp))
		pm.orientConstraint(rotGrp,ikfkJoint[0][2],mo=1)
		rotGrp.tx.set(lock=1,channelBox=0,keyable=0)
		rotGrp.ty.set(lock=1,channelBox=0,keyable=0)
		rotGrp.tz.set(lock=1,channelBox=0,keyable=0)
		rotGrp.rx.set(lock=1,channelBox=0,keyable=0)
		rotGrp.ry.set(lock=1,channelBox=0,keyable=0)
		rotGrp.rz.set(lock=1,channelBox=0,keyable=0)
		rotGrp.sx.set(lock=1,channelBox=0,keyable=0)
		rotGrp.sy.set(lock=1,channelBox=0,keyable=0)
		rotGrp.sz.set(lock=1,channelBox=0,keyable=0)
		rotGrp.v.set(lock=1,channelBox=0,keyable=0)
	return [ikfkJoint[0],ikfkJoint[1],ikfkJoint[2],fkGrp,ikConGrp,IkHandleDisGrp,grp]
#import pymel.core as pm
#建立样条ik拉伸绑定
def SplineIkStretch(JointList,con,Curve):
	CurveBase = pm.duplicate(Curve,rr=1,n=Curve+'Base')
	pm.addAttr(con,ln = 'VolumeRetention' , at = 'float' , min = 0 , max = 10 , dv = 0 , k = 1)
	
	curveInfo = pm.arclen(Curve,ch=1)
	curveInfoBase = pm.arclen(CurveBase,ch=1)
	
	multiplyDivide = pm.shadingNode('multiplyDivide',asUtility=1,n=Curve.split('|')[-1]+'MultiplyDivide')
	multiplyDivide.operation.set(2)
	curveInfo.arcLength.connect(multiplyDivide.i1x)
	curveInfoBase.arcLength.connect(multiplyDivide.i2x)
	
	multiplyDivide2 = pm.shadingNode('multiplyDivide',asUtility=1,n=Curve.split('|')[-1]+'MultiplyDivideStter')
	multiplyDivide2.operation.set(2)
	multiplyDivide2.i1.set((1,1,1))
	multiplyDivide2.i2.set((1,10,1))
	multiplyDivide.ox.connect(multiplyDivide2.i2x)
	con.VolumeRetention.connect(multiplyDivide2.i1y)
	
	blendColors = pm.shadingNode('blendColors',asUtility=1,n=Curve.split('|')[-1]+'blendColors')
	multiplyDivide2.oy.connect(blendColors.blender)
	
	blendColors.color1.set((1,1,1))
	blendColors.color2.set((1,1,1))
	multiplyDivide.ox.connect(blendColors.color1R)
	multiplyDivide2.ox.connect(blendColors.color1G)
	multiplyDivide2.ox.connect(blendColors.color1B)
	multiplyDivide.ox.connect(blendColors.color2R)
	
	
	#[blendColors.op.connect(i.s) for i in JointList[0:-1]]
	return (Curve,CurveBase[0],blendColors.op)
def NOStretchCon(jin,con,curve):
	#jin = pm.selected()
	#con = pm.selected()[0]
	#curve = pm.selected()[0]
	Curve,CurveBase,outS = SplineIkStretch(jin,con,curve)
	[outS.connect(i.s) for i in jin]
	return (Curve,CurveBase)
