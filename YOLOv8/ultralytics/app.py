from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from route_handlers.dataset_routes import dataset_bp
from route_handlers.diagnosis_routes import diagnosis_bp


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)

    # 配置应用
    app.config.from_object(Config)

    # 确保目录存在
    Config.ensure_directories()

    # 初始化扩展
    CORS(app)  # 允许跨域请求
    db.init_app(app)
    JWTManager(app)

    # 注册蓝图
    app.register_blueprint(dataset_bp)
    app.register_blueprint(diagnosis_bp)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
