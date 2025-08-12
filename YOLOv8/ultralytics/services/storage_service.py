import os
import uuid
import base64
import cv2
from config import Config


class StorageService:
    @staticmethod
    def get_patient_image_path(patient_id):
        """获取患者图片的路径"""
        return os.path.join(Config.PATIENT_DATA_DIR, f"{patient_id}.jpg")

    @staticmethod
    def patient_image_exists(patient_id):
        """检查患者图片是否存在"""
        image_path = StorageService.get_patient_image_path(patient_id)
        return os.path.exists(image_path)

    @staticmethod
    def save_dataset_image(dataset_id, file, patient_id=None):
        """
        保存数据集中的图片

        参数:
            dataset_id: 数据集ID
            file: 上传的文件对象
            patient_id: 可选的患者ID

        返回:
            包含图片ID、文件名和文件路径的字典
        """
        # 生成唯一ID和文件名
        image_id = str(uuid.uuid4())
        filename = f"{image_id}_{file.filename}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

        # 保存文件
        file.save(file_path)

        return {
            'image_id': image_id,
            'filename': file.filename,
            'file_path': file_path,
            'patient_id': patient_id
        }

    @staticmethod
    def image_to_base64(image):
        """将OpenCV图像转换为base64编码"""
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')
