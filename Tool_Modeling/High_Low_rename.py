# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math


def get_model_center(model):
    bbox = cmds.exactWorldBoundingBox(model)
    return [(bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2]


def distance_between_models(model1, model2):
    center1 = get_model_center(model1)
    center2 = get_model_center(model2)
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(center1, center2)))


def find_high_low_pairs():
    all_models = cmds.ls(geometry=True)
    paired_models = set()
    high_low_pairs = []
    for model in all_models:
        if model in paired_models:
            continue
        distances = [(other_model, distance_between_models(model, other_model))
                     for other_model in all_models if other_model != model and other_model not in paired_models]

        if not distances:
            print("Warning: No unpaired model found for {0}".format(model))
            continue
        closest_model, _ = min(distances, key=lambda x: x[1])

        model_faces = cmds.polyEvaluate(model, face=True)
        closest_model_faces = cmds.polyEvaluate(closest_model, face=True)

        if model_faces >= closest_model_faces:
            high_model, low_model = model, closest_model
        else:
            high_model, low_model = closest_model, model

        high_low_pairs.append((high_model, low_model))
        paired_models.add(model)
        paired_models.add(closest_model)
    return high_low_pairs


def rename_models_with_prefix(prefix):
    pairs = find_high_low_pairs()
    for i, (high, low) in enumerate(pairs, 1):
        base_name = "{0}{1}".format(prefix, i)
        high_name = "{0}_high".format(base_name)
        low_name = "{0}_low".format(base_name)

        # 获取模型的父对象（如果有的话）
        high_parent = cmds.listRelatives(high, parent=True)
        low_parent = cmds.listRelatives(low, parent=True)

        # 重命名模型
        high = cmds.rename(high, high_name)
        low = cmds.rename(low, low_name)

        # 如果模型有父对象，重命名父对象
        if high_parent:
            cmds.rename(high_parent[0], high_name)
        if low_parent:
            cmds.rename(low_parent[0], low_name)

        print("Renamed pair {0}:".format(i))
        print("  High poly: {0}".format(high))
        print("  Low poly:  {0}".format(low))

    print("Renaming completed.")


def execute_rename(prefix_field):
    prefix = cmds.textFieldGrp(prefix_field, query=True, text=True)
    rename_models_with_prefix(prefix)


def show_ui():
    if cmds.window("renameWindow", exists=True):
        cmds.deleteUI("renameWindow", window=True)

    window = cmds.window("renameWindow", title="Batch Rename High/Low Models", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)

    prefix_field = cmds.textFieldGrp(label="Prefix: ", text="chest")

    cmds.button(label="Rename Models", command=lambda x: execute_rename(prefix_field))

    cmds.showWindow(window)


# 显示UI
show_ui()