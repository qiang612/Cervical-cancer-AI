from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import shutil
from werkzeug.utils import secure_filename

from extensions import db
from models.dataset import Dataset
from models.image import Image
from models.share import DatasetShare
from models.user import User
from utils.auth import token_required, has_dataset_permission

datasets_bp = Blueprint('datasets', __name__)

# --- 数据集列表和创建 ---
@datasets_bp.route('/datasets', methods=['GET'])
@token_required
def get_datasets(current_user):
    """获取数据集列表"""
    try:
        owned_datasets = Dataset.query.filter_by(owner_id=current_user.id).all()
        shares = DatasetShare.query.filter_by(user_id=current_user.id).all()
        shared_dataset_ids = [share.dataset_id for share in shares]
        shared_datasets = Dataset.query.filter(Dataset.id.in_(shared_dataset_ids)).all()
        all_datasets_map = {ds.id: ds for ds in owned_datasets}
        for ds in shared_datasets:
            if ds.id not in all_datasets_map:
                all_datasets_map[ds.id] = ds
        result = [ds.to_dict(current_user_id=current_user.id) for ds in all_datasets_map.values()]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'获取数据集失败: {str(e)}'}), 500

@datasets_bp.route('/datasets', methods=['POST'])
@token_required
def create_dataset(current_user):
    """创建新数据集"""
    try:
        data = request.get_json()
        new_dataset = Dataset(
            name=data.get('name'),
            task_type=data.get('taskType') or data.get('task_type'),
            image_type=data.get('imageType') or data.get('image_type'),
            description=data.get('description', ''),
            owner_id=current_user.id
        )
        db.session.add(new_dataset)
        db.session.commit()
        from config import Config
        dataset_folder = os.path.join(Config.UPLOAD_FOLDER, str(new_dataset.id))
        os.makedirs(dataset_folder, exist_ok=True)
        return jsonify(new_dataset.to_dict(current_user_id=current_user.id)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'创建数据集失败: {str(e)}'}), 500

# --- 数据集详情、更新、删除 ---
@datasets_bp.route('/datasets/<int:dataset_id>', methods=['GET'])
@token_required
def get_dataset_details(current_user, dataset_id):
    """获取数据集详情"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(dataset, current_user):
            return jsonify({'message': '没有访问该数据集的权限'}), 403
        return jsonify(dataset.to_dict(include_images=True, current_user_id=current_user.id)), 200
    except Exception as e:
        return jsonify({'message': f'获取数据集详情失败: {str(e)}'}), 500

@datasets_bp.route('/datasets/<int:dataset_id>', methods=['PUT'])
@token_required
def update_dataset(current_user, dataset_id):
    """更新数据集信息"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(dataset, current_user, 'edit'):
            return jsonify({'message': '没有编辑该数据集的权限'}), 403
        data = request.get_json()
        dataset.name = data.get('name', dataset.name)
        dataset.task_type = data.get('taskType') or data.get('task_type', dataset.task_type)
        dataset.image_type = data.get('imageType') or data.get('image_type', dataset.image_type)
        dataset.description = data.get('description', dataset.description)
        dataset.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(dataset.to_dict(include_images=True, current_user_id=current_user.id)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新数据集失败: {str(e)}'}), 500

@datasets_bp.route('/datasets/<int:dataset_id>', methods=['DELETE'])
@token_required
def delete_dataset(current_user, dataset_id):
    """删除数据集"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if dataset.owner_id != current_user.id:
            return jsonify({'message': '只有所有者可以删除数据集'}), 403
        from config import Config
        dataset_folder = os.path.join(Config.UPLOAD_FOLDER, str(dataset_id))
        if os.path.exists(dataset_folder):
            shutil.rmtree(dataset_folder)
        db.session.delete(dataset)
        db.session.commit()
        return jsonify({'message': '数据集已成功删除'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'删除数据集失败: {str(e)}'}), 500

# --- 数据集操作：复制、迁移、分享 ---
@datasets_bp.route('/datasets/<int:dataset_id>/copy', methods=['POST'])
@token_required
def copy_dataset(current_user, dataset_id):
    """复制数据集"""
    try:
        source_dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(source_dataset, current_user):
            return jsonify({'message': '没有访问源数据集的权限'}), 403
        new_dataset = Dataset(
            name=f"{source_dataset.name}_copy",
            task_type=source_dataset.task_type,
            image_type=source_dataset.image_type,
            description=f"复制自 {source_dataset.name}",
            owner_id=current_user.id
        )
        db.session.add(new_dataset)
        db.session.commit()
        from config import Config
        new_folder = os.path.join(Config.UPLOAD_FOLDER, str(new_dataset.id))
        os.makedirs(new_folder, exist_ok=True)
        for image in source_dataset.images:
            dest_path = os.path.join(new_folder, image.filename)
            if os.path.exists(image.file_path):
                shutil.copy2(image.file_path, dest_path)
                new_image = Image(dataset_id=new_dataset.id, filename=image.filename, file_path=dest_path, format=image.format, size=image.size)
                db.session.add(new_image)
        db.session.commit()
        return jsonify(new_dataset.to_dict(current_user_id=current_user.id)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'复制数据集失败: {str(e)}'}), 500

@datasets_bp.route('/datasets/<int:dataset_id>/move', methods=['POST'])
@token_required
def move_dataset(current_user, dataset_id):
    """迁移数据集（更改任务类型）"""
    try:
        source_dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(source_dataset, current_user, 'edit'):
            return jsonify({'message': '没有迁移该数据集的权限'}), 403
        data = request.get_json()
        new_task_type = data.get('newTaskType')
        if not new_task_type: return jsonify({'message': '缺少新任务类型参数'}), 400
        new_name = data.get('newName', f"{source_dataset.name}_{new_task_type}")
        new_dataset = Dataset(name=new_name, task_type=new_task_type, image_type=source_dataset.image_type, description=f"迁移自 {source_dataset.name}", owner_id=current_user.id)
        db.session.add(new_dataset)
        db.session.commit()
        from config import Config
        new_folder = os.path.join(Config.UPLOAD_FOLDER, str(new_dataset.id))
        os.makedirs(new_folder, exist_ok=True)
        for image in source_dataset.images:
            dest_path = os.path.join(new_folder, image.filename)
            if os.path.exists(image.file_path):
                shutil.copy2(image.file_path, dest_path)
                new_image = Image(dataset_id=new_dataset.id, filename=image.filename, file_path=dest_path, format=image.format, size=image.size)
                db.session.add(new_image)
        db.session.commit()
        return jsonify(new_dataset.to_dict(current_user_id=current_user.id)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'迁移数据集失败: {str(e)}'}), 500


@datasets_bp.route('/datasets/<int:dataset_id>/share', methods=['POST'])
@token_required
def share_dataset(current_user, dataset_id):
    """分享数据集给其他用户"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if dataset.owner_id != current_user.id:
            return jsonify({'message': '只有所有者可以分享数据集'}), 403
        data = request.get_json()
        user_id, permission = data.get('userId'), data.get('permission')
        if not user_id or not permission:
            return jsonify({'message': '缺少用户ID或权限参数'}), 400
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        if user.id == current_user.id:
            return jsonify({'message': '不能分享给你自己'}), 400
        valid_permissions = ['view', 'edit', 'admin']
        if permission not in valid_permissions:
            return jsonify({'message': '无效的权限类型'}), 400
        share = DatasetShare.query.filter_by(dataset_id=dataset_id, user_id=user_id).first()
        if share:
            share.permission = permission
        else:
            share = DatasetShare(dataset_id=dataset_id, user_id=user_id, permission=permission)
            db.session.add(share)
        db.session.commit()
        return jsonify({'message': f'数据集已成功分享给 {user.username}', 'share': share.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'分享数据集失败: {str(e)}'}), 500

# --- 图片相关路由 ---
def allowed_file(filename):
    """检查文件是否是允许的格式"""
    from config import Config
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@datasets_bp.route('/datasets/<int:dataset_id>/images/batch', methods=['POST'])
@token_required
def batch_import_images(current_user, dataset_id):
    """批量导入图片到数据集"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(dataset, current_user, 'edit'):
            return jsonify({'message': '您没有权限上传图片到该数据集'}), 403
        if 'file' not in request.files: return jsonify({'message': '请求中没有文件部分'}), 400
        files = request.files.getlist('file')
        if not files or all(f.filename == '' for f in files): return jsonify({'message': '没有选择任何文件'}), 400
        from config import Config
        dataset_folder = os.path.join(Config.UPLOAD_FOLDER, str(dataset_id))
        os.makedirs(dataset_folder, exist_ok=True)
        uploaded_images = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(dataset_folder, filename)
                counter = 1
                while os.path.exists(file_path):
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{counter}{ext}"
                    file_path = os.path.join(dataset_folder, filename)
                    counter += 1
                file.save(file_path)
                file_size = os.path.getsize(file_path)
                image = Image(dataset_id=dataset_id, filename=filename, file_path=file_path, format=filename.rsplit('.', 1)[1].lower(), size=file_size)
                db.session.add(image)
                uploaded_images.append(image)
        db.session.commit()
        images_dict = [img.to_dict() for img in uploaded_images]
        return jsonify({'message': f'成功上传 {len(images_dict)} 张图片', 'images': images_dict}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'上传图片失败: {str(e)}'}), 500

@datasets_bp.route('/datasets/<int:dataset_id>/images/<int:image_id>', methods=['DELETE'])
@token_required
def delete_image(current_user, dataset_id, image_id):
    """删除数据集中的单张图片"""
    try:
        dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(dataset, current_user, 'edit'):
            return jsonify({'message': '没有删除该图片的权限'}), 403
        image = Image.query.filter_by(id=image_id, dataset_id=dataset_id).first_or_404()
        if hasattr(image, 'delete_file') and callable(getattr(image, 'delete_file')):
            image.delete_file()
        elif os.path.exists(image.file_path):
            os.remove(image.file_path)
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': '图片已成功删除'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'删除图片失败: {str(e)}'}), 500

@datasets_bp.route('/datasets/<int:dataset_id>/images/copy', methods=['POST'])
@token_required
def copy_images(current_user, dataset_id):
    """复制图片到其他数据集"""
    try:
        source_dataset = Dataset.query.get_or_404(dataset_id)
        if not has_dataset_permission(source_dataset, current_user):
            return jsonify({'message': '没有访问源数据集的权限'}), 403
        data = request.get_json()
        target_dataset_id, image_ids = data.get('targetDatasetId'), data.get('imageIds')
        if not target_dataset_id or not image_ids: return jsonify({'message': '缺少目标数据集ID或图片ID列表'}), 400
        target_dataset = Dataset.query.get_or_404(target_dataset_id)
        if not has_dataset_permission(target_dataset, current_user, 'edit'):
            return jsonify({'message': '没有向目标数据集添加图片的权限'}), 403
        if source_dataset.id == target_dataset.id: return jsonify({'message': '源数据集和目标数据集不能相同'}), 400
        from config import Config
        target_folder = os.path.join(Config.UPLOAD_FOLDER, str(target_dataset_id))
        os.makedirs(target_folder, exist_ok=True)
        images = Image.query.filter(Image.id.in_(image_ids), Image.dataset_id == dataset_id).all()
        if not images: return jsonify({'message': '没有找到要复制的图片'}), 404
        copied_images = []
        for image in images:
            filename = image.filename
            target_path = os.path.join(target_folder, filename)
            counter = 1
            while os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{counter}{ext}"
                target_path = os.path.join(target_folder, filename)
                counter += 1
            if os.path.exists(image.file_path):
                shutil.copy2(image.file_path, target_path)
                new_image = Image(dataset_id=target_dataset_id, filename=filename, file_path=target_path, format=image.format, size=image.size)
                db.session.add(new_image)
                copied_images.append(new_image)
        db.session.commit()
        images_dict = [img.to_dict() for img in copied_images]
        return jsonify({'message': f'成功复制 {len(images_dict)} 张图片到目标数据集', 'images': images_dict}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'复制图片失败: {str(e)}'}), 500