import uuid
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Dataset, DatasetImage
from services.storage_service import StorageService

# 创建蓝图
dataset_bp = Blueprint('dataset', __name__, url_prefix='/api/datasets')


@dataset_bp.route('', methods=['GET'])
@jwt_required()
def get_datasets():
    """获取当前用户的所有数据集"""
    user_id = get_jwt_identity()
    datasets = Dataset.query.filter_by(owner_id=user_id).all()

    return jsonify([{
        'id': dataset.id,
        'name': dataset.name,
        'description': dataset.description,
        'image_count': dataset.image_count,
        'created_at': dataset.created_at.isoformat(),
        'updated_at': dataset.updated_at.isoformat()
    } for dataset in datasets])


@dataset_bp.route('', methods=['POST'])
@jwt_required()
def create_dataset():
    """创建新数据集"""
    user_id = get_jwt_identity()
    data = request.json

    if not data or not data.get('name'):
        return make_response(jsonify({"error": "Dataset name is required"}), 400)

    dataset_id = str(uuid.uuid4())
    new_dataset = Dataset(
        id=dataset_id,
        name=data.get('name'),
        description=data.get('description', ''),
        owner_id=user_id
    )

    db.session.add(new_dataset)
    db.session.commit()

    return jsonify({
        'id': new_dataset.id,
        'name': new_dataset.name,
        'description': new_dataset.description,
        'image_count': 0,
        'created_at': new_dataset.created_at.isoformat()
    }), 201


@dataset_bp.route('/<dataset_id>/images', methods=['POST'])
@jwt_required()
def upload_dataset_image(dataset_id):
    """上传图片到数据集"""
    user_id = get_jwt_identity()

    # 验证数据集是否存在且属于当前用户
    dataset = Dataset.query.filter_by(id=dataset_id, owner_id=user_id).first()
    if not dataset:
        return make_response(jsonify({"error": "Dataset not found or access denied"}), 404)

    if 'file' not in request.files:
        return make_response(jsonify({"error": "No file uploaded"}), 400)

    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({"error": "No file selected"}), 400)

    # 保存文件
    result = StorageService.save_dataset_image(
        dataset_id,
        file,
        request.form.get('patient_id', '')
    )

    # 创建数据库记录
    new_image = DatasetImage(
        id=result['image_id'],
        dataset_id=dataset_id,
        filename=result['filename'],
        patient_id=result['patient_id'],
        file_path=result['file_path']
    )

    db.session.add(new_image)
    dataset.image_count += 1
    db.session.commit()

    return jsonify({
        'id': new_image.id,
        'filename': new_image.filename,
        'patient_id': new_image.patient_id,
        'uploaded_at': new_image.uploaded_at.isoformat()
    }), 201


@dataset_bp.route('/<dataset_id>/images', methods=['GET'])
@jwt_required()
def get_dataset_images(dataset_id):
    """获取数据集中的所有图片"""
    user_id = get_jwt_identity()

    # 验证数据集是否存在且属于当前用户
    dataset = Dataset.query.filter_by(id=dataset_id, owner_id=user_id).first()
    if not dataset:
        return make_response(jsonify({"error": "Dataset not found or access denied"}), 404)

    images = DatasetImage.query.filter_by(dataset_id=dataset_id).all()

    return jsonify([{
        'id': image.id,
        'filename': image.filename,
        'patient_id': image.patient_id,
        'uploaded_at': image.uploaded_at.isoformat()
    } for image in images])
