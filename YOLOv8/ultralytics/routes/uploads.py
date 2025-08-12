# routes/uploads.py

from flask import Blueprint, send_from_directory
from config import Config

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    """
    提供对上传文件的访问。
    例如: /uploads/1/image.jpg 将会从 UPLOAD_FOLDER/1/image.jpg 提供文件
    """
    return send_from_directory(Config.UPLOAD_FOLDER, filename)