from datetime import datetime
from .user import db


class DatasetShare(db.Model):
    __tablename__ = 'dataset_shares'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    permission = db.Column(db.String(20), nullable=False)  # view, edit, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 联合唯一约束
    __table_args__ = (
        db.UniqueConstraint('dataset_id', 'user_id', name='unique_dataset_user'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'dataset_id': self.dataset_id,
            'user_id': self.user_id,
            'username': self.user.username if hasattr(self, 'user') else None,
            'permission': self.permission,
            'created_at': self.created_at.isoformat()
        }
