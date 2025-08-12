# routes/uploads.py
from flask import Blueprint, send_from_directory
from config import Config
import os

uploads_bp = Blueprint('uploads', __name__)

# 使用更灵活的路由来处理嵌套目录
@uploads_bp.route('/uploads/<path:subpath>')
def serve_upload(subpath):
    """提供对上传文件的访问"""
    # send_from_directory 会安全地处理路径
    return send_from_directory(Config.UPLOAD_FOLDER, subpath)