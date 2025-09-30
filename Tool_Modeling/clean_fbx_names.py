# -*- coding: utf-8 -*-
import maya.cmds as cmds
import re

def clean_fbx_names():
    print("=" * 50)
    print("开始清理FBX命名...")
    print("=" * 50)
    objects = list(set(cmds.ls(transforms=True) + cmds.ls(shapes=True) + cmds.ls(materials=True)))
    print("找到 {} 个对象待处理".format(len(objects)))
    renamed = {}
    for obj in objects:
        try:
            if not obj.strip() or (':' in obj and all(part.strip() for part in obj.split(':'))):
                continue
            new_name = re.sub(r'FBXASC\d{3}', '_', obj)
            new_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', new_name)
            new_name = re.sub(r'_+', '_', new_name).strip('_')
            if not new_name:
                new_name = "unnamed"
            if new_name[0].isdigit():
                new_name = "obj_" + new_name
            unique_name = new_name
            i = 1
            while cmds.ls(unique_name):
                unique_name = "{}_{}".format(new_name, i)
                i += 1
            if unique_name != obj:
                cmds.rename(obj, unique_name)
                renamed[obj] = unique_name
                print("  {} -> {}".format(obj, unique_name))
        except Exception as e:
            print("  [失败] {}: {}".format(obj, e))
    print("\n共重命名 {} 个对象".format(len(renamed)))
    return renamed

clean_fbx_names()
