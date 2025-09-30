# -*- coding: utf-8 -*-
#处理fbx和mesh命名不一致的情况

import os
import maya.cmds as cmds

def rename_meshes_to_filename(*args):
    # 获取输入框中的文件夹路径
    fbx_directory = cmds.textField("fbxDirectory", q=True, text=True)

    # 获取指定文件夹中的所有FBX文件
    fbx_files = [f for f in os.listdir(fbx_directory) if f.endswith('.fbx')]
    print(fbx_files)

    # 记录导入前的mesh节点数量
    initial_meshes = cmds.ls(type="mesh")

    for fbx_file in fbx_files:
        # 构建FBX文件的完整路径
        fbx_path = os.path.join(fbx_directory, fbx_file)

        # 导入FBX文件到Maya场景中
        cmds.file(fbx_path, i=True)

        # 获取导入后新增加的mesh节点
        new_meshes = set(cmds.ls(type="mesh")) - set(initial_meshes)

        # 使用FBX文件名作为Mesh对象的名称
        new_name = os.path.splitext(fbx_file)[0]

        for mesh in new_meshes:
            # 获取Mesh对象所属的Transform节点的名称
            transform_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
            # 设置Mesh对象的名称为FBX文件名
            cmds.rename(transform_node, new_name)

        # 更新导入前的mesh节点数量
        initial_meshes = cmds.ls(type="mesh")
    print ('well done !')


# 创建窗口和布局
window_name = "Import_FBX_Rename 6666"
if cmds.window(window_name, exists=True):
    cmds.deleteUI(window_name)

cmds.window(window_name, title="Import_FBX_Rename 6666", widthHeight=(300, 100))
cmds.columnLayout(adjustableColumn=True)
cmds.text(label="Enter the FBX directory path:")
fbx_directory_field = cmds.textField("fbxDirectory", text=r"D:\Models\nn")
cmds.button(label="Import and Rename", width=200, height=30, command=rename_meshes_to_filename)
cmds.showWindow()
