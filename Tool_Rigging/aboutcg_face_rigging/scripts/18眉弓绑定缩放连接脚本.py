#!/usr/bin/python
#encoding:gbk
#对象最近点功能类模块
import pymel.core as pm
decomposeMatrix = pm.PyNode("decomposeMatrix1")
multiplyDivide = pm.PyNode("multiplyDivide4")
sel = pm.selected()
for i in sel:
    if pm.xform(i, q = True, t = True, ws = True)[0] < -0.01:
        multiplyDivide.outputX >> i.scaleX;
        decomposeMatrix.outputScaleY >> i.scaleY;
        decomposeMatrix.outputScaleZ >> i.scaleZ;
    else:
        decomposeMatrix.outputScale >> i.scale;


import pymel.core as pm
sel = pm.selected(fl=True)
for i in  sel:
    pm.select(cl=True)
    pm.joint(p=pm.xform(i,q=True,t=True,ws=True))