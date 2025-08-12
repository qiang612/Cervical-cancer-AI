import os
import uuid
from flask import Blueprint, request, jsonify, make_response, current_app
# 统一使用 flask_login 进行认证
from flask_login import login_required, current_user
from models import db, Dataset, DatasetImage
from services.storage_service import StorageService

# 创建蓝图
# 注意：我在您的原始代码基础上，将 url_prefix 从 '/api/datasets' 改为了 '/api'
# 因为您的路由定义是 @dataset_bp.route('/datasets', ...)，如果前缀是/api/datasets，
# 最终URL会变成 /api/datasets/datasets，这可能是个错误。如果您的本意就是如此，可以改回去。
dataset_bp = Blueprint('dataset', __name__, url_prefix='/api')


@dataset_bp.route('/datasets', methods=['GET'])
@login_required # <-- 改为 login_required
def get_datasets():
    """获取当前用户的所有数据集"""
    # user_id 直接从 current_user 获取
    user_id = current_user.id
    datasets = Dataset.query.filter_by(user_id=user_id).all() # <-- 您的模型中使用的是 user_id 而非 owner_id

    return jsonify([{
        'id': dataset.id,
        'name': dataset.name,
        'description': dataset.description,
        'image_count': len(dataset.images), # <-- 通过关系动态计算图片数量
        'created_at': dataset.created_at.isoformat(),
        'updated_at': dataset.updated_at.isoformat()
    } for dataset in datasets])


# 这个函数必须在 get_datasets 函数外部，作为独立的路由
@dataset_bp.route('/datasets', methods=['POST'])
@login_required
def create_dataset():
    """
    处理创建新数据集的请求。
    新逻辑: 在数据库中创建记录，并在文件系统中创建一套空的目录结构。
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'message': '数据集名称不能为空'}), 400

    name = data.get('name')
    task_type = data.get('task_type', 'Detection')
    image_type = data.get('image_type', 'TCT')
    description = data.get('description', '')

    if Dataset.query.filter_by(name=name, user_id=current_user.id).first():
        return jsonify({'message': '该数据集名称已存在'}), 409

    try:
        new_dataset = Dataset(
            name=name,
            description=description,
            task_type=task_type,
            image_type=image_type,
            user_id=current_user.id
        )
        db.session.add(new_dataset)
        db.session.commit()

        datasets_root_dir = current_app.config['DATASETS_DIR']
        new_dataset_path = os.path.join(datasets_root_dir, name)

        sub_dirs = [
            os.path.join(new_dataset_path, 'images', 'train'),
            os.path.join(new_dataset_path, 'images', 'val'),
            os.path.join(new_dataset_path, 'labels', 'train'),
            os.path.join(new_dataset_path, 'labels', 'val')
        ]

        # 修复了 'for-' 的拼写错误
        for d in sub_dirs:
            os.makedirs(d, exist_ok=True)

        return jsonify({'message': '数据集已成功创建空的目录结构', 'dataset': {
            'id': new_dataset.id,
            'name': new_dataset.name,
            'description': new_dataset.description,
            'task_type': new_dataset.task_type,
            'image_type': new_dataset.image_type
        }}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建数据集时发生错误: {e}")
        return jsonify({'message': f'创建数据集失败: {str(e)}'}), 500


@dataset_bp.route('/datasets/<int:dataset_id>/images', methods=['POST'])
@login_required # <-- 改为 login_required
def upload_dataset_image(dataset_id):
    """上传图片到数据集"""
    user_id = current_user.id # <-- 直接从 current_user 获取

    dataset = Dataset.query.filter_by(id=dataset_id, user_id=user_id).first()
    if not dataset:
        return make_response(jsonify({"error": "Dataset not found or access denied"}), 404)

    if 'file' not in request.files:
        return make_response(jsonify({"error": "No file uploaded"}), 400)

    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({"error": "No file selected"}), 400)

    storage = StorageService(current_app.config['DATASETS_DIR'])
    result = storage.save_dataset_image(
        dataset.name, # 传入数据集名称
        file
    )

    new_image = DatasetImage(
        id=str(uuid.uuid4()), # 使用uuid生成ID
        dataset_id=dataset_id,
        filename=result['filename'],
        patient_id=request.form.get('patient_id', ''),
        file_path=result['file_path']
    )

    db.session.add(new_image)
    # dataset.image_count 字段在您的模型中不存在，通过查询动态获取
    db.session.commit()

    return jsonify({
        'id': new_image.id,
        'filename': new_image.filename,
        'patient_id': new_image.patient_id,
        'uploaded_at': new_image.uploaded_at.isoformat()
    }), 201


@dataset_bp.route('/datasets/<int:dataset_id>/images', methods=['GET'])
@login_required # <-- 改为 login_required
def get_dataset_images(dataset_id):
    """获取数据集中的所有图片"""
    user_id = current_user.id # <-- 直接从 current_user 获取

    dataset = Dataset.query.filter_by(id=dataset_id, user_id=user_id).first()
    if not dataset:
        return make_response(jsonify({"error": "Dataset not found or access denied"}), 404)

    images = DatasetImage.query.filter_by(dataset_id=dataset_id).all()

    return jsonify([{
        'id': image.id,
        'filename': image.filename,
        'patient_id': image.patient_id,
        'uploaded_at': image.uploaded_at.isoformat()
    } for image in images])