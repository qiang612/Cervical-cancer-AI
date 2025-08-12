# utils/auth.py

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import decode_token
from models.user import User
from models.share import DatasetShare

def token_required(f):
    """
    装饰器：验证请求中的JWT令牌
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # ## FINAL FIX: 如果是 OPTIONS 预检请求，直接放行 ##
        if request.method == 'OPTIONS':
            return jsonify({'message': 'Preflight request successful'}), 200

        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': '认证令牌缺失！'}), 401

        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            current_user = User.query.get(user_id)

            if not current_user:
                raise Exception('用户不存在')

        except Exception as e:
            return jsonify({'message': f'认证失败: {str(e)}'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# ... (has_dataset_permission 函数保持不变) ...
def has_dataset_permission(dataset, user, required_permission='view'):
    if dataset.owner_id == user.id:
        return True
    permission_levels = {'view': 1, 'edit': 2, 'admin': 3}
    required_level = permission_levels.get(required_permission, 1)
    share = DatasetShare.query.filter_by(
        dataset_id=dataset.id,
        user_id=user.id
    ).first()
    if not share:
        return False
    user_level = permission_levels.get(share.permission, 0)
    return user_level >= required_level