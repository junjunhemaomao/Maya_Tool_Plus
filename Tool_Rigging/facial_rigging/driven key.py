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