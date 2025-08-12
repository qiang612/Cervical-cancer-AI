from datetime import datetime
import os
from .user import db
from config import Config


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    format = db.Column(db.String(10), nullable=False)  # jpg, png, tiff, dcm等
    size = db.Column(db.Integer, nullable=False)  # 文件大小，字节
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        # 从 UPLOAD_FOLDER 的绝对路径中，提取出相对路径部分
        relative_path = os.path.relpath(self.file_path, Config.UPLOAD_FOLDER)
        # 将 Windows 的反斜杠 \ 替换为 URL 的正斜杠 /
        url_path = relative_path.replace('\\', '/')
        return {
            'id': self.id,
            'dataset_id': self.dataset_id,
            'filename': self.filename,
            'filePath': f'/uploads/{url_path}',
            'format': self.format,
            'size': self.size,
            'createdAt': self.created_at.isoformat()
        }

    def delete_file(self):
        """删除图片文件"""
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                return True
            except Exception as e:
                print(f"Error deleting file {self.file_path}: {str(e)}")
                return False
        return True
