import maya.cmds as cmds
import pymel.core as pm

sel = pm.selected()
edge_to_curve = pm.PyNode("polyEdgeToCurve1")
mesh = pm.PyNode("face")

mesh_shape = mesh.getShape()
closestPointOnMesh = pm.createNode("closestPointOnMesh")
mesh_shape.outMesh >> closestPointOnMesh.inMesh

mesh_ids = list()

for i in sel:
    pos = pm.xform(i, q = True, t = True, ws = True)
    closestPointOnMesh.ip.set(pos)
    
    mesh_ids.append(closestPointOnMesh.vt.get())
pm.delete(closestPointOnMesh)

cmds.setAttr(str(edge_to_curve.ics), len(mesh_ids), *["vtx[%d]"%i for i in mesh_ids], type = "componentList")

for ID, i in enumerate(mesh_ids):
    obj = sel[ID]
    pointOnCurveInfo = pm.createNode("pointOnCurveInfo", n = "pointOnCurveInfo_" + obj.nodeName())
    
    edge_to_curve.outputcurve >> pointOnCurveInfo.inputCurve
    pointOnCurveInfo.parameter.set(ID)
    
    composeMatrix = pm.createNode("composeMatrix", n = "composeMatrix_" + obj.nodeName())
    pointOnCurveInfo.position >> composeMatrix.inputTranslate
    
    multMatrix = pm.createNode("multMatrix", n = "multMatrix_" + obj.nodeName())
    composeMatrix.outputMatrix >> multMatrix.matrixIn[0]
    obj.parentInverseMatrix[0] >> multMatrix.matrixIn[1]
    
    decomposeMatrix = pm.createNode("decomposeMatrix", n = "decomposeMatrix_" + obj.nodeName())
    multMatrix.matrixSum >> decomposeMatrix.inputMatrix
    
    decomposeMatrix.outputTranslate >> obj.translate;