from datetime import datetime
from .user import db


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # detection, classification, segmentation, pose
    image_type = db.Column(db.String(50), nullable=False)  # xray, ct, pathology, ultrasound
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    images = db.relationship('Image', backref='dataset', lazy=True, cascade="all, delete-orphan")
    shares = db.relationship('DatasetShare', backref='dataset', lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_images=False, current_user_id=None):
        data = {
            'id': self.id,
            'name': self.name,
            'taskType': self.task_type,
            'imageType': self.image_type,
            'description': self.description,
            'ownerId': self.owner_id,
            'owner': self.owner.to_dict() if hasattr(self, 'owner') else None,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'imageCount': len(self.images),
            'isOwner': self.owner_id == current_user_id,
            'sharedWith': [share.to_dict() for share in self.shares] if hasattr(self, 'shares') else []
        }

        if include_images:
            data['images'] = [image.to_dict() for image in self.images]

        return data
