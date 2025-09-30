#针对有的情况贴图并没有连接完全，只连接了颜色贴图，在生成资产后，把其他贴图移动过去
# -*- coding: utf-8 -*-
import os
import shutil

def move_texture_files(source_dir, target_dir):
    # 定义文件后缀
    suffixes = ["_M.png", "_N.png", "_alpha.png"]

    # 遍历目标路径下的所有子文件夹
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            # 只处理.png文件
            if file.endswith(".png"):
                # 获取文件的前缀
                prefix = file[:-6]  # 去掉 "_D.png"

                # 遍历后缀
                for suffix in suffixes:
                    source_file = os.path.join(source_dir, prefix + suffix)
                    target_file = os.path.join(root, prefix + suffix)

                    if os.path.exists(source_file):
                        # 将文件复制到目标文件夹（覆盖现有文件）
                        shutil.copy2(source_file, target_file)
                        # 删除源文件
                        os.remove(source_file)
                        print(f"Moved {source_file} to {target_file} (overwritten if existed)")

    print("完成移动！")

if __name__ == "__main__":
    source_dir = r"D:\mod\Zenonia 全套模型 角色 动作 怪物 场景\0428.Zenonia 石头 岩石 山脉 冰山\Stone2"
    target_dir = r"D:\mod\Zenonia 全套模型 角色 动作 怪物 场景\0428.Zenonia 石头 岩石 山脉 冰山\Mountain"
    move_texture_files(source_dir, target_dir)