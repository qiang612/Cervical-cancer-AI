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

        参数:
            image_path: 图像文件路径

        返回:
            包含诊断结果、依据、处理后的图像和细胞计数的字典
        """
        # 加载图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("无法读取图像文件")

        # 模型预测
        results = self.model(image)
        annotated_image = image.copy()  # 用于绘制标注的图片

        # 按类别统计高置信度细胞（置信度>50%）
        ssc_count = 0  # 癌变细胞（SSC）
        hsil_count = 0  # 重度病变（HSIL）
        lsil_count = 0  # 轻度病变（LSIL）
        confidence_threshold = 0.5  # 置信度阈值

        for r in results:
            for box in r.boxes:
                conf = box.conf[0]  # 置信度
                cls_name = r.names[int(box.cls[0])]  # 细胞类别名称

                # 只统计置信度>50%的目标
                if conf > confidence_threshold:
                    # 绘制标注框和类别文字
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f"{cls_name}: {conf:.2f}"
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_image, label, (x1, y1 - 10),
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
