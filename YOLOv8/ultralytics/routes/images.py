from flask import Blueprint, request, jsonify
from models.dataset import Dataset
from models.image import Image
from models.user import db
from utils.auth import token_required, has_dataset_permission
import os
import shutil
from werkzeug.utils import secure_filename

images_bp = Blueprint('images', __name__)


def allowed_file(filename):
    """检查文件是否是允许的格式"""
    from config import Config
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@images_bp.route('/datasets/<int:dataset_id>/images/batch', methods=['POST'])
@token_required
def batch_import_images(current_user, dataset_id):
    """批量导入图片到数据集"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)

        # 检查权限（需要edit权限）
        if not has_dataset_permission(dataset, current_user, 'edit'):
            return jsonify({'message': '没有上传图片到该数据集的权限'}), 403

        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'message': '没有文件被上传'}), 400

        files = request.files.getlist('file')
        if not files or all(file.filename == '' for file in files):
            return jsonify({'message': '没有选择文件'}), 400

        # 准备存储路径
        from config import Config
        dataset_folder = os.path.join(Config.UPLOAD_FOLDER, str(dataset_id))
        os.makedirs(dataset_folder, exist_ok=True)

        uploaded_images = []

        for file in files:
            if file and allowed_file(file.filename):
                # 安全处理文件名
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()

                # 检查文件是否已存在
                file_path = os.path.join(dataset_folder, filename)
                counter = 1
                while os.path.exists(file_path):
                    # 如果文件已存在，添加计数器
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{counter}{ext}"
                    file_path = os.path.join(dataset_folder, filename)
                    counter += 1

                # 保存文件
                file.save(file_path)

                # 获取文件大小
                file_size = os.path.getsize(file_path)

                # 创建图片记录
                image = Image(
                    dataset_id=dataset_id,
                    filename=filename,
                    file_path=file_path,
                    format=file_ext,
                    size=file_size
                )

                db.session.add(image)
                uploaded_images.append(image.to_dict())

        db.session.commit()

        return jsonify({
            'message': f'成功上传 {len(uploaded_images)} 张图片',
            'images': uploaded_images
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'上传图片失败: {str(e)}'}), 500


@images_bp.route('/datasets/<int:dataset_id>/images/<int:image_id>', methods=['DELETE'])
@token_required
def delete_image(current_user, dataset_id, image_id):
    """删除数据集中的单张图片"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        image = Image.query.filter_by(id=image_id, dataset_id=dataset_id).first_or_404()

        # 检查权限（需要edit权限）
        if not has_dataset_permission(dataset, current_user, 'edit'):
            return jsonify({'message': '没有删除该图片的权限'}), 403

        # 删除文件
        if not image.delete_file():
            return jsonify({'message': '删除图片文件失败，但数据库记录已更新'}), 200

        # 删除数据库记录
        db.session.delete(image)
        db.session.commit()

        return jsonify({'message': '图片已成功删除'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'删除图片失败: {str(e)}'}), 500


@images_bp.route('/datasets/<int:dataset_id>/images/copy', methods=['POST'])
@token_required
def copy_images(current_user, dataset_id):
    """复制图片到其他数据集"""
    try:
        source_dataset = Dataset.query.get_or_404(dataset_id)

        # 检查源数据集权限
        if not has_dataset_permission(source_dataset, current_user):
            return jsonify({'message': '没有访问源数据集的权限'}), 403

        data = request.get_json()

        if 'targetDatasetId' not in data or 'imageIds' not in data:
            return jsonify({'message': '缺少目标数据集ID或图片ID列表'}), 400

        target_dataset_id = data['targetDatasetId']
        image_ids = data['imageIds']

        # 检查目标数据集
        target_dataset = Dataset.query.get_or_404(target_dataset_id)

        # 检查目标数据集权限（需要edit权限）
        if not has_dataset_permission(target_dataset, current_user, 'edit'):
            return jsonify({'message': '没有向目标数据集添加图片的权限'}), 403

        # 检查源数据集和目标数据集是否相同
        if source_dataset.id == target_dataset.id:
            return jsonify({'message': '源数据集和目标数据集不能相同'}), 400

        # 准备目标文件夹
        from config import Config
        target_folder = os.path.join(Config.UPLOAD_FOLDER, str(target_dataset_id))
        os.makedirs(target_folder, exist_ok=True)

        # 获取要复制的图片
        images = Image.query.filter(
            Image.id.in_(image_ids),
            Image.dataset_id == dataset_id
        ).all()

        if not images:
            return jsonify({'message': '没有找到要复制的图片'}), 404

        copied_images = []

        # 复制图片
        for image in images:
            # 构建目标路径
            filename = image.filename
            target_path = os.path.join(target_folder, filename)

            # 处理文件名冲突
            counter = 1
            while os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{counter}{ext}"
                target_path = os.path.join(target_folder, filename)
                counter += 1

            # 复制文件
            if os.path.exists(image.file_path):
                shutil.copy2(image.file_path, target_path)

                # 创建新图片记录
                new_image = Image(
                    dataset_id=target_dataset_id,
                    filename=filename,
                    file_path=target_path,
                    format=image.format,
                    size=image.size
                )

                db.session.add(new_image)
                copied_images.append(new_image.to_dict())

        db.session.commit()

        return jsonify({
            'message': f'成功复制 {len(copied_images)} 张图片到目标数据集',
            'images': copied_images
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'复制图片失败: {str(e)}'}), 500
