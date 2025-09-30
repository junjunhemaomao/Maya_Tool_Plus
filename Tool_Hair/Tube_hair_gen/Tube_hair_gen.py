# -*- coding: utf-8 -*-

#风格化头发创建脚本

import maya.cmds as cmds

def set_curve_pivot_to_first_cv():
    # Get the selected objects
    selected = cmds.ls(sl=True)
    # Set the pivot to the first CV of each selected curve
    for node in selected:
        p = cmds.getAttr(node + ".cv[0]")
        cmds.xform(node, ws=True, piv=[p[0][0],p[0][1],p[0][2]])

def create_tube():
    # Create a cylinder and delete the faces
    cmds.polyCylinder(r=1, h=2, sx=20, sy=16, sz=0, ax=[0, 1, 0], rcp=0, cuv=3, ch=1, n='tube')
    cmds.select('tube*.f[320]')
    cmds.Delete()
    cmds.select('tube*.f[321]')
    cmds.Delete()

"""
First select the Cylinder created from the Creating Tube Script, then SHIFT+select the Curve in
that order. Cylinder first, Curve next.
After the Curve Warp is run, the cylinder should show up at the pivot point of the curve.
Now select the curve, in the Attribute Editor, goto CurveWarp tab then click select.
With the curve warp selected, click botton Modify curve warp
"""
def modify_curve_warp():
    # Modify Curve Warp settings
    selected = cmds.ls(sl=True)
    for node in selected:
        cmds.setAttr(node + ".keepLength", 0)
        cmds.setAttr(node + ".alignmentMode", 3)
        cmds.setAttr(node + ".scaleCurve[3].scaleCurve_Value", 0.09)
        cmds.setAttr(node + ".scaleCurve[0].scaleCurve_Value", 0.29)

def group_tube_curve():
    if cmds.objExists('GRP_Groom_Tube'):
        print "GRP_Groom_Tube already exists!"
    else:
        cmds.group(empty=True, name="GRP_Groom_Tube")
    cmds.parent("tube*", "GRP_Groom_Tube")
    cmds.parent("curve*", "GRP_Groom_Tube")

###################################   UI   #################################

cmds.window("Stylized Hair by TubeGroom",widthHeight=(700,140),s=0)
cmds.columnLayout( adjustableColumn=True )
cmds.text(label="Must be NUBS Curve.")
cmds.button(label = "Set curve pivot to first CV",width = 200,height=30,command = "set_curve_pivot_to_first_cv()")
cmds.button(label = "Create Tube",width = 200,height=30,command = "create_tube()")
cmds.text(label="select curve, in the Attribute Editor,CurveWarp tab then click select")
cmds.button(label = "Modify curve warp",bgc=[0, 0.5, 1],width = 200,height=30,command = "modify_curve_warp()")
cmds.text(label="extra")
cmds.button(label = "GRP_Groom_Tube",width = 200,height=30,command = "group_tube_curve()")
cmds.showWindow()