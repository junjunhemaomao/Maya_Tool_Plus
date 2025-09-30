# -*- coding: utf-8 -*-

#####step5######
"""
复制控制器组，把原来的重命名，注意他这里把原来"ctrl"字段的改命名为"Lctrl"。
新复制的控制器通过一下代码和原来控制器产生关联。
看代码是位置和旋转约束

重点，难点：
此时解决可以控制器组可以key动画，但上面一层的offest组可以任意移动，不会对骨骼产生影响
"""

import maya.cmds as cmds

born = cmds.ls(sl=True)
for i in range(len(born)):
    GRPnam = born[i].replace("ctrl", "Lctrl")
    cmds.connectAttr(born[i] + ".translate", GRPnam + ".translate")
    cmds.connectAttr(born[i] + ".rotate", GRPnam + ".rotate")

}


"""
当您在Maya中选择一个或多个对象并运行此代码时，它将为每个对象创建一个新的组（Group），并将其命名为以“Lctrl”代替原名称中的“ctrl”字符。
然后，它将使用 connectAttr 命令将原对象的旋转和平移属性连接到新组的旋转和平移属性。这个过程相当于将每个选定的对象放置到自己的组中，并将组用作它们的父节点。

以下是更详细的解释：

第一行代码 born = cmds.ls(sl=True) 使用 Maya Python 模块（cmds）中的 ls 命令来获取所选对象的名称，并将它们存储在名为 born 的字符串列表中。sl=True 参数表示只获取当前选择的对象。

for 循环迭代 born 列表中的每个对象。在循环中，第二行代码 GRPnam = born[i].replace("ctrl", "Lctrl") 使用字符串 replace 方法来创建一个名为 GRPnam 的新字符串，
它是将当前对象的名称中的“ctrl”替换为“Lctrl”之后的结果。例如，如果当前对象名称为“myctrl”，则 GRPnam 将被设置为 “myLctrl”。

最后，第三行和第四行代码使用 connectAttr 命令将原对象的旋转和平移属性连接到新组的旋转和平移属性。例如，对于当前迭代的对象 born[i] 和对应的新组 GRPnam，
第三行代码 cmds.connectAttr(born[i] + ".translate", GRPnam + ".translate") 将连接原对象的平移属性到新组的平移属性上。
同样，第四行代码 cmds.connectAttr(born[i] + ".rotate", GRPnam + ".rotate") 将连接原对象的旋转属性到新组的旋转属性上。

总的来说，这个代码的目的是为了创建一个组层次结构，让每个所选对象都位于自己的组中。这在制作复杂的场景时非常有用，因为它可以使对象之间的关系更加清晰，并且可以更轻松地对对象进行控制和修改。
"""