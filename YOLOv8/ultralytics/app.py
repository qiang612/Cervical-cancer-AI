import os
import cv2
import numpy as np
import base64
from flask import Flask, jsonify, send_file, make_response
from flask_cors import CORS
from ultralytics import YOLO

# 1. 初始化 Flask 应用和 CORS
app = Flask(__name__)
CORS(app)  # 允许所有来源跨域请求

# 2. 加载YOLOv8模型
MODEL_PATH = 'runs/detect/cervical_train2/weights/best.pt'
print(f"--- 正在加载模型，路径: {MODEL_PATH} ---")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"模型文件未找到: {MODEL_PATH}。请检查路径。")
model = YOLO(MODEL_PATH)
print("--- 模型加载成功 ---")

# 3. 图片数据目录设置
IMAGE_DIR = './patient_data/'
print(f"--- 图片数据目录: {IMAGE_DIR} ---")
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print(f"--- 已自动创建图片目录，请将患者图片放入该目录 ---")


# API：获取原始患者图片
@app.route('/patient_image/<patient_id>', methods=['GET'])
def get_patient_image(patient_id):
    print(f"\n--- 接收原始图片请求，患者ID: {patient_id} ---")
    try:
        image_path = os.path.join(IMAGE_DIR, f"{int(patient_id)}.jpg")
        if not os.path.exists(image_path):
            print(f"--- 图片未找到: {image_path} ---")
            return make_response(jsonify({"error": "Image not found"}), 404)
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        print(f"--- 图片请求异常: {e} ---")
        return make_response(jsonify({"error": "Invalid patient ID"}), 404)


# API：AI诊断（核心逻辑修改部分）
@app.route('/predict/<patient_id>', methods=['POST'])
def predict(patient_id):
    print(f"\n--- 接收AI诊断请求，患者ID: {patient_id} ---")
    try:
        # 1. 加载图片
        image_path = os.path.join(IMAGE_DIR, f"{int(patient_id)}.jpg")
        if not os.path.exists(image_path):
            return make_response(jsonify({"error": "Image not found"}), 404)
        image = cv2.imread(image_path)
        if image is None:
            return make_response(jsonify({"error": "Could not read image"}), 500)
        print(f"--- 图片加载成功，尺寸: {image.shape} ---")

        # 2. 模型预测
        results = model(image)
        annotated_image = image.copy()  # 用于绘制标注的图片

        # 3. 按类别统计高置信度细胞（置信度>50%）
        # 初始化计数器（只关注需要判断的三类病变细胞）
        ssc_count = 0  # 癌变细胞（SSC）
        hsil_count = 0  # 重度病变（HSIL）
        lsil_count = 0  # 轻度病变（LSIL）
        confidence_threshold = 0.5  # 置信度阈值

        for r in results:
            for box in r.boxes:
                conf = box.conf[0]  # 置信度
                cls_name = r.names[int(box.cls[0])]  # 细胞类别名称（需与模型输出一致）

                # 只统计置信度>50%的目标
                if conf > confidence_threshold:
                    # 绘制标注框和类别文字
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f"{cls_name}: {conf:.2f}"
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_image, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # 按类别计数（严格匹配类别名称）
                    if cls_name == "SSC":
                        ssc_count += 1
                    elif cls_name == "HSIL":
                        hsil_count += 1
                    elif cls_name == "LSIL":
                        lsil_count += 1

        print(f"--- 高置信度细胞统计: SSC={ssc_count}, HSIL={hsil_count}, LSIL={lsil_count} ---")

        # 4. 核心判断逻辑（按优先级：SSC > HSIL > LSIL）
        if ssc_count >= 3:
            diagnosis = "D(阳性)"
            basis = f"检测到 {ssc_count} 个SSC（癌变细胞），置信度>50%，判定为结果D（阳性）。"
        elif hsil_count >= 3:
            diagnosis = "C(阳性)"
            basis = f"检测到 {hsil_count} 个HSIL（重度病变细胞），置信度>50%，判定为结果C（阳性）。"
        elif lsil_count >= 3:
            diagnosis = "B(阳性)"
            basis = f"检测到 {lsil_count} 个LSIL（轻度病变细胞），置信度>50%，判定为结果B（阳性）。"
        else:
            diagnosis = "A(阴性)"
            basis = f"未检测到足够数量的病变细胞（SSC、HSIL、LSIL均<3个），判定为结果A（阴性）。"

        # 5. 编码处理后的图片为base64
        _, buffer = cv2.imencode('.jpg', annotated_image)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

        # 6. 返回结果
        return jsonify({
            'diagnosis': diagnosis,
            'basis': basis,
            'processed_image': processed_image_base64,
            'cell_counts': {  # 新增：返回各类细胞数量（方便前端调试）
                'SSC': ssc_count,
                'HSIL': hsil_count,
                'LSIL': lsil_count
            }
        })

    except Exception as e:
        print(f"--- 诊断异常: {str(e)} ---")
        import traceback
        print(traceback.format_exc())
        return make_response(jsonify({"error": str(e)}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
