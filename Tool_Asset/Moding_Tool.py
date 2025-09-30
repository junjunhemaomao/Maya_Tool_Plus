import maya.cmds as cmds

def separate_objects():
    selected_objects = cmds.ls(selection=True, long=True)

    if not selected_objects:
        cmds.warning("No objects selected. Please select some objects.")
        return

    for obj in selected_objects:
        cmds.select(obj, replace=True)
        cmds.polySeparate()
        cmds.delete(obj, constructionHistory=True)

def detach_separate():
    name_split_skip = []
    face_num = []
    temp = []
    new_obj = []
    new_face_sel = []

    orig_face_sel = cmds.filterExpand(sm=34, ex=1)
    orig_obj_shape = cmds.listRelatives(orig_face_sel[0], parent=True)
    orig_obj = cmds.listRelatives(orig_obj_shape[0], parent=True)

    for step in range(len(orig_face_sel)):
        temp = orig_face_sel[step].split(".")
        name_split_skip.extend(temp)
        temp = []

    for step2 in range(0, len(name_split_skip), 2):
        face_num.append(name_split_skip[step2 + 1])

    new_obj = cmds.duplicate(orig_obj[0], un=True)
    cmds.delete(new_obj[0], ch=True)
    new_all_faces = cmds.ls(new_obj[0] + ".f[*]")

    for step3 in range(len(face_num)):
        new_face_sel.append(new_obj[0] + "." + face_num[step3])

    cmds.delete(orig_face_sel)

    cmds.select(new_all_faces)
    cmds.select(new_face_sel, d=True)
    cmds.delete()
    cmds.select(new_obj[0])

def mergeAndDeleteHistory():
    selected_objects = cmds.ls(selection=True)

    if len(selected_objects) < 2:
        cmds.warning("Select at least two objects to merge.")
        return

    merged_object = cmds.polyUnite(selected_objects, ch=False, mergeUVSets=True, centerPivot=True)[0]

    cmds.delete(merged_object, ch=True)
    cmds.select(merged_object, replace=True)

def center_pivot_to_selected():
    selected_objects = cmds.ls(selection=True)

    if selected_objects:
        for obj in selected_objects:
            cmds.select(obj)
            cmds.CenterPivot()

def centerPivotToOrigin():
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("Please select objects!")
        return

    for obj in selected_objects:
        pivot_position = cmds.xform(obj, query=True, rotatePivot=True, worldSpace=True)
        cmds.xform(obj, pivots=(0, 0, 0), worldSpace=True)
        print("Moved pivot of object {} to origin.".format(obj))

def reverse_normals():
    selected_objects = cmds.ls(selection=True,  long=True)

    if not selected_objects:
        cmds.warning("Please select objects to reverse normals.")
        return

    for obj in selected_objects:
        cmds.polyNormal(nm=3)
        cmds.delete(obj, constructionHistory=True)

def delete_joints():
    mesh_objects = cmds.ls(type='mesh', long=True)
    joints_objects = cmds.ls(type='joint', long=True)

    for obj in mesh_objects:
        skin_cluster = cmds.listConnections(obj, type='skinCluster')
        if skin_cluster:
            cmds.skinCluster(skin_cluster[0], edit=True, unbind=True)
            print("Unbound skin: {}".format(obj))

    if joints_objects:
        cmds.delete(joints_objects)
        print("Deleted {} joint objects".format(len(joints_objects)))

def rename_object_to_material_name():
    selected_objects = cmds.ls(selection=True)

    if selected_objects:
        for obj in selected_objects:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []

            if not shapes:
                print("Object %s has no shape node." % obj)
                continue

            shadingEngines = cmds.listConnections(shapes, type="shadingEngine")

            if not shadingEngines:
                print("Object %s has no connected shading engine." % obj)
                continue

            materials = cmds.ls(cmds.listConnections(shadingEngines), materials=True)

            if not materials:
                print("Object %s has no associated materials." % obj)
                continue

            material_name = materials[0]

            cmds.rename(obj, material_name)

cmds.window("Detach&Combine", widthHeight=(600, 300))
cmds.columnLayout(adjustableColumn=True)

cmds.text(label="Automatically separate individual components")
cmds.button(label="Separate", width=400, height=40, backgroundColor=(0.345, 0.525, 1.0), command="separate_objects()")

cmds.text(label="Detach selected faces from one object")
cmds.button(label="Detach Separate Face", width=400, height=40, backgroundColor=(0.345, 0.525, 1.0), command="detach_separate()")

cmds.text(label="Merge selected objects")
cmds.button(label="Combine", width=200, height=40, command="mergeAndDeleteHistory()")

cmds.text(label="Reset pivot to center")
cmds.button(label="Center Pivot", width=200, height=40, command="center_pivot_to_selected()")

cmds.text(label="Move pivot to origin")
cmds.button(label="Center Pivot To Origin", width=400, height=40, command="centerPivotToOrigin()")

cmds.text(label="Reverse Normals")
cmds.button(label="Flip Normals", width=200, height=40, command="reverse_normals()")

cmds.text(label="Delete Joints and Skin Bindings")
cmds.button(label="Delete Joints", width=200, height=40, command="delete_joints()")

cmds.text(label="Rename objects to material names")
cmds.button(label="Rename by Material", width=200, height=40, command="rename_object_to_material_name()")

cmds.showWindow()
