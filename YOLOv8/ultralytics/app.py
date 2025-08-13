from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
from extensions import db

# 导入模型
from models.user import User

# 导入其他蓝图
from routes.datasets import datasets_bp
from routes.users import users_bp
from routes.diagnosis_routes import diagnosis_bp
from routes.uploads import uploads_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)
    db.init_app(app)
    JWTManager(app)

    @app.before_request
    def handle_preflight():
        if request.method.upper() == 'OPTIONS':
            return make_response()

    # ## FINAL FIX: 将登录和注册路由直接定义在 app 上 ##

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """用户登录接口"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({"message": "用户名和密码不能为空"}), 400

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                access_token = create_access_token(identity=user.id)

                # ## FIX: 在返回token的同时，也返回用户信息 ##
                # 我们使用之前定义好的 user.to_dict() 方法来获取用户信息
                return jsonify({
                    "accessToken": access_token,
                    "user": user.to_dict()
                }), 200
            else:
                return jsonify({"message": "用户名或密码错误"}), 401
        except Exception as e:
            return jsonify({'message': f'登录时发生错误: {str(e)}'}), 500

    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """用户注册接口"""
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            if not all([username, email, password]):
                return jsonify({"message": "用户名、邮箱和密码均不能为空"}), 400
            if User.query.filter_by(username=username).first():
                return jsonify({"message": "该用户名已被注册"}), 409
            if User.query.filter_by(email=email).first():
                return jsonify({"message": "该邮箱已被注册"}), 409
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "用户注册成功！"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'注册时发生错误: {str(e)}'}), 500

    # 注册其他蓝图
    app.register_blueprint(datasets_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(diagnosis_bp, url_prefix='/api')
    app.register_blueprint(uploads_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    # 建议暂时禁用 reloader，直到所有功能稳定
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)