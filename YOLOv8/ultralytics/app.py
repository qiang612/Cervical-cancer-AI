# app.py

from flask import Flask, request, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db

# 导入所有蓝图
from routes.datasets import datasets_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.diagnosis_routes import diagnosis_bp
from routes.uploads import uploads_bp # ## ADDED: 导入新的 uploads_bp

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)
    db.init_app(app)
    JWTManager(app)

    @app.before_request
    def handle_preflight():
        if request.method.upper() == 'OPTIONS':
            return make_response()

    # 注册所有蓝图
    app.register_blueprint(datasets_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(diagnosis_bp, url_prefix='/api')
    app.register_blueprint(uploads_bp)
    # ## DELETED: 移除这里的 with app.app_context() 和 db.create_all() ##

    # 移除调试路由（可选，但推荐）
    # @app.route('/debug/routes') ...

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)