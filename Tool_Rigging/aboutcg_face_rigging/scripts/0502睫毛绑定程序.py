import pymel.core as pm
is_lowe = True
sel = pm.selected()
collision_cv = pm.PyNode("evelash_lowe_collision_curve")
FORSIZE = 1000
OFF = 10

collision_cv_shape = collision_cv.getShape()
motionPath_test = pm.createNode("motionPath")
motionPath_test.fractionMode.set(True)
collision_cv_shape.worldSpace[0] >> motionPath_test.geometryPath

x_and_u_s = tuple([(motionPath_test.u.set(float(i) / (FORSIZE - 1)), float(i) / (FORSIZE - 1), motionPath_test.xc.get())[1:] for i in range(FORSIZE)])

pm.delete(motionPath_test)

def get_min_x_u(val):
    return min([(i[0], abs(val - i[1])) for i in x_and_u_s], key = lambda i:i[1])[0]

for i in sel:
    pos = pm.xform(i, q = True, t = True, ws = True)
    u = get_min_x_u(pos[0])
    loc = pm.spaceLocator(n = i.nodeName() + "_evelahs_collision_loc")
    pm.select(cl = True)
    jin = pm.joint(n = i.nodeName() + "_evelahs_collision_joint")
    pm.parent(jin, i)
    jin.t.set((0,0,0))
    jin.r.set((0,0,0))
    motionPath = pm.createNode("motionPath")
    motionPath.fractionMode.set(True)
    collision_cv_shape.worldSpace[0] >> motionPath.geometryPath
    motionPath.u.set(u)
    motionPath.ac >> loc.t
    if is_lowe:
        pm.aimConstraint(loc, jin, offset = (-OFF, 0, 0), weight = 1, aimVector = (0, 0, 1), upVector=(0, 1, 0), worldUpType = "objectrotation", worldUpVector = (0, 1, 0), worldUpObject = i)
    else:
        pm.aimConstraint(loc, jin, offset = (OFF, 0, 0), weight = 1, aimVector = (0, 0, 1), upVector=(0, 1, 0), worldUpType = "objectrotation", worldUpVector = (0, 1, 0), worldUpObject = i)
    pm.transformLimits(jin, ry = (0, 0), ery =  (1, 1))
    pm.transformLimits(jin, rz = (0, 0), erz =  (1, 1))
    if is_lowe:
        pm.transformLimits(jin, rx = (-360, 0), erx =  (0, 1))
    else:
        pm.transformLimits(jin, rx = (0, 360), erx =  (1, 0))