from flask import Blueprint, send_file, make_response, jsonify
from services.model_service import ModelService
from services.storage_service import StorageService
from config import Config

# 创建蓝图
diagnosis_bp = Blueprint('diagnosis', __name__)


@diagnosis_bp.route('/patient_image/<patient_id>', methods=['GET'])
def get_patient_image(patient_id):
    """获取原始患者图片"""
    print(f"\n--- 接收原始图片请求，患者ID: {patient_id} ---")
    try:
        image_path = StorageService.get_patient_image_path(patient_id)
        if not StorageService.patient_image_exists(patient_id):
            print(f"--- 图片未找到: {image_path} ---")
            return make_response(jsonify({"error": "Image not found"}), 404)
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        print(f"--- 图片请求异常: {e} ---")
        return make_response(jsonify({"error": "Invalid patient ID"}), 404)


@diagnosis_bp.route('/predict/<patient_id>', methods=['POST'])
def predict(patient_id):
    """AI诊断接口"""
    print(f"\n--- 接收AI诊断请求，患者ID: {patient_id} ---")
    try:
        # 检查图片是否存在
        if not StorageService.patient_image_exists(patient_id):
            image_path = StorageService.get_patient_image_path(patient_id)
            return make_response(jsonify({"error": f"Image not found at {image_path}"}), 404)

        # 获取图片路径
        image_path = StorageService.get_patient_image_path(patient_id)

        # 调用模型服务进行预测
        model_service = ModelService()
        result = model_service.predict(image_path)

        # 处理结果
        processed_image_base64 = StorageService.image_to_base64(result['annotated_image'])

        # 返回结果
        return jsonify({
            'diagnosis': result['diagnosis'],
            'basis': result['basis'],
            'processed_image': processed_image_base64,
            'cell_counts': result['cell_counts']
        })

    except Exception as e:
        print(f"--- 诊断异常: {str(e)} ---")
        import traceback
        print(traceback.format_exc())
        return make_response(jsonify({"error": str(e)}), 500)
