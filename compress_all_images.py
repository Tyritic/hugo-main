#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量压缩博客所有图片"""

import os
import sys
from pathlib import Path
from PIL import Image
import time

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def compress_image(image_path, quality=80, max_width=1920, backup=True, min_size_kb=100):
    """
    压缩单张图片

    Args:
        image_path: 图片路径
        quality: JPEG质量 (1-100)
        max_width: 最大宽度（保持宽高比）
        backup: 是否备份原文件
        min_size_kb: 最小处理文件大小（KB）

    Returns:
        (original_size, compressed_size, success)
    """
    try:
        original_size = os.path.getsize(image_path)

        # 跳过小文件
        if original_size < min_size_kb * 1024:
            return original_size, original_size, False

        # 备份原文件
        if backup:
            backup_path = str(image_path) + '.backup'
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(image_path, backup_path)

        img = Image.open(image_path)

        # 转换RGBA到RGB（PNG转JPG需要）
        if img.mode in ('RGBA', 'LA', 'P'):
            # 保持PNG格式以支持透明度
            if str(image_path).lower().endswith('.png'):
                # 优化PNG
                img.save(image_path, 'PNG', optimize=True, compress_level=9)
                new_size = os.path.getsize(image_path)
                return original_size, new_size, True
            else:
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

        # 调整尺寸（如果图片太大）
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # 保存压缩后的图片
        if str(image_path).lower().endswith('.png'):
            img.save(image_path, 'PNG', optimize=True, compress_level=9)
        else:
            img.save(image_path, 'JPEG', quality=quality, optimize=True)

        new_size = os.path.getsize(image_path)
        return original_size, new_size, True

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
        return 0, 0, False

def format_size(bytes_size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f}TB"

def find_all_images(root_dir='content/post'):
    """查找所有图片文件"""
    image_extensions = {'.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'}
    images = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if Path(file).suffix in image_extensions:
                full_path = os.path.join(root, file)
                # 跳过备份文件
                if not full_path.endswith('.backup'):
                    images.append(full_path)

    return images

def main():
    print("=" * 70)
    print("Batch Image Compression Tool")
    print("=" * 70)
    print()

    # 查找所有图片
    print("[1/4] Scanning images...")
    all_images = find_all_images('content/post')
    print(f"Found {len(all_images)} images")
    print()

    # 按大小排序，优先处理大文件
    print("[2/4] Analyzing file sizes...")
    image_info = []
    for img_path in all_images:
        size = os.path.getsize(img_path)
        image_info.append((img_path, size))

    image_info.sort(key=lambda x: x[1], reverse=True)

    # 统计信息
    total_size = sum(size for _, size in image_info)
    large_images = [img for img, size in image_info if size > 100 * 1024]

    print(f"Total size: {format_size(total_size)}")
    print(f"Images > 100KB: {len(large_images)} (will be processed)")
    print(f"Images < 100KB: {len(all_images) - len(large_images)} (will be skipped)")
    print()

    # 确认继续
    print("[3/4] Starting compression...")
    print(f"Quality: 80%, Max width: 1920px")
    print(f"Backup: Enabled (.backup suffix)")
    print()

    total_original = 0
    total_compressed = 0
    success_count = 0
    skip_count = 0
    error_count = 0

    start_time = time.time()

    for i, (img_path, original_size) in enumerate(image_info, 1):
        # 显示进度
        if i % 10 == 0 or i == len(image_info):
            progress = i / len(image_info) * 100
            print(f"Progress: {i}/{len(image_info)} ({progress:.1f}%)")

        original, compressed, success = compress_image(
            img_path,
            quality=80,
            max_width=1920,
            backup=True,
            min_size_kb=100
        )

        if success:
            reduction = ((original - compressed) / original * 100) if original > 0 else 0
            if reduction > 5:  # 只显示减少超过5%的
                print(f"  [OK] {Path(img_path).name}: {format_size(original)} -> {format_size(compressed)} (-{reduction:.1f}%)")
            total_original += original
            total_compressed += compressed
            success_count += 1
        elif original > 0:
            skip_count += 1
        else:
            error_count += 1

    elapsed_time = time.time() - start_time

    print()
    print("=" * 70)
    print("[4/4] Compression Summary")
    print("=" * 70)
    print(f"Processed: {success_count} images")
    print(f"Skipped: {skip_count} images (< 100KB)")
    print(f"Errors: {error_count} images")
    print()

    if total_original > 0:
        total_reduction = ((total_original - total_compressed) / total_original * 100)
        print(f"Total size: {format_size(total_original)} -> {format_size(total_compressed)}")
        print(f"Saved: {format_size(total_original - total_compressed)} ({total_reduction:.1f}%)")
        print()

    print(f"Time elapsed: {elapsed_time:.1f}s")
    print()
    print("Backup files created with .backup suffix")
    print("To restore: find content/post -name '*.backup' -exec bash -c 'mv \"$0\" \"${0%.backup}\"' {} \\;")
    print("=" * 70)

if __name__ == '__main__':
    main()
