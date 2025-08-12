import uuid
from app import create_app
from models import db, User

def add_default_user():
    """
    创建一个默认的管理员用户，如果他不存在的话。
    """
    # 我们预设的用户名和密码
    USERNAME = 'admin'
    PASSWORD = 'admin'

    app = create_app()
    with app.app_context():
        # 检查用户是否已存在
        if User.query.filter_by(username=USERNAME).first():
            print(f"用户 '{USERNAME}' 已存在。")
            return

        # 创建新用户
        print(f"正在创建默认用户: {USERNAME}...")
        user_id = str(uuid.uuid4())
        default_user = User(id=user_id, username=USERNAME)
        default_user.set_password(PASSWORD)  # 使用 set_password 来加密

        db.session.add(default_user)
        db.session.commit()
        print(f"用户 '{USERNAME}' 创建成功！")

if __name__ == '__main__':
    add_default_user()