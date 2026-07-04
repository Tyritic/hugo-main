#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量压缩博客图片"""

import os
import sys
from pathlib import Path
from PIL import Image

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def compress_image(image_path, quality=85, max_width=1920, backup=True):
    """
    压缩单张图片

    Args:
        image_path: 图片路径
        quality: JPEG质量 (1-100)
        max_width: 最大宽度（保持宽高比）
        backup: 是否备份原文件

    Returns:
        压缩前后的文件大小（字节）
    """
    try:
        original_size = os.path.getsize(image_path)

        # 跳过小文件
        if original_size < 500 * 1024:  # 小于500KB
            return original_size, original_size, False

        # 备份原文件
        if backup:
            backup_path = image_path + '.backup'
            import shutil
            shutil.copy2(image_path, backup_path)

        img = Image.open(image_path)

        # 转换RGBA到RGB（PNG转JPG需要）
        if img.mode in ('RGBA', 'LA', 'P'):
            # 保持PNG格式以支持透明度
            if image_path.lower().endswith('.png'):
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
        if image_path.lower().endswith('.png'):
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
    for unit in ['B', 'KB', 'MB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f}GB"

def main():
    # 大图片列表（超过700KB的）
    large_images = [
        "content/post/Agent的规划能力/new-complexities.png",
        "content/post/Agent的规划能力/other-methods.png",
        "content/post/Go的GMP机制/retake方法修改.png",
        "content/post/Go的内存管理和垃圾回收/image.png",
        "content/post/卷积神经网络/3c266da23107494b04b09683b8427f0e.png",
        "content/post/Agent的规划能力/multi-agent-system.png",
        "content/post/Go的GMP机制/gmp-find-runnable.png",
        "content/post/Agent的规划能力/single-agent-bottleneck.png",
        "content/post/Go的GMP机制/schedt修改.png",
        "content/post/Go的GMP机制/寻找g修改.png",
        "content/post/OpenSpec的概念与基本使用/ea52e0ee389511f1b9b8260bb3baec80.png",
        "content/post/Go的GMP机制/阻塞让渡修改.png",
        "content/post/Agent的记忆模块/1774526786451.png",
        "content/post/Agent的记忆模块/1774527085924.png",
        "content/post/Go的GMP机制/g0与g修改.png",
        "content/post/分片系统的通用框架/28f209cc-6566-11f1-96b4-463ce7757bbe.png",
        "content/post/分片系统的通用框架/77f19024-6566-11f1-b126-a27132688e95.png",
        "content/post/分片系统的通用框架/64e62b52-6566-11f1-8f47-d271581afbe2.png",
        "content/post/分片系统的通用框架/532b1832-6566-11f1-9fdf-6e86b87206bc.png"
    ]

    total_original = 0
    total_compressed = 0
    success_count = 0

    print("Starting image compression...")
    print("=" * 60)

    for img_path in large_images:
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue

        original, compressed, success = compress_image(img_path, quality=85, max_width=1920)

        if success:
            reduction = ((original - compressed) / original * 100) if original > 0 else 0
            print(f"[OK] {os.path.basename(img_path)}")
            print(f"  {format_size(original)} -> {format_size(compressed)} (reduce {reduction:.1f}%)")
            total_original += original
            total_compressed += compressed
            success_count += 1
        elif original > 0:
            print(f"[SKIP] {os.path.basename(img_path)} (file too small)")

    print("=" * 60)
    print(f"Compression completed: {success_count} images")
    if total_original > 0:
        total_reduction = ((total_original - total_compressed) / total_original * 100)
        print(f"Total size: {format_size(total_original)} -> {format_size(total_compressed)}")
        print(f"Saved: {format_size(total_original - total_compressed)} ({total_reduction:.1f}%)")

if __name__ == '__main__':
    main()
