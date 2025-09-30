# 将指定根目录下所有子文件夹中的文件移动到根目录，并删除空的子文件夹，同时会智能处理文件名重复的情况
import os
import shutil
import send2trash  # 需要安装 `pip install send2trash`


def move_files_to_root(root_path):
    if not os.path.exists(root_path):
        print("根路径不存在")
        return

    file_count = {}

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if dirpath == root_path:
            continue  # 跳过根目录

        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            new_name = filename

            # 处理重名文件
            name, ext = os.path.splitext(filename)
            count = 1
            while os.path.exists(os.path.join(root_path, new_name)):
                new_name = f"{name}_{count}{ext}"
                count += 1

            new_path = os.path.join(root_path, new_name)
            shutil.move(old_path, new_path)
            print(f"移动: {old_path} -> {new_path}")

        # 如果子文件夹为空，则删除
        if not os.listdir(dirpath):
            send2trash.send2trash(dirpath)
            print(f"已删除空文件夹: {dirpath}")


if __name__ == "__main__":
    root_directory = r"H:\模型\武器"
    move_files_to_root(root_directory)
