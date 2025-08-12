# routes/auth.py

from flask import Blueprint, request, jsonify
from models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "用户名和密码不能为空"}), 400

        # 从数据库查找用户
        user = User.query.filter_by(username=username).first()

        # 验证用户和密码
        if user and user.check_password(password):
            # 密码正确，生成JWT
            # 'identity' 可以存储用户ID或其他唯一标识
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            # 用户不存在或密码错误
            return jsonify({"message": "用户名或密码错误"}), 401

    except Exception as e:
        return jsonify({'message': f'登录时发生错误: {str(e)}'}), 500