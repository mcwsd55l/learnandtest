#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import shutil
from pathlib import Path


def unique_target(dst: Path, filename: str, overwrite: bool = False) -> Path:
    """生成不冲突的目标路径；overwrite=True 时直接使用原名。"""
    target = dst / filename
    if overwrite or not target.exists():
        return target

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    i = 1
    while True:
        candidate = dst / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def flatten_folder(src: Path, dst: Path, move: bool = False, overwrite: bool = False):
    src = src.resolve()
    dst = dst.resolve()

    if not src.exists():
        raise FileNotFoundError(f"源文件夹不存在: {src}")
    if not src.is_dir():
        raise NotADirectoryError(f"源路径不是文件夹: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    # 判断目标文件夹是否在源文件夹内部
    dst_inside_src = (dst == src) or (src in dst.parents)

    # 先收集所有文件，避免边遍历边移动导致遍历混乱
    files = []
    for p in src.rglob("*"):
        if not p.is_file():
            continue

        # 如果目标就是源目录，根目录下的文件已经在目标位置，跳过
        if p.parent == dst:
            continue

        # 如果目标目录在源目录内部，跳过目标目录里的文件，避免自己复制自己
        if dst_inside_src and dst != src and dst in p.parents:
            continue

        files.append(p)

    for f in files:
        target = unique_target(dst, f.name, overwrite)

        if overwrite and target.exists():
            target.unlink()

        if move:
            shutil.move(str(f), str(target))
        else:
            shutil.copy2(str(f), str(target))

    # 如果是移动模式，尝试删除源文件夹下已经变空的子文件夹
    if move:
        dirs = [p for p in src.rglob("*") if p.is_dir()]
        dirs.sort(key=lambda p: len(p.parts), reverse=True)

        for d in dirs:
            if dst_inside_src and dst != src and (d == dst or dst in d.parents):
                continue
            try:
                d.rmdir()
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="将源文件夹下所有子文件夹中的文件递归扁平化到一个目标文件夹。"
    )
    parser.add_argument("source", help="源文件夹")
    parser.add_argument("-d", "--dest", help="目标文件夹，默认与源文件夹相同")
    parser.add_argument("-m", "--move", action="store_true", help="移动文件（默认是复制）")
    parser.add_argument("--overwrite", action="store_true", help="同名文件直接覆盖（默认自动重命名）")

    args = parser.parse_args()

    src = Path(args.source)
    dst = Path(args.dest) if args.dest else src

    flatten_folder(src, dst, move=args.move, overwrite=args.overwrite)
    print("完成。")


if __name__ == "__main__":
    main()