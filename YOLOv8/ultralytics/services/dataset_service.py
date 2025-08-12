# services/dataset_service.py

import os
from datetime import datetime
import shutil

# ## FIX: 从中央 extensions.py 导入 db，并分别导入模型 ##
from extensions import db
from models.dataset import Dataset
from models.image import Image
# ## NOTE: StorageService 是您项目中的一个依赖，这里保留导入 ##
from services.storage_service import StorageService
from config import Config


class DatasetService:
    @staticmethod
    def create_dataset(user_id, name, task_type="Detection", image_type="TCT", description=""):
        """
        创建新数据集
        """
        # ## FIX: 查询数据库时使用 owner_id 而不是 user_id ##
        if Dataset.query.filter_by(name=name, owner_id=user_id).first(): #
            raise ValueError("该名称的数据集已存在")

        # 创建数据集记录
        new_dataset = Dataset(
            # ## DELETED: 移除 id=str(os.urandom(16).hex()) ##
            # 数据库模型 id 是自增整数，应由数据库自动生成。
            name=name,
            description=description,
            task_type=task_type,
            image_type=image_type,
            owner_id=user_id, #
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_dataset)
        db.session.commit()

        # 创建数据集目录结构
        # ## NOTE: 此处的 new_dataset.id 在 commit 后才能获取到数据库生成的值 ##
        dataset_dir = os.path.join(Config.UPLOAD_FOLDER, "datasets", str(new_dataset.id))
        subdirs = [
            os.path.join(dataset_dir, "images", "train"),
            os.path.join(dataset_dir, "images", "val"),
            os.path.join(dataset_dir, "labels", "train"),
            os.path.join(dataset_dir, "labels", "val")
        ]
        for subdir in subdirs:
            os.makedirs(subdir, exist_ok=True)

        return new_dataset

    @staticmethod
    def get_user_datasets(user_id):
        """获取用户的所有数据集"""
        # ## FIX: 查询数据库时使用 owner_id 而不是 user_id ##
        return Dataset.query.filter_by(owner_id=user_id).order_by(Dataset.created_at.desc()).all() #

    @staticmethod
    def get_dataset_by_id(dataset_id, user_id):
        """获取指定ID的数据集（带权限校验）"""
        # ## FIX: 查询数据库时使用 owner_id 而不是 user_id ##
        return Dataset.query.filter_by(id=dataset_id, owner_id=user_id).first() #

    @staticmethod
    def delete_dataset(dataset_id, user_id):
        """删除数据集（包括关联图片和文件）"""
        dataset = DatasetService.get_dataset_by_id(dataset_id, user_id)
        if not dataset:
            raise ValueError("数据集不存在或无权限")

        # ## FIX: 使用正确的模型名 Image ##
        images = Image.query.filter_by(dataset_id=dataset_id).all()
        for image in images:
            if os.path.exists(image.file_path):
                os.remove(image.file_path)
            db.session.delete(image)

        # 删除数据集目录
        dataset_dir = os.path.join(Config.UPLOAD_FOLDER, "datasets", str(dataset_id))
        if os.path.exists(dataset_dir):
            shutil.rmtree(dataset_dir, ignore_errors=True)

        # 删除数据集记录
        db.session.delete(dataset)
        db.session.commit()
        return True

    @staticmethod
    def add_image_to_dataset(dataset_id, user_id, file, patient_id=None):
        """向数据集中添加图片"""
        dataset = DatasetService.get_dataset_by_id(dataset_id, user_id)
        if not dataset:
            raise ValueError("数据集不存在或无权限")

        # ## NOTE: 此处依赖 StorageService，请确保其实现正确 ##
        storage_result = StorageService.save_dataset_image(
            dataset_id=dataset_id,
            file=file,
            patient_id=patient_id
        )

        # ## FIX: 使用正确的模型名 Image，并只传入模型中存在的字段 ##
        new_image = Image(
            # id 由数据库自增
            dataset_id=dataset_id,
            filename=storage_result["filename"],
            file_path=storage_result["file_path"],
            # ## NOTE: 以下字段根据 image.py 模型定义进行修正 ##
            format=storage_result["filename"].rsplit('.', 1)[1].lower(), # [cite: 6]
            size=os.path.getsize(storage_result["file_path"]) # [cite: 6]
        )
        db.session.add(new_image)
        db.session.commit()
        return new_image