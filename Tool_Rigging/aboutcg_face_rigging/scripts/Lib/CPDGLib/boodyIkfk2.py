#!/usr/bin/python
# encoding:gbk
# 作者：张隆鑫
# 完成时间:2019.11.5
# 最近修改时间:2019.11.7
"""
本模块为boody绑定提供ikfk功能函数集2.0
"""
import pymel.core as pm
import Cangphantom
import Cangphantom.Lib.CPDGLib.Matrix as matrix#矩阵控制模块
import Cangphantom.Lib.CPDGLib.constraintSwitch as constraintSwitch
import Cangphantom.Lib.CPMath as cmath  # 自定义数学库
import Cangphantom.Lib.CPDGLib.boodyIkfk as boodyIkfk  # ikfk功能集
import Cangphantom.Lib.CPFnCreateCon as fnCreateCon


#
def getObjDis(objStart, objEnd):
    start = pm.xform(objStart, q=True, t=True, ws=True)
    End = pm.xform(objEnd, q=True, t=True, ws=True)
    return cmath.dis(start, End)


# 建立ikfk切换绑定需要的属性
def ikfkAddAttr(con):
    pm.addAttr(con, ln='ikfk', at='float', min=0, max=10, dv=0, k=1)
    return 0


# 建立ik拉伸绑定需要的属性
def ikStretchAddAttr(con):
    pm.addAttr(con, ln='Stretch', at='float', min=0, max=10, dv=0, k=1)
    pm.addAttr(con, ln='StretchMax', at='float', min=1, dv=10, k=1)
    pm.addAttr(con, ln='StretchMin', at='float', min=0.1, dv=1, k=1)
    return 0


# 添加肘部跟随绑定需要的属性
def ikFollowAddAttr(con):
    pm.addAttr(con, ln='follow', sn='follow', at=float, min=0.0, max=10.0, dv=0.0, k=1)
    return 0


# 添加肘部锁定绑定需要的属性
def ikLockingAddAttr(con):
    pm.addAttr(con, ln='locking', at='float', min=0, max=10, dv=0, k=1)
    return 0


# 添加fk整体旋转控制属性
def addAttrFkRoot(fkCon):
    pm.addAttr(fkCon, ln='rotx', at='float', dv=0, k=1)
    pm.addAttr(fkCon, ln='roty', at='float', dv=0, k=1)
    pm.addAttr(fkCon, ln='rotz', at='float', dv=0, k=1)

# 获得ik绑定的控制器位置(关节列表,全局缩放)
def getIkLok(jointList, globalScale=1):
    start = pm.xform(jointList[0], q=True, t=True, ws=True)
    End = pm.xform(jointList[-1], q=True, t=True, ws=True)
    temporaryLoc = pm.spaceLocator()
    pos = [(a + b) / 2 for a, b in zip(start, End)]
    pm.xform(temporaryLoc, t=pos, ws=True)
    pm.delete(pm.aimConstraint(jointList[-1], temporaryLoc))

    temporaryLocList = [pm.spaceLocator() for i in jointList]
    [pm.xform(i, t=pm.xform(t, q=True, t=True, ws=True), ws=True) for i, t in zip(temporaryLocList, jointList)]

    pm.parent(temporaryLocList, temporaryLoc)

    XYdisList = [(abs(i.ty.get()) + abs(i.tz.get()), i) for i in temporaryLocList]
    XYdisList.sort(key=lambda x: x[0])

    XYdisList[-1][1].tx.set(0)
    globalScale = getObjDis(jointList[0], jointList[-1]) / getObjDis(temporaryLoc, XYdisList[-1][1]) + globalScale

    XYdisList[-1][1].ty.set(XYdisList[-1][1].ty.get() * globalScale)
    XYdisList[-1][1].tz.set(XYdisList[-1][1].tz.get() * globalScale)
    pole_vectot = pm.xform(XYdisList[-1][1], q=True, ws=True, t=True)
    pm.delete(temporaryLoc)
    return (start, pole_vectot, End)

# 建立基本的ik绑定(关节列表，是否约束旋转，全局大小)
def Ik_simple_binding(jointList, rootIf=True, globalScale=1):
    # jointList = pm.selected()
    rootIf = True
    globalScale = globalScale * 2

    otherGrp = pm.group(n=jointList[0].nodeName() + 'otherGrp', em=True)
    # help(fnCreateCon)
    # fnCreateCon.getColour(pm.selected())
    # ik开始控制器
    IkStart = fnCreateCon.Con6(n=jointList[0].nodeName() + 'IkStartCon', colour=17, Scale=globalScale)
    pm.rotate(IkStart.cv, (0, 90, 0))
    IkStartGrp = pm.group(IkStart, n=IkStart.nodeName() + 'Grp')
    if rootIf:
        pm.delete(pm.parentConstraint(jointList[0], IkStartGrp))
    # ik控制器
    IkCon = fnCreateCon.Con2(n=jointList[0].nodeName() + 'IkCon', colour=13, Scale=globalScale)
    IkConGrp = pm.group(IkCon, n=IkCon.nodeName() + 'Grp')
    if rootIf:
        pm.delete(pm.parentConstraint(jointList[-1], IkConGrp))
    # ik极向量控制器
    PolarVectorCon = fnCreateCon.Con3(n=jointList[0].nodeName() + 'PolarVectorCon', colour=13, Scale=globalScale)
    PolarVectorConGrp = pm.group(PolarVectorCon, n=PolarVectorCon.nodeName() + 'Grp')
    if rootIf:
        pm.delete(pm.parentConstraint(jointList[0], PolarVectorConGrp))
    # ik控制器定位
    startPos, poleVectotPos, EndPos = getIkLok(jointList)

    pm.xform(IkStartGrp, t=startPos, ws=True)
    pm.xform(PolarVectorConGrp, t=poleVectotPos, ws=True)
    pm.xform(IkConGrp, t=EndPos, ws=True)

    pm.select(jointList[0], jointList[-1], r=True)

    ikHandle = pm.ikHandle()[0]

    ikHandle.v.set(0, lock=True)

    pm.parent(ikHandle, IkCon)

    pm.poleVectorConstraint(PolarVectorCon, ikHandle, weight=1)

    pm.pointConstraint(IkStart, jointList[0])

    pm.select(cl=True)
    Polar_vector_follow_jointList = [
        pm.joint(n=i.nodeName() + 'Polar_vector_follow_joint', p=pm.xform(i, q=True, ws=True, t=True)) for i in
        (IkStart, IkCon)]
    pm.joint(Polar_vector_follow_jointList, e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    pm.select(Polar_vector_follow_jointList[0], Polar_vector_follow_jointList[-1], r=True)
    Polar_vector_follow_ikH = pm.ikHandle(sol='ikSCsolver')[0]
    Polar_vector_follow_ikH.v.set(0, lock=True)
    pm.parent(Polar_vector_follow_ikH, IkCon)
    pm.parent(Polar_vector_follow_jointList[0], otherGrp)
    pm.pointConstraint(IkStart, Polar_vector_follow_jointList[0])
    [i.v.set(0, lock=True) for i in Polar_vector_follow_jointList]

    constraintSwitch.Polar_vector_switch(PolarVectorCon, otherGrp, Polar_vector_follow_jointList[0], PolarVectorConGrp,
                                         10, True)
    return (IkStartGrp , PolarVectorConGrp , IkConGrp , IkStart , PolarVectorCon , IkCon , otherGrp)
#IkStartGrp, PolarVectorConGrp, IkConGrp,IkStart, PolarVectorCon, IkCon, otherGrp = Ik_simple_binding(pm.selected())
#获得拉伸的位置矩阵输出开始默认位置，结束默认位置，开始距离位置，结束距离位置
def getStretchPos(IkStartGrp,IkConGrp,IkStart,IkCon):
    #开始结束距离计算矩阵
    startMatrix = matrix.getWorldMatrix(n=IkStart.nodeName())
    endMatrix = matrix.getWorldMatrix(n=IkCon.nodeName())
    startMatrix.inplus(IkStart)
    endMatrix.inplus(IkCon)
    #开始结束默认矩阵
    startDefaultMatrix = matrix.getWorldMatrix(n=IkStartGrp.nodeName())
    endDefaultMatrix = matrix.getWorldMatrix(n=IkConGrp.nodeName())
    startDefaultMatrix.inplus(IkStartGrp)
    endDefaultMatrix.inplus(IkConGrp)
    return (startDefaultMatrix,endDefaultMatrix,startMatrix,endMatrix)
#help(matrix)
getStretchPos(IkStartGrp,IkConGrp,IkStart,IkCon)
