#!/usr/bin/python
#encoding:gbk
#本模块实现了一些pm命令的拆包
#使用本模块应该使用from mod import *
import pymel.core as pm
sel = pm.selected
liR = pm.listRelatives
liC = pm.listConnections
lia = pm.listAttr

parent = pm.parent
group = pm.group
delete = pm.delete
xform = pm.xform

tCon = pm.pointConstraint
rCon = pm.orientConstraint
sCon = pm.scaleConstraint
parCon = pm.parentConstraint
aimCon = pm.aimConstraint
polyPt = pm.pointOnPolyConstraint
geoCon = pm.geometryConstraint
norCon = pm.normalConstraint
tangCon = pm.tangentConstraint


ls = pm.ls
node = pm.createNode
name = pm.rename
joint = pm.joint

skp = pm.skinPercent
skc = pm.skinCluster
skb = pm.skinBindCtx

ik = pm.ikHandle

def getName(obj):
	return str(obj.split('|')[-1])