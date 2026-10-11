import os
import subprocess
import shutil

# 1. 7z.exe 路径（已更新为你提供的路径）
SEVEN_ZIP_PATH = r"D:\application\7-Zip\7z.exe"


def extract_single_archive(archive_path, output_dir, target_move_dir, passwords):
    """
    尝试解压，成功后将解压出来的文件夹移动到指定的目标目录
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📦 开始处理压缩包: {archive_path}")

    for idx, pwd in enumerate(passwords, start=1):
        print(f"  ⏳ [尝试 {idx}/{len(passwords)}] 密码: '{pwd}' ...", end="", flush=True)

        cmd = [
            SEVEN_ZIP_PATH, "x",
            archive_path,
            f"-p{pwd}",
            f"-o{output_dir}",
            "-y"
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f" -> 🎉 解压成功！密码: '{pwd}'")

            # 确定移动的目标路径
            folder_name = os.path.basename(output_dir)
            final_path = os.path.join(target_move_dir, folder_name)

            # 如果目标文件夹已存在同名目录，先清理避免覆盖报错
            if os.path.exists(final_path):
                shutil.rmtree(final_path)

            # 移动解压出来的文件夹
            shutil.move(output_dir, target_move_dir)
            print(f"  🚚 已将解压结果移动到: {final_path}")
            return True
        else:
            print(" -> ❌ 失败")

    # 如果所有密码均失败，清理临时建的空文件夹
    if os.path.exists(output_dir) and not os.listdir(output_dir):
        os.rmdir(output_dir)

    print(f"❌ 无法解压文件: {archive_path}")
    return False


def batch_extract_and_move(scan_directory, target_move_directory, candidate_passwords):
    """
    扫描目录：
    - pdf, rar, zip, 7z：尝试 7z 碰撞解压，成功后移动解压文件夹
    - mp4：免解压，直接当作成品移动/复制到目标文件夹
    """
    if not os.path.exists(SEVEN_ZIP_PATH):
        print(f"❌ 错误：找不到 7z.exe，请检查路径: '{SEVEN_ZIP_PATH}'")
        return

    # 创建用于存放解压及 MP4 结果的目标文件夹
    os.makedirs(target_move_directory, exist_ok=True)

    # 判定集合
    archive_extensions = ('.pdf', '.rar', '.zip', '.7z')
    all_extensions = ('.pdf', '.rar', '.zip', '.7z', '.mp4')

    print("=" * 60)
    print(f"🔍 扫描目录: {scan_directory}")
    print(f"📂 目标存放位置: {target_move_directory}")
    print("=" * 60)

    success_count = 0
    total_found = 0

    for root, dirs, files in os.walk(scan_directory):
        for file in files:
            file_clean = file.strip()
            file_lower = file_clean.lower()

            # 1. 拦截处理 MP4 文件（直接当做成品移动）
            if file_lower.endswith('.mp4'):
                total_found += 1
                file_path = os.path.join(root, file)
                dest_file_path = os.path.join(target_move_directory, file)

                print(f"\n🎥 发现 MP4 视频文件（直接转存）: {file_path}")

                # 如果目标文件夹已存在同名 mp4，先覆盖/删除旧的
                if os.path.exists(dest_file_path):
                    os.remove(dest_file_path)

                # 移动文件（如果想保留原文件可将 move 改为 copy2）
                shutil.move(file_path, dest_file_path)
                print(f"  🚚 已直接移动 MP4 至: {dest_file_path}")
                success_count += 1

            # 2. 处理常规/伪装压缩包文件
            elif file_lower.endswith(archive_extensions):
                total_found += 1
                archive_path = os.path.join(root, file)

                # 临时解压输出目录
                file_name_without_ext = os.path.splitext(file)[0]
                temp_output_folder = os.path.join(root, f"{file_name_without_ext}_extracted")

                # 执行解压并移动
                is_success = extract_single_archive(
                    archive_path, temp_output_folder, target_move_directory, candidate_passwords
                )
                if is_success:
                    success_count += 1

    print("\n" + "=" * 60)
    print(f"📊 完成！共处理 {total_found} 个文件（含 MP4），成功解压/移交 {success_count} 个。")
    print("=" * 60)


if __name__ == "__main__":
    # 1. 待扫描的目标文件夹
    scan_dir = r"D:/python_test/sex"

    # 2. 统一保存的目标文件夹
    destination_dir = r"D:/python_test/all_extracted_files"

    # 3. 密码列表
    passwords = [
        "lovelily",
        "lovelili",
        "lililove",
        "lililovesmenot",
        "Ilovelilinomore"
    ]

    # 开始执行
    batch_extract_and_move(scan_dir, destination_dir, passwords)