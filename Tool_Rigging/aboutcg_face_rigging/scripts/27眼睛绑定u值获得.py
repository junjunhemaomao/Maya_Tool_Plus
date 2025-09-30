#!/usr/bin/python
#encoding:gbk
#对象最近点功能类模块
import pymel.core as pm
import maya.api.OpenMaya as om
import CPMel.math as math

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

min_size = 0.001
size_v = 0.01
FORMAXSIZE = 100


#curve = pm.PyNode("curve1")
#con_curve = pm.PyNode("curveShape2")

def getPathClosestPoint(obj, con_curve):
    #(1.7618908086321845, -2.1188558922505734, 0.0)
    #obj = curve.cv[5]
    fn_curve = curve()
    closepos,u = fn_curve.closestPoint(obj)
    u = float(u)/con_curve.max.get()
    path_node = pm.createNode("motionPath")
    con_curve.worldSpace[0] >> path_node.geometryPath
    path_node.fractionMode.set(True)
    path_node.uValue.set(u)
    
    
    up_dis = 999999999999999999
    for _ in range(FORMAXSIZE):
        lise_u = u - size_v
        add_u = u + size_v
        
        path_node.uValue.set(lise_u)
        lise_dis = math.dis(closepos, tuple(path_node.allCoordinates.get()))
        
        path_node.uValue.set(add_u)
        add_dis = math.dis(closepos, tuple(path_node.allCoordinates.get()))
        
        if add_dis > up_dis and lise_dis > up_dis:
            size_v = size_v * 0.5
            continue
        if add_dis < up_dis:
            u = add_u
            up_dis = add_dis
            continue
        if lise_dis < up_dis:
            u = lise_u
            up_dis = lise_dis
            continue
    pm.delete(path_node)
    return u