# -*- coding: utf-8 -*-
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

def get_skin_cluster(obj):
    history_nodes = cmds.listHistory(obj)
    skin_clusters = cmds.ls(history_nodes, type='skinCluster')
    return skin_clusters[0] if skin_clusters else None

def copy_skin_weights(source_obj, target_objs):
    source_skinnode = get_skin_cluster(source_obj)

    if source_skinnode:
        source_guge = cmds.skinCluster(source_skinnode, query=True, inf=True)

        for target_obj in target_objs:
            target_skinnode = get_skin_cluster(target_obj)

            if target_skinnode:
                target_guge = cmds.skinCluster(target_skinnode, query=True, inf=True)

                if target_guge and source_guge:
                    if source_guge != target_guge:
                        new_need_add = [each_list for each_list in source_guge if each_list not in target_guge]

                        if new_need_add:
                            for each_need_add in new_need_add:
                                cmds.skinCluster(target_skinnode, edit=True, lw=True, wt=0, ai=each_need_add)
            else:
                cmds.skinCluster(source_guge, target_obj, rui=0, tsb=True)

            cmds.select(clear=True)
            cmds.select(source_obj)
            cmds.select(target_obj, add=True)
            cmds.copySkinWeights(noMirror=True, sa='closestPoint', ia='oneToOne')
            print('\nSuccess copy.............', target_obj)


# 获取 Maya 主窗口
def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class CopySkinWeightsUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(CopySkinWeightsUI, self).__init__(parent)
        self.setWindowTitle("Copy Skin Weights")
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.source_obj = ""
        self.target_objs = []

        self.create_ui()
        self.create_connections()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # 源物体选择
        src_layout = QtWidgets.QHBoxLayout()
        self.source_field = QtWidgets.QLineEdit()
        self.source_field.setPlaceholderText("Select a source object...")
        self.source_field.setReadOnly(True)
        self.src_btn = QtWidgets.QPushButton("Pick Source")
        src_layout.addWidget(QtWidgets.QLabel("Source:"))
        src_layout.addWidget(self.source_field)
        src_layout.addWidget(self.src_btn)

        # 目标物体选择
        tgt_layout = QtWidgets.QHBoxLayout()
        self.target_field = QtWidgets.QLineEdit()
        self.target_field.setPlaceholderText("Select one or more target objects...")
        self.tgt_btn = QtWidgets.QPushButton("Pick Targets")
        tgt_layout.addWidget(QtWidgets.QLabel("Targets:"))
        tgt_layout.addWidget(self.target_field)
        tgt_layout.addWidget(self.tgt_btn)

        # 执行按钮
        self.copy_btn = QtWidgets.QPushButton("Copy Skin Weights")
        self.copy_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 30px;")

        layout.addLayout(src_layout)
        layout.addLayout(tgt_layout)
        layout.addWidget(self.copy_btn)

    def create_connections(self):
        self.src_btn.clicked.connect(self.select_source_object)
        self.tgt_btn.clicked.connect(self.select_target_objects)
        self.copy_btn.clicked.connect(self.execute_copy)

    def select_source_object(self):
        selected = cmds.ls(selection=True)
        if selected:
            self.source_obj = selected[0]
            self.source_field.setText(self.source_obj)

    def select_target_objects(self):
        selected = cmds.ls(selection=True)
        if selected:
            self.target_objs = selected
            self.target_field.setText(", ".join(self.target_objs))

    def execute_copy(self):
        if not self.source_obj or not self.target_objs:
            cmds.warning("Please select both source and target objects.")
            return
        copy_skin_weights(self.source_obj, self.target_objs)
        QtWidgets.QMessageBox.information(self, "Done", "Skin weights copied successfully!")


# 打开 UI
def show_ui():
    for widget in QtWidgets.QApplication.allWidgets():
        if isinstance(widget, CopySkinWeightsUI):
            widget.close()
            widget.deleteLater()
    dlg = CopySkinWeightsUI()
    dlg.show()


show_ui()
