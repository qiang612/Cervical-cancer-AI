import os
import io
import base64
import cv2
import numpy as np
from flask import Flask, jsonify, send_file, make_response
from flask_cors import CORS
from ultralytics import YOLO

# 1. 初始化 Flask 应用和 CORS
app = Flask(__name__)
# 允许所有来源的跨域请求，方便前后端对接
CORS(app)

# 2. 加载你的YOLOv8模型 (在服务启动时加载一次)
# 请再次确认这个路径是正确的，指向你训练好的 best.pt 文件
MODEL_PATH = 'runs/detect/cervical_train2/weights/best.pt'
print(f"--- 正在加载模型，路径: {MODEL_PATH} ---")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"模型文件未找到: {MODEL_PATH}。请检查路径。")
model = YOLO(MODEL_PATH)
print("--- 模型加载成功 ---")

# 3. 设置患者图片所在的目录
IMAGE_DIR = './patient_data/'
print(f"--- 图片数据目录设置为: {IMAGE_DIR} ---")
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print(f"--- 警告: 目录不存在，已自动创建。请将患者图片放入 {IMAGE_DIR} 目录中。 ---")


# API端点：根据患者ID获取原始图片
@app.route('/patient_image/<patient_id>', methods=['GET'])
def get_patient_image(patient_id):
    """提供原始的、未处理的患者图片给前端"""
    print(f"\n--- 接收到获取原始图片的请求, 患者ID: {patient_id} ---")
    try:
        # 构建图片路径
        image_path = os.path.join(IMAGE_DIR, f"{int(patient_id)}.jpg")
        print(f"--- 正在尝试从路径加载图片: {image_path} ---")

        if not os.path.exists(image_path):
            print(f"--- 错误: 路径 {image_path} 下的图片未找到! ---")
            return make_response(jsonify({"error": "Image not found"}), 404)

        print(f"--- 图片加载成功，正在发往前端 ---")
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        print(f"--- 错误: get_patient_image 函数发生异常: {e} ---")
        return make_response(jsonify({"error": "Invalid patient ID or image not found"}), 404)


# API端点：对指定患者图片进行AI模型预测
@app.route('/predict/<patient_id>', methods=['POST'])
def predict(patient_id):
    """接收预测请求，运行模型，并返回带标注的图片、诊断结果和依据"""
    print(f"\n--- 接收到AI诊断请求, 患者ID: {patient_id} ---")
    try:
        # 增加日志：记录开始处理
        print(f"--- 步骤1: 构建图片路径 ---")
        image_path = os.path.join(IMAGE_DIR, f"{int(patient_id)}.jpg")
        print(f"--- 图片路径: {image_path} ---")

        if not os.path.exists(image_path):
            print(f"--- 错误: 图片不存在 ---")
            return make_response(jsonify({"error": "Image not found"}), 404)

        # 增加日志：开始读取图片
        print(f"--- 步骤2: 尝试读取图片 ---")
        image = cv2.imread(image_path)
        if image is None:
            print(f"--- 错误: 无法读取图片（可能格式错误） ---")
            return make_response(jsonify({"error": "Could not read image"}), 500)
        print(f"--- 图片读取成功，尺寸: {image.shape} ---")

        # 增加日志：开始模型预测
        print(f"--- 步骤3: 开始模型预测 ---")
        results = model(image)
        print(f"--- 模型预测完成，返回结果数量: {len(results)} ---")

        # 处理预测结果
        print(f"--- 步骤4: 处理预测结果 ---")
        high_confidence_count = 0
        confidence_threshold = 0.50
        annotated_image = image.copy()

        for r in results:
            for box in r.boxes:
                conf = box.conf[0]
                if conf > confidence_threshold:
                    high_confidence_count += 1
                # 绘制边界框
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{r.names[int(box.cls[0])]}: {conf:.2f}"
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print(f"--- 高置信度目标数量: {high_confidence_count} ---")

        # 生成诊断结果
        print(f"--- 步骤5: 生成诊断结果 ---")
        cell_count_threshold = 3
        if high_confidence_count > cell_count_threshold:
            diagnosis = "结果A（阳性）"
            basis = f"诊断为阳性。检测到 {high_confidence_count} 个高置信度病变细胞。"
        else:
            diagnosis = "结果B（阴性）"
            basis = f"诊断为阴性。检测到 {high_confidence_count} 个高置信度病变细胞。"

        # 编码图片为base64
        print(f"--- 步骤6: 编码处理后图片 ---")
        _, buffer = cv2.imencode('.jpg', annotated_image)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
        print(f"--- 图片编码完成，长度: {len(processed_image_base64)} ---")

        # 返回结果
        print(f"--- 步骤7: 返回诊断结果 ---")
        return jsonify({
            'diagnosis': diagnosis,
            'basis': basis,
            'processed_image': processed_image_base64
        })

    except Exception as e:
        # 捕获所有异常并打印详细信息
        print(f"--- 预测接口异常: {str(e)} ---")
        import traceback
        print(traceback.format_exc())  # 打印完整堆栈信息
        return make_response(jsonify({"error": str(e)}), 500)


# 启动Flask服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)