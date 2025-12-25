import os
from PIL import Image
from pillow_heif import register_heif_opener

# 注册 HEIF 支持
register_heif_opener()


def process_images():
    path = "."  # 当前路径

    # 1. 转换 HEIC 到 JPG
    print("正在转换 HEIC 文件...")
    for filename in os.listdir(path):
        if filename.lower().endswith(".heic"):
            file_path = os.path.join(path, filename)
            # 打开并转换
            image = Image.open(file_path)
            # 转换为 RGB 模式（JPG 不支持带有透明度的 RGBA）
            image = image.convert("RGB")

            # 生成新的文件名
            target_name = os.path.splitext(filename)[0] + ".jpg"
            image.save(os.path.join(path, target_name), "JPEG")

            # 删除原 HEIC 文件
            os.remove(file_path)
            print(f"已转换并删除: {filename}")

    # 2. 统一重命名所有 JPG 文件
    print("\n正在统一重命名...")
    # 获取所有 jpg 和 jpeg 文件
    jpg_files = [f for f in os.listdir(path) if f.lower().endswith((".jpg", ".jpeg"))]
    # 排序以保证命名的逻辑顺序
    jpg_files.sort()

    # 为了防止重命名冲突（例如 1.jpg 已存在），先重命名为临时名称
    temp_files = []
    for i, filename in enumerate(jpg_files, 1):
        old_path = os.path.join(path, filename)
        temp_name = f"temp_{i}_{filename}"
        os.rename(old_path, os.path.join(path, temp_name))
        temp_files.append(temp_name)

    # 最终正式命名
    for i, temp_name in enumerate(temp_files, 1):
        old_path = os.path.join(path, temp_name)
        new_name = f"{i}.jpg"
        os.rename(old_path, os.path.join(path, new_name))
        print(f"重命名: {temp_name} -> {new_name}")

    print("\n所有操作已完成！")


if __name__ == "__main__":
    process_images()
