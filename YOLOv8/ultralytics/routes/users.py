from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth import token_required


users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
@token_required
def search_users(current_user):
    """搜索用户（用于分享功能）"""
    try:
        query = request.args.get('search', '')

        if not query:
            return jsonify([]), 200

        # 搜索用户名或邮箱包含查询字符串的用户
        users = User.query.filter(
            (User.username.ilike(f'%{query}%')) |
            (User.email.ilike(f'%{query}%'))
        ).all()

        # 排除当前用户
        users = [user for user in users if user.id != current_user.id]

        return jsonify([{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users]), 200

    except Exception as e:
        return jsonify({'message': f'搜索用户失败: {str(e)}'}), 500
