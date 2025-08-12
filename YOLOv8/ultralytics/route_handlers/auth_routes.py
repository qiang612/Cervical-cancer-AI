from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

# 建议将蓝图前缀统一为 /api
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "用户名已存在"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "用户注册成功"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "请输入用户名和密码"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # 【优化】使用 user.id 作为 JWT 的身份标识
        access_token = create_access_token(identity=user.id)

        # 【优化】同时返回 token 和用户信息
        return jsonify(
            access_token=access_token,
            user={
                'id': user.id,
                'username': user.username
            }
        )

    return jsonify({"msg": "用户名或密码错误"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """获取当前用户信息"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify(id=user.id, username=user.username)
    return jsonify({"msg": "未找到用户"}), 404
