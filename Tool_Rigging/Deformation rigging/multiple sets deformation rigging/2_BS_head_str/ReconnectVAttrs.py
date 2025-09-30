# -*- coding: utf-8 -*-

#####step4######
#控制器组复制新的后，子层级的显示隐藏关系消失
#这个脚本是恢复显示隐藏关系

#这个脚本比较坑爹的地方是，执行subCtrl属性连接的层级不对。要么是之前创建的脚本错了。作者并没有更新这个脚本

import maya.cmds as cmds

born = cmds.ls(sl=True)

for i in range(len(born)):
    octrl = born[i].replace("_ctrl", "_sub_ctrl")
    cmds.connectAttr(born[i] + ".subCtrl", octrl + "Shape.v")
