# -*- coding: utf-8 -*-
import maya.cmds as cmds

def set_driven_key(driver, driven):
    attributes = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]

    for attr in attributes:
        cmds.setDrivenKeyframe("{}.{}".format(driven, attr), cd="{}.brow_inner_up_down".format(driver))
        print("Successfully set driven key for {}.{} with {}.brow_inner_up_down".format(driven, attr, driver))

driver = 'l_brow_ctrl'
driven = ['l_brow_inner_ctrl', 'l_brow_inner_upper_ctrl']

for obj in driven:
    set_driven_key(driver, obj)

"""
MEL
select -r  'skinCluster -q -inf'
让我们逐个解释该命令的各个部分：

skinCluster：这是用于控制皮肤绑定（Skinning）的Maya节点类型之一。Skin Cluster节点用于将一个或多个物体与骨骼绑定，以便在动画或变形时保持与骨骼的连接。它是用于角色动画和变形的重要工具。

-q：这是skinCluster命令的一个选项，表示查询（query）模式。使用此选项，我们可以查询Skin Cluster节点的属性。

-inf：这是skinCluster命令的另一个选项，表示查询节点的输入（input）连接。在这种情况下，我们使用-inf选项来查询给定物体上应用的所有Skin Cluster节点。

select -r：这部分是将查询结果选中并在Maya中高亮显示。select命令用于选择物体或组件，而-r选项表示选择后保持选择（retain）模式，即保留之前选择的物体并添加新的选择结果。

综上所述，该命令的作用是查询给定物体上应用的所有Skin Cluster节点，并将其选中以在Maya视图中突出显示。

###############  l_brow_ctrl  ###############
眉弓
brow_inner_up_down
l_brow_inner_ctrl,l_brow_inner_upper_ctrl,

brow_mid_up_down
l_brow_mid_upper_ctrl,l_brow_mid_ctrl,l_brow_bone_ctrl

brow_outer_up_down
l_brow_outer_upper_ctrl,l_brow_outer_ctrl,l_brow_bone_ctrl

brow_squeeze_in_out
brow_mid_ctrl,l_brow_inner_upper_ctrl,l_brow_inner_ctrl,  l_brow_mid_ctrl,l_brow_outer_ctrl

###############  mid_brow_ctrl  ###############
眉心
brow_up_down
brow_mid_upper_ctrl,brow_mid_ctrl,nose_bridge_crease_ctrl

###############  nose _ctrl  ###############
鼻孔的缩放，放大时候只是鼻孔放大，缩放时候鼻孔缩小，鼻翼往内收一点
l_nostril_flare
l_nostril_ctrl,l_nose_crease_ctrl

耸鼻，鼻翼脸颊肌肉被压紧，靠近鼻翼的骨骼动幅最大
l_sneer
l_nasolabial_upper_ctrl,l_squint_inner_ctrl,l_squint_mid_ctrl,
l_nose_crease_ctrl,l_nasolabial_mid_ctrl,l_cheek_lower_inner_ctrl,
l_nostril_ctrl,l_lip_below_nose_ctrl,l_lip_nasolabial_crease_ctrl,l_nasolabial_mouth_corner_ctrl

只key位移。正常位置横向往外扩展
l_nostril_widen
l_nostril_ctrl,l_nose_crease_ctrl,l_nasolabial_mid_ctrl

颧骨鼓起，主要是颧骨周围到眼眶周围。模拟笑
l_smile_cheek_puff    范围(0-10)
第一组：
l_squint_outer_ctrl,l_squint_mid_ctrl,l_squint_inner_ctrl,l_nasolabial_upper_ctrl,l_nose_crease_ctrl,
l_nasolabial_mid_ctrl,l_cheek_upper_inner_ctrl,l_cheek_upper_outer_ctrl
第二组：
嘴周围，往后略收，嘴角往上提一点
l_nasolabial_mouth_corner_ctrl,l_lip_nasolabial_crease_ctrl,l_lip_below_nose_ctrl


脸颊鼓气.嘴唇周围也会略微鼓起
l_cheek_suck_puff
l_nostril_ctrl,l_nose_crease_ctrl,l_nasolabial_mid_ctrl,l_cheek_upper_inner_ctrl,l_cheek_lower_inner_ctrl,
lip_above_ctrl,l_lip_below_nose_ctrl,l_lip_nasolabial_crease_ctrl,l_nasolabial_mouth_corner_ctrl,l_jawline_ctrl,
l_nasolabial_lower_ctrl,l_chin_ctrl,l_lip_corner_ctrl,l_lip_lower_outer_ctrl,l_lip_upper_outer_ctrl,l_lip_lower_inner_ctrl,
l_lip_upper_inner_ctrl

脸颊吸气，塌陷 负方向
下巴jaw会略微旋转打开一点,上下嘴唇会闭合
jaw_ctrl,l_nasolabial_mid_ctrl,l_cheek_upper_inner_ctrl,l_cheek_lower_inner_ctrl,
lip_above_ctrl,l_lip_below_nose_ctrl,l_lip_nasolabial_crease_ctrl,l_nasolabial_mouth_corner_ctrl,l_jawline_ctrl,l_nasolabial_lower_ctrl,
l_chin_ctrl,l_lip_corner_ctrl,l_lip_lower_outer_ctrl,l_lip_upper_outer_ctrl,l_lip_lower_inner_ctrl,l_lip_upper_inner_ctrl，
lip_mid_lower_ctrl,lip_mid_upper_ctrl,lip_above_ctrl
  

###############  mouth_ctrl  ###############

jaw_open_close
驱动大部分骨骼，最开嘴动作
反向紧闭嘴，会略上抬一点嘴，咬肌会横向扩

l_mouth_corner_narrow_wide
嘴拉宽，主要在嘴角周围造成挤压，嘴角会靠后，鼻翼稍稍会配合拉开
反方向，嘴唇紧抿

l_mouth_corner_up_down
嘴角上下移动

mouth_up_down
嘴整体上下移动

mouth_left_right
旋转嘴唇。需要一个整体的定位器移动嘴部定位器。使用后可以删除

upper_lip_roll_in_out,lower_lip_roll_in_out
上下嘴唇的分别外翻内翻

upper_lip_up_down
只上下移动上嘴唇

lower_lip_up_down
只上下移动下嘴唇

upper_lip_in_out,lower_lip_in_out
前撅嘴，反向收紧紧贴牙齿

"""
