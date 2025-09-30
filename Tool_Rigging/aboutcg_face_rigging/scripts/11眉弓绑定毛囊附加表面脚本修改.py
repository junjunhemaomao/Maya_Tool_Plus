nurbs_shape = pm.PyNode("con_nurbsShape")
sel = pm.selected()

pm.select(cl = True)
main_grp = pm.group(n = nurbs_shape.name())

fn_nurbs = nurbs(nurbs_shape.name())

for i in sel:
    _,uv = fn_nurbs.closestPoint(i)
    uv = (float(uv[0])/float(nurbs_shape.mxu.get()), float(uv[1])/float(nurbs_shape.mxv.get()))
    transform = pm.createNode("transform")
    follicle = pm.createNode("follicle", p = transform)
    nurbs_shape.worldSpace[0] >> follicle.inputSurface
    follicle.parameterU.set(uv[0])
    follicle.parameterV.set(uv[1])
    follicle.outTranslate >> i.translate
    follicle.outRotate >> i.rotate
    pm.parent(transform, main_grp)
    