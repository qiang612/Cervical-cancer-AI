import cv2
import os
import numpy as np
from config import Config
from services.storage_service import StorageService


class ImageService:
    @staticmethod
    def validate_image(file):
        """
        验证上传的文件是否为有效的图片

        参数:
            file: 上传的文件对象

        返回:
            验证通过返回True，否则抛出异常
        """
        # 检查文件扩展名
        allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise ValueError("不支持的图片格式，仅支持PNG、JPG、JPEG、BMP")

        # 检查文件大小（不超过配置的最大值）
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # 重置文件指针
        if file_size > Config.MAX_CONTENT_LENGTH:
            max_size_mb = Config.MAX_CONTENT_LENGTH / (1024 * 1024)
            raise ValueError(f"图片大小超过限制，最大支持{max_size_mb}MB")

        return True

    @staticmethod
    def preprocess_image(image_path, target_size=(640, 640)):
        """
        预处理图片（用于模型输入）

        参数:
            image_path: 图片路径
            target_size: 目标尺寸 (width, height)

        返回:
            预处理后的图片（numpy数组）
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")

        # 缩放图片
        resized = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        # 转换为RGB（如果模型需要）
        rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        # 归一化（根据模型需求调整）
        normalized = rgb_image / 255.0
        return normalized

    @staticmethod
    def save_annotated_image(annotated_image, image_id):
        """
        保存模型标注后的图片

        参数:
            annotated_image: 标注后的图片（numpy数组，BGR格式）
            image_id: 图片唯一ID

        返回:
            保存的图片路径
        """
        # 创建标注图片存储目录
        annotated_dir = os.path.join(Config.UPLOAD_FOLDER, "annotated")
        os.makedirs(annotated_dir, exist_ok=True)

        # 生成保存路径
        save_path = os.path.join(annotated_dir, f"{image_id}_annotated.jpg")
        # 保存图片
        cv2.imwrite(save_path, annotated_image)
        return save_path

    @staticmethod
    def convert_to_base64(image_path):
        """将图片转换为base64编码（用于前端展示）"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")

        # 使用存储服务中的方法转换
        image = cv2.imread(image_path)
        return StorageService.image_to_base64(image)

    @staticmethod
    def crop_image(image_path, bbox):
        """
        根据边界框裁剪图片

        参数:
            image_path: 原始图片路径
            bbox: 边界框 (x1, y1, x2, y2)

        返回:
            裁剪后的图片（numpy数组）
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")

        x1, y1, x2, y2 = map(int, bbox)
        # 确保边界框在图片范围内
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.shape[1], x2)
        y2 = min(image.shape[0], y2)

        return image[y1:y2, x1:x2]