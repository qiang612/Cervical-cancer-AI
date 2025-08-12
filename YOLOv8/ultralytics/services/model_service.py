import cv2
import numpy as np
import os
from ultralytics import YOLO
from config import Config


class ModelService:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        """加载YOLO模型"""
        print(f"--- 正在加载模型，路径: {Config.MODEL_PATH} ---")
        if not os.path.exists(Config.MODEL_PATH):
            raise FileNotFoundError(f"模型文件未找到: {Config.MODEL_PATH}。请检查路径。")
        self.model = YOLO(Config.MODEL_PATH)
        print("--- 模型加载成功 ---")

    def predict(self, image_path):
        """
        对图像进行预测并返回结果
        """
        # 加载图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("无法读取图像文件")

        # ## FINAL FIX: 在预测前，统一将图片进行缩放以节省内存 ##
        # 设定一个标准宽度，例如 640 像素，并按比例计算高度
        target_width = 640
        height, width, _ = image.shape
        scale = target_width / width
        target_height = int(height * scale)

        # 使用 INTER_AREA 插值算法进行高质量的缩放
        resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)
        print(f"--- Image resized from {width}x{height} to {target_width}x{target_height} for prediction ---")

        # 使用缩放后的图片进行模型预测
        results = self.model(resized_image)

        # 在原始尺寸的图片副本上进行绘制，以保证标注结果的清晰度
        annotated_image = image.copy()

        # 按类别统计高置信度细胞
        ssc_count = 0
        hsil_count = 0
        lsil_count = 0
        confidence_threshold = 0.5

        for r in results:
            for box in r.boxes:
                conf = box.conf[0]
                cls_name = r.names[int(box.cls[0])]

                if conf > confidence_threshold:
                    # ## FIX: 将预测的边界框坐标按比例还原到原始图片尺寸 ##
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    orig_x1, orig_y1, orig_x2, orig_y2 = int(x1 / scale), int(y1 / scale), int(x2 / scale), int(
                        y2 / scale)

                    label = f"{cls_name}: {conf:.2f}"
                    cv2.rectangle(annotated_image, (orig_x1, orig_y1), (orig_x2, orig_y2), (0, 255, 0), 2)
                    cv2.putText(annotated_image, label, (orig_x1, orig_y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # 按类别计数
                    if cls_name == "SSC":
                        ssc_count += 1
                    elif cls_name == "HSIL":
                        hsil_count += 1
                    elif cls_name == "LSIL":
                        lsil_count += 1

        print(f"--- 高置信度细胞统计: SSC={ssc_count}, HSIL={hsil_count}, LSIL={lsil_count} ---")

        # 核心判断逻辑
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

        return {
            'diagnosis': diagnosis,
            'basis': basis,
            'annotated_image': annotated_image,
            'cell_counts': {
                'SSC': ssc_count,
                'HSIL': hsil_count,
                'LSIL': lsil_count
            }
        }