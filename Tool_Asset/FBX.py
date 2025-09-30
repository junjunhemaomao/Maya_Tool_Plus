# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import maya.mel as mel
import time
import logging


class FBXProcessorUI:
    def __init__(self):
        self.window_name = "fbxProcessorWindow"
        self.setup_logging()
        self.create_ui()

    def setup_logging(self):
        """设置日志系统"""
        self.logger = logging.getLogger('FBXProcessor')
        self.logger.setLevel(logging.DEBUG)

        log_dir = os.path.join(os.path.expanduser("~"), "fbx_processor_logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, f'fbx_processor_{time.strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def create_ui(self):
        """创建用户界面"""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        window = cmds.window(self.window_name, title="FBX文件处理工具", width=400)
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))

        cmds.frameLayout(label="输入设置", collapsable=False, marginWidth=5, marginHeight=5)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(80, 240, 60),
                       columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'left', 0)])
        cmds.text(label="输入文件夹:")
        self.input_field = cmds.textField()
        cmds.button(label="浏览", command=lambda x: self.browse_folder("input"))
        cmds.setParent('..')
        self.recursive_option = cmds.checkBox(label="递归读取子文件夹", value=False)
        cmds.setParent('..')

        cmds.frameLayout(label="输出设置", collapsable=False, marginWidth=5, marginHeight=5)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(80, 240, 60),
                       columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'left', 0)])
        cmds.text(label="输出文件夹:")
        self.output_field = cmds.textField()
        cmds.button(label="浏览", command=lambda x: self.browse_folder("output"))
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(label="处理选项", collapsable=False, marginWidth=5, marginHeight=5)
        self.merge_option = cmds.checkBox(label="合并相同Mesh", value=True)
        self.delete_joints = cmds.checkBox(label="删除骨骼", value=True)
        cmds.setParent('..')

        cmds.frameLayout(label="处理进度", collapsable=False, marginWidth=5, marginHeight=5)
        self.progress_text = cmds.text(label="准备就绪", align="left")
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnWidth2=(190, 190), columnAlign2=('center', 'center'))
        cmds.button(label="开始处理", command=self.start_processing, width=180)
        cmds.button(label="关闭", command=self.close_ui, width=180)

        cmds.showWindow(window)

    def browse_folder(self, field_type):
        """浏览文件夹"""
        folder = cmds.fileDialog2(fileMode=3, dialogStyle=2)
        if folder:
            if field_type == "input":
                cmds.textField(self.input_field, edit=True, text=folder[0])
            else:
                cmds.textField(self.output_field, edit=True, text=folder[0])

    def unlock_attributes(self, objects):
        """解锁对象的锁定属性"""
        for obj in objects:
            try:
                attrs = ['translate', 'rotate', 'scale']
                for attr in attrs:
                    for axis in ['X', 'Y', 'Z']:
                        full_attr = f'{obj}.{attr}{axis}'
                        if cmds.getAttr(full_attr, lock=True):
                            cmds.setAttr(full_attr, lock=False)
            except Exception as e:
                self.logger.warning(f"解锁属性失败 {obj}: {str(e)}")

    def get_fbx_files(self, input_folder, recursive):
        """获取FBX文件列表"""
        fbx_files = []
        for root, _, files in os.walk(input_folder):
            fbx_files.extend([os.path.join(root, f) for f in files if f.lower().endswith('.fbx')])
            if not recursive:
                break
        return fbx_files

    def process_fbx_files(self, input_folder, output_folder):
        """处理FBX文件的主要函数（优化命名逻辑）"""
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
                self.logger.info(f"已创建输出文件夹: {output_folder}")
            except Exception as e:
                self.logger.error(f"创建输出文件夹失败: {str(e)}")
                cmds.text(self.progress_text, edit=True, label="错误：无法创建输出文件夹！")
                return
            
        recursive = cmds.checkBox(self.recursive_option, query=True, value=True)
        fbx_files = self.get_fbx_files(input_folder, recursive)

        total_files = len(fbx_files)
        self.logger.info(f"找到 {total_files} 个FBX文件")

        success_count = 0
        error_count = 0

        for index, input_path in enumerate(fbx_files, 1):
            fbx_file = os.path.basename(input_path)
            output_path = os.path.join(output_folder, fbx_file)
            base_name = os.path.splitext(fbx_file)[0]  # 提前获取基础名称

            progress_msg = f"处理中: {fbx_file} ({index}/{total_files})"
            self.logger.info(progress_msg)
            cmds.text(self.progress_text, edit=True, label=progress_msg)

            try:
                # 新建场景
                cmds.file(new=True, force=True)

                # 导入FBX
                cmds.file(input_path, i=True, type="FBX", ignoreVersion=True, options="v=0;", ra=True)

                # 删除骨骼和绑定
                if cmds.checkBox(self.delete_joints, query=True, value=True):
                    joints = cmds.ls(type='joint')
                    if joints:
                        self.unlock_attributes(joints)
                        cmds.delete(joints)

                # 清理和冻结变换
                all_transforms = cmds.ls(type='transform')
                for obj in all_transforms:
                    try:
                        self.unlock_attributes([obj])
                        cmds.makeIdentity(obj, apply=True, translate=True, rotate=True, scale=True, normal=False)
                        cmds.delete(obj, ch=True)
                    except Exception as e:
                        self.logger.warning(f"跳过对象 {obj}: {str(e)}")

                # 合并Mesh并应用文件名命名
                if cmds.checkBox(self.merge_option, query=True, value=True):
                    meshes = cmds.ls(type='mesh', long=True)
                    if meshes:
                        parent_transforms = list(set(cmds.listRelatives(meshes, parent=True, fullPath=True)))
                        if parent_transforms:
                            try:
                                merged_mesh = cmds.polyUnite(
                                    parent_transforms,
                                    ch=False,
                                    mergeUVSets=True,
                                    name=base_name
                                )[0]
                                cmds.polyNormal(merged_mesh, normalMode=0)
                                cmds.delete(merged_mesh, ch=True)
                                self.logger.info(f"合并 {len(parent_transforms)} 个Mesh成功: {merged_mesh}")
                            except Exception as e:
                                self.logger.warning(f"合并Mesh失败: {str(e)}")

                # 删除空组
                transforms = cmds.ls(type='transform', long=True)
                empty_count = 0
                for transform in transforms:
                    children = cmds.listRelatives(transform, children=True, fullPath=True) or []
                    if not children:
                        cmds.delete(transform)
                        empty_count += 1
                self.logger.debug(f"删除 {empty_count} 个空组")

                # 导出前检查
                if not cmds.ls(type='mesh'):
                    raise Exception("没有找到可导出的mesh")

                # 导出FBX
                cmds.file(output_path, force=True, type="FBX export", exportAll=True, options="v=0;")
                if not os.path.exists(output_path):
                    raise Exception("文件导出失败")

                success_count += 1
                self.logger.info(f"成功处理: {fbx_file}")

            except Exception as e:
                error_count += 1
                error_msg = f"处理失败 {fbx_file}: {str(e)}"
                self.logger.error(error_msg)
                cmds.text(self.progress_text, edit=True, label=error_msg)
                continue

        final_msg = f"处理完成！成功: {success_count}, 失败: {error_count}"
        self.logger.info(final_msg)
        cmds.text(self.progress_text, edit=True, label=final_msg)

    def start_processing(self, *args):
        """开始处理文件"""
        input_folder = cmds.textField(self.input_field, query=True, text=True)
        output_folder = cmds.textField(self.output_field, query=True, text=True)

        if not input_folder or not output_folder:
            cmds.warning("请选择输入和输出文件夹！")
            return

        self.process_fbx_files(input_folder, output_folder)

    def close_ui(self, *args):
        """关闭UI"""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
            self.logger.info("关闭UI")


def show_ui():
    FBXProcessorUI()


if __name__ == "__main__":
    show_ui()