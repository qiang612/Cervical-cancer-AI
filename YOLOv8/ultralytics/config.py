import os
from datetime import timedelta


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_datasets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT配置
    JWT_SECRET_KEY = 'your-secret-key-here'  # 生产环境需更换
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # 路径配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    PATIENT_DATA_DIR = os.path.join(BASE_DIR, 'patient_data')

    # 文件上传限制
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    # 模型路径
    MODEL_PATH = os.path.join(BASE_DIR, 'runs/detect/cervical_train2/weights/best.pt')

    # 确保目录存在
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PATIENT_DATA_DIR, exist_ok=True)
