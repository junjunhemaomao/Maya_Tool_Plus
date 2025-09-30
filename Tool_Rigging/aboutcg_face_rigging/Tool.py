# -*- coding: utf-8 -*-

import pymel.core as pm

#在点上创建骨骼
#是一个方便的可选项，并不强求骨骼每次都在点上
def create_joints_at_vertices():
    sel = pm.selected(fl=True)
    for i in sel:
        pm.select(cl=True)
        pm.joint(p=pm.xform(i,q=True,t=True,ws=True))
create_joints_at_vertices()

#镜像骨骼前注意前缀的名称需要有前缀
def mirror_left_joints():
    selected = pm.ls('l_*', type='joint')
    for s in selected:
        pm.select(s, replace=True)
        pm.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("l", "r"))
