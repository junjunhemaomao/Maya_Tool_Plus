#!/usr/bin/python
#encoding:gbk
import pymel.core as pm
import maya.api.OpenMaya as om

maya_useNewAPI = True
def getClosestPoint(obj,mesh):
	#obj = pm.selected()[0]
	
	#mesh = pm.selected()[0]
	
	
	obj=str(obj)
	mesh = str(mesh)
	
	pos = pm.xform(obj,q=1,ws=1,t=1)
	objPos = om.MPoint(pos[0],pos[1],pos[2])
	
	selList = om.MSelectionList()
	selList.add(mesh)
	
	fnMesh = om.MFnMesh(selList.getDagPath(0))
	
	objPos = fnMesh.getClosestPoint(objPos,om.MSpace.kWorld)[0]
	return (objPos[0],objPos[1],objPos[2])
