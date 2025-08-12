import os
from datetime import timedelta


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dataset_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 图片存储路径
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))

    # 允许的图片格式
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff', 'dcm', 'gif'}

    # 最大上传文件大小 (10MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')  # 生产环境应更换为安全的密钥
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # 模型相关配置 - 新增/保留的部分
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.environ.get('MODEL_PATH',
                                os.path.join(BASE_DIR, 'runs/detect/cervical_train2/weights/best.pt'))
    PATIENT_DATA_DIR = os.environ.get('PATIENT_DATA_DIR',
                                      os.path.join(BASE_DIR, 'patient_data'))

    # 创建所需目录（如果不存在）
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PATIENT_DATA_DIR, exist_ok=True)