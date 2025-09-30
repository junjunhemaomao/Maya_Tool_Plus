#如果有的情况是一些贴图有漏网，把这些没匹配上的贴图集中收纳。
import os
import shutil

def find_existing_subdir(destination_dir, prefix):
    """
    在目标目录中查找已存在的文件前缀，并返回相应的子目录路径
    """
    for root, dirs, files in os.walk(destination_dir):
        for file in files:
            if file.startswith(prefix) and file.endswith("_D.png"):
                return root
    return None

def move_series_textures(source_dir, destination_dir):
    # 定义文件后缀
    suffixes = ["_D.png", "_M.png", "_N.png", "_alpha.png"]

    # 创建一个字典来存储系列文件
    series_dict = {}

    # 遍历源路径下的所有文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".png"):
                # 找到文件前缀
                for suffix in suffixes:
                    if file.endswith(suffix):
                        prefix = file[:-len(suffix)]
                        if prefix not in series_dict:
                            series_dict[prefix] = []
                        series_dict[prefix].append(os.path.join(root, file))
                        break

    # 移动属于同一系列的文件到新路径
    for prefix, file_list in series_dict.items():
        # 只要系列中有两张或更多的文件
        if len(file_list) >= 2:
            # 查找目标目录中已存在的子目录
            target_subdir = find_existing_subdir(destination_dir, prefix)
            if target_subdir is None:
                # 如果没有找到，跳过该系列文件
                print(f"目标文件夹不存在，跳过系列：{prefix}")
                continue

            for file in file_list:
                new_path = os.path.join(target_subdir, os.path.basename(file))
                shutil.move(file, new_path)
                print(f"Moved {file} to {new_path}")

    print("完成移动！")

if __name__ == "__main__":
    source_dir = r"I:\mod\17\Texture2D"
    destination_dir = r"D:\Asset_Library\#1 Character\Wild West Heroes"
    move_series_textures(source_dir, destination_dir)
