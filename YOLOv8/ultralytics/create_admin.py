# create_admin.py

from app import create_app
# ## FIX: 从正确的模块导入 User 和 db ##
from models.user import User
from extensions import db


def add_default_user():
    """
    创建一个默认的管理员用户，如果他不存在的话。
    """
    USERNAME = 'admin1'
    PASSWORD = 'admin1'
    # ## NOTE: User 模型需要 email 字段，我们在这里提供一个默认值 ##
    EMAIL = 'admin1@example.com'

    # 1. 创建 Flask 应用实例
    app = create_app()

    # 2. 推入应用上下文，所有数据库操作都必须在此代码块内执行
    with app.app_context():
        # 检查用户是否已存在
        if User.query.filter_by(username=USERNAME).first():
            print(f"用户 '{USERNAME}' 已存在。")
            return

        # 创建新用户
        print(f"正在创建默认用户: {USERNAME}...")

        # 使用修正后的 User 模型创建实例 (ID自增, email必须)
        default_user = User(username=USERNAME, email=EMAIL)
        default_user.set_password(PASSWORD)  # 使用 set_password 来加密

        db.session.add(default_user)
        db.session.commit()
        print(f"用户 '{USERNAME}' 创建成功！")


if __name__ == '__main__':
    add_default_user()