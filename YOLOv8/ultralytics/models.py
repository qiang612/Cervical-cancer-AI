from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    datasets = db.relationship('Dataset', backref='owner', lazy=True)


class Dataset(db.Model):
    """数据集模型"""
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_count = db.Column(db.Integer, default=0)

    # 关系
    images = db.relationship('DatasetImage', backref='dataset', lazy=True, cascade="all, delete-orphan")


class DatasetImage(db.Model):
    """数据集中的图片模型"""
    id = db.Column(db.String(36), primary_key=True)
    dataset_id = db.Column(db.String(36), db.ForeignKey('dataset.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.String(50))  # 关联的患者ID
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255), nullable=False)
