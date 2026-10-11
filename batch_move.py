import os
import shutil

# 1. 之前解压文件所在的源目录
source_dir = r"D:/python_test/sex"

# 2. 想要统一存放移动结果的目标目录
destination_dir = r"D:/python_test/all_extracted_files"

def move_extracted_folders(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)

    moved_count = 0
    print("=" * 60)
    print(f"📦 开始搜寻并移动所有的 _extracted 文件夹...")
    print(f"📂 源目录: {src_dir}")
    print(f"🎯 目标目录: {dst_dir}")
    print("=" * 60)

    # os.walk 递归遍历所有层级的子目录
    for root, dirs, files in os.walk(src_dir, topdown=False):
        for dir_name in dirs:
            # 筛选出所有名称带 _extracted 的文件夹
            if dir_name.endswith("_extracted"):
                folder_src_path = os.path.join(root, dir_name)
                folder_dst_path = os.path.join(dst_dir, dir_name)

                print(f"🚚 正在移动: {dir_name} ...", end="")

                # 如果目标文件夹已存在同名目录，先清理避免覆盖冲突
                if os.path.exists(folder_dst_path):
                    shutil.rmtree(folder_dst_path)

                # 移动文件夹
                shutil.move(folder_src_path, dst_dir)
                moved_count += 1
                print(" -> ✅ 完成")

    print("\n" + "=" * 60)
    print(f"📊 处理完成！共成功移动了 {moved_count} 个文件夹到 '{dst_dir}'。")
    print("=" * 60)

if __name__ == "__main__":
    move_extracted_folders(source_dir, destination_dir)