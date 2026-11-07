"""Pelatihan model klasifikasi kualitas jeruk (YOLOv8n-cls).

Jalankan dari root repositori:  python training/train.py
Dataset: datasets/train/{good,bad} dan datasets/val/{good,bad}
Hasil  : runs/classify/train/weights/best.pt
"""
import os

from ultralytics import YOLO

# Menghindari error konflik library pada Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

if __name__ == "__main__":
    model = YOLO("yolov8n-cls.pt")

    model.train(
        data="datasets",
        epochs=100,
        imgsz=224,
        batch=16,

        # --- Augmentasi ---
        degrees=15.0,   # putar gambar
        flipud=0.5,     # balik vertikal
        fliplr=0.5,     # balik horizontal
        hsv_v=0.4,      # variasi kecerahan
        hsv_s=0.7,      # variasi saturasi
        shear=10.0,

        # --- Optimizer ---
        patience=20,
        optimizer="AdamW",
        lr0=0.001,
    )

    print("Training selesai!")
