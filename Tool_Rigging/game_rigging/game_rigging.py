# -*- coding: utf-8 -*-

# 适用于游戏的身体绑定
# 还比较初级和不完善

import maya.cmds as cmds

#创建独立的骨骼点。关键是下个循环前要取消当前的骨骼选择，不然会形成父子结构
#单位尺寸的厘米。
def create_body_joints():
    joints_body_data = {
        #脊柱
        'root': (0, 109.883, 0),'Spine_1': (0, 121.765, 0.931),'Spine_2': (0, 130.514, 0.438),'Spine_3': (0, 147.879, -1.087),
        #手臂
        'l_clavicle': (2.671, 149.306, 1.007),'l_bicep': (14.577, 148.644, -5.632),'l_elbow': (22.666, 123.654, -7.517),'l_wrist': (36.886, 102.232, 0.16),
        #手
        'l_thumb':(36.978, 97.705, 4.264), 'l_thumb_end':(38.021, 94.74, 7.104),
        'l_index_1':(43.435, 92.97, 2.908),'l_index_2':(44.778, 87.986, 4.264),'l_index_end':(42.541, 85.803, 4.865),
        #脚
        'l_thigh': (12.941, 102.687, 0.302), 'l_knee': (19.063, 60.464, -1.296), 'l_ankle': (24.35, 19.096, -7.296),'l_toeBase': (28.464, 2.524, 1.34)
    }
    biped_joints_body_data = {
        #脊柱
        'Bip001': (0, 109.883, 0),'Bip001 Pelvis': (0, 109.883, 0),'Spine_1': (0, 121.765, 0.931),'Spine_2': (0, 130.514, 0.438),'Spine_3': (0, 147.879, -1.087),
        #手臂
        'l_clavicle': (2.671, 149.306, 1.007),'l_bicep': (14.577, 148.644, -5.632),'l_elbow': (22.666, 123.654, -7.517),'l_wrist': (36.886, 102.232, 0.16),
        #手
        'l_thumb':(36.978, 97.705, 4.264), 'l_thumb_end':(38.021, 94.74, 7.104),
        'l_index_1':(43.435, 92.97, 2.908),'l_index_2':(44.778, 87.986, 4.264),'l_index_end':(42.541, 85.803, 4.865),
        #脚
        'l_thigh': (12.941, 102.687, 0.302), 'l_knee': (19.063, 60.464, -1.296), 'l_ankle': (24.35, 19.096, -7.296),'l_toeBase': (28.464, 2.524, 1.34)
    }
    cmds.headsUpMessage("Game Joint V1.0")
    # set the unit to centimeters
    cmds.currentUnit(linear='cm')
    # confirm the new unit
    unit = cmds.currentUnit(q=True, linear=True)
    print('Current linear unit: {}'.format(unit))

    # clear the current selection
    cmds.select(clear=True)

    for name, pos in joints_body_data.items():
        cmds.joint(p=pos, n=name, relative=True)
        cmds.select(clear=True)

################################################################

def mirror_left_joints():
    selected = cmds.ls('l_thigh','l_clavicle')
    for s in selected:
        # Check if name starts with "l_"
        if not s.startswith("l_"):
            continue
        # Replace first "l_" with "r_"
        mirror_name = s.replace("l_", "r_", 1)
        cmds.mirrorJoint(s, mirrorYZ=True, mirrorBehavior=True, searchReplace=("l", "r"))
        cmds.rename(mirror_name)
    cmds.select(clear=True)

################################################################
#这里要调整下骨骼的旋转
def connect_body_joints():
    cmds.headsUpMessage("Parent Joints")

    cmds.parent('Spine_3','Spine_2')
    cmds.parent('Spine_2', 'Spine_1')
    cmds.parent('Spine_1', 'root')

    cmds.parent('l_wrist','l_elbow')
    cmds.parent('l_elbow', 'l_bicep')
    cmds.parent('l_bicep', 'l_clavicle')
    cmds.parent('l_clavicle','Spine_3')

    cmds.parent('l_thumb_end','l_thumb')
    cmds.parent('l_thumb', 'l_wrist')
    cmds.parent('l_index_end', 'l_index_2')
    cmds.parent( 'l_index_2','l_index_1')
    cmds.parent('l_index_1', 'l_wrist')

    cmds.parent('l_toeBase','l_ankle')
    cmds.parent('l_ankle', 'l_knee')
    cmds.parent('l_knee', 'l_thigh')
    cmds.parent('l_thigh','root')

    cmds.select(clear=True)

################################################################

def create_ctrl_from_anim():
    cmds.headsUpMessage("Tip:head_anim Joint drawStyle is None")
############################        添加控制曲线        #########################################
## Cube_ctrl
def cube (arg):
	cmds. polyCube(n='edg' )
	cmds. select ('edg.e[1]', 'edg.e[2]','edg.e[3]', 'edg.e[4]', 'edg.e[5]','edg.e[6]','edg.e[7]','edg.e[8]','edg.e[9]','edg.e[10]','edg.e[11]','edg.e[12]',)
	cmds. polyToCurve (form=2, degree=1, conformToSmoothMeshPreview=1)
	cmds. select ('edg.e[0]')
	cmds. polyToCurve (form=2, degree=1, conformToSmoothMeshPreview=1)
	cmds. select ('edg.e[6]')
	cmds. polyToCurve (form=2, degree=1, conformToSmoothMeshPreview=1)
	cmds. select ('edg.e[9]')
	cmds. polyToCurve (form=2, degree=1, conformToSmoothMeshPreview=1)
	cmds. select ('polyToCurve1','polyToCurve2', 'polyToCurve3', 'polyToCurve4')
	cmds. DeleteHistory()
	cmds. Group (em= True, name= 'null')
	cmds. select ('polyToCurve1','polyToCurve2', 'polyToCurve3', 'polyToCurve4')
	cmds. parent (w = True)
	cmds. select ('polyToCurveShape1', 'polyToCurveShape2', 'polyToCurveShape3', 'polyToCurveShape4')
	cmds. select ('group1', add=True)
	cmds. parent (r=True, s=True)
	cmds. delete ('polyToCurve1','polyToCurve2', 'polyToCurve3', 'polyToCurve4', 'edg')
	cmds. rename ("group1","Cube")
	cmds. rename ('polyToCurveShape1','CubeShape1')
	cmds. rename ('polyToCurveShape2','CubeShape2')
	cmds. rename ('polyToCurveShape3','CubeShape3')
	cmds. rename ('polyToCurveShape4','CubeShape4')
	cmds. select (clear=True)
	om. MGlobal. displayInfo ("The Cube is Built")

## Circle_ctrl
def circle (arg):
	cmds. CreateNURBSCircle (d= 1)
	cmds. DeleteHistory ()
	cmds. rename ("nurbsCircle1", "Circle")
	cmds. select (clear=True)
	om. MGlobal.displayInfo ("The Circle is Built")


############################     给控制器添加属性        #########################################
#眉弓控制器  l_brow_ctrl
def add_brow_attributes():
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.warning("Please select a control curve.")
        return

    ctrl_name = sel[0]
    attrs = ['brow_inner_up_down', 'brow_mid_up_down', 'brow_outer_up_down', 'brow_squeeze_in_out']
    for attr in attrs:
        cmds.addAttr(ctrl_name, longName=attr, attributeType='float', minValue=-10.0, maxValue=10.0, defaultValue=0.0,
                     keyable=True)

###################################   UI   #################################

cmds.window("Game Rrigging")
cmds.columnLayout()
cmds.text(label="Base Joint")
cmds.button(label="Base Body Joint", width=350, height=30, command="create_body_joints()")
cmds.button(label="connect_Body_joints", width=350, height=30, command="connect_body_joints()")
cmds.button(label="Mirror Joints", width=350, height=30, command="mirror_left_joints()")


cmds.text(label="Add NUBS Curve Ctrl")
cmds.button(label='Cube Ctrl', width=350, height=30, command=cube)
cmds.button(label='Circle Ctrl', width=350, height=30, command=circle)
cmds.showWindow()
