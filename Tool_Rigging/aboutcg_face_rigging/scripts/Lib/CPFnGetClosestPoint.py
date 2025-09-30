#!/usr/bin/python
#encoding:gbk
#对象最近点功能类模块
import pymel.core as pm
import maya.api.OpenMaya as om

maya_useNewAPI = True
#模型最近点类效率优先需要先初始化模型
class mesh:
    '''
    __init__(self,curve)#初始化
    closestPoint(self,obj)#查找最近点
    '''
    def __init__(self,mesh):
        mesh = str(mesh)
        self.selList = om.MSelectionList()
        self.selList.add(mesh)
        
        self.fnMesh = om.MFnMesh(self.selList.getDagPath(0))
    def closestPoint(self,obj):
        #obj = pm.selected()[0]
        #mesh = pm.selected()[0]
        obj=str(obj)
        pos = pm.xform(obj,q=1,ws=1,t=1)
        objPos = om.MPoint(*pos)
        
        objUv = self.fnMesh.getUVAtPoint(objPos,om.MSpace.kWorld)[0:-1]
        objPos = self.fnMesh.getClosestPoint(objPos,om.MSpace.kWorld)[0]
        return ((objPos[0],objPos[1],objPos[2]),objUv)
#曲线最近点类效率优先需要先初始化曲线
class curve:
    '''
    __init__(self,curve)#初始化
    closestPoint(self,obj)#查找最近点
    pointAtParam(self,U)#查询曲线上的点
    '''
    def __init__(self,curve):
        curve = str(curve)
        selList = om.MSelectionList()
        selList.add(curve)
        self.fnCurve = om.MFnNurbsCurve(selList.getDagPath(0))
    def closestPoint(self,obj):
        #obj = pm.selected()[0]
        
        #curve = pm.selected()[0]
        obj=str(obj)
        pos = pm.xform(obj,q=1,ws=1,t=1)
        objPos = om.MPoint(*pos)
        
        objPos = self.fnCurve.closestPoint(objPos,0.0001,om.MSpace.kWorld)
        return ((objPos[0][0],objPos[0][1],objPos[0][2]),objPos[1])
    def pointAtParam(self,U):
        objPos = self.fnCurve.getPointAtParam(U,om.MSpace.kWorld)
        return (objPos[0],objPos[1],objPos[2])
#曲面最近点类效率优先需要先初始化曲面
class nurbs:
    '''
    __init__(self,curve)#初始化
    closestPoint(self,obj)#查找最近点
    pointAtParam(self,U,V)#查询曲面上的点
    '''
    def __init__(self,nurbs):
        nurbs = str(nurbs)
        self.selList = om.MSelectionList()
        self.selList.add(nurbs)
        self.fnNurbs = om.MFnNurbsSurface(self.selList.getDagPath(0))
    def closestPoint(self,obj):
        #obj = pm.selected()[0]
        #nurbs = pm.selected()[0]
        obj=str(obj)
        pos = pm.xform(obj,q=1,ws=1,t=1)
        objPos = om.MPoint(*pos)
        objPos = self.fnNurbs.closestPoint(objPos,False,0.0001,om.MSpace.kWorld)
        return ((objPos[0][0],objPos[0][1],objPos[0][2]),(objPos[1],objPos[2]))
    def pointAtParam(self,U,V):
        objPos = self.fnNurbs.getPointAtParam(U,V,om.MSpace.kWorld)
        return (objPos[0],objPos[1],objPos[2])
