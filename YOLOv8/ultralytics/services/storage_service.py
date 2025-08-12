# services/storage_service.py

import os
import base64
import uuid
import cv2
from werkzeug.utils import secure_filename
from config import Config


class StorageService:
    @staticmethod
    def save_dataset_image(dataset_id, file, patient_id=None):
        """
        将上传的图片文件保存到文件系统。
        您需要在此处实现具体的文件保存逻辑。
        """
        # 1. 获取安全的文件名
        filename = secure_filename(file.filename)

        # 2. 定义保存路径
        #    注意：此处的目录结构应与您的 routes/images.py 中的逻辑保持一致
        dataset_folder = os.path.join(Config.UPLOAD_FOLDER, str(dataset_id))
        os.makedirs(dataset_folder, exist_ok=True)
        file_path = os.path.join(dataset_folder, filename)

        # 3. 处理文件名冲突 (如果需要)
        counter = 1
        while os.path.exists(file_path):
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{counter}{ext}"
            file_path = os.path.join(dataset_folder, new_filename)
            counter += 1

        # 4. 保存文件
        file.save(file_path)

        # 5. 返回包含文件信息的字典
        return {
            "image_id": str(uuid.uuid4()),  # 生成一个唯一的图片ID
            "filename": os.path.basename(file_path),
            "file_path": file_path
        }

    @staticmethod
    def image_to_base64(image):
        """
        将OpenCV图片对象(numpy array)转换为Base64编码的字符串。
        """
        # 将图片编码为.jpg格式的字节流
        _, buffer = cv2.imencode('.jpg', image)
        # 将字节流转换为Base64字符串
        return base64.b64encode(buffer).decode('utf-8')

    @staticmethod
    def get_patient_image_path(patient_id):
        """
        根据患者ID获取其原始图片的完整路径。
        您需要根据实际存储规则实现此逻辑。
        """
        # 示例逻辑：假设图片以 patient_id.jpg 的形式存储在 PATIENT_DATA_DIR 中
        filename = f"{patient_id}.jpg"
        return os.path.join(Config.PATIENT_DATA_DIR, filename)

    @staticmethod
    def patient_image_exists(patient_id):
        """
        检查指定患者的图片是否存在。
        """
        image_path = StorageService.get_patient_image_path(patient_id)
        return os.path.exists(image_path)