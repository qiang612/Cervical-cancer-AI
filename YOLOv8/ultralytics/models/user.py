# models/user.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# ## ADDED: 从我们创建的中央 extensions.py 文件导入 db ##
from extensions import db

# ## DELETED: db = SQLAlchemy()  (必须删除这一行！)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    owned_datasets = db.relationship('Dataset', backref='owner', lazy=True, foreign_keys='Dataset.owner_id')
    shared_datasets = db.relationship('DatasetShare', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }