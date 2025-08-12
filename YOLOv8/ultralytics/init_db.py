# init_db.py

from app import create_app
from extensions import db

print("正在创建数据库表...")

# 创建一个应用实例并推入上下文
app = create_app()
with app.app_context():
    # 创建所有定义的表
    db.create_all()

print("数据库表创建成功！")