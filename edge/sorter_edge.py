"""Klasifikasi kualitas jeruk real-time (YOLO classify) -> perintah serial ke ESP32.

Logika:
  - "good"   : harus terdeteksi konstan selama LOCK_SECONDS sebelum perintah 'G' dikirim
  - "bad"    : langsung reject, perintah 'B' dikirim tanpa jeda
  - standby  : tidak ada objek atau keyakinan di bawah threshold -> perintah 'N'
Sesuai alur di laporan Big Data, setiap keputusan (good/bad) juga dikirim sebagai log JSON
ke pipeline Spark lewat TCP (port 9999).
"""
import json
import os
import socket
import time

import cv2
import serial
from ultralytics import YOLO

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "True")

MODEL_PATH = os.getenv("MODEL_PATH", "models/best.pt")
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUD = int(os.getenv("SERIAL_BAUD", "115200"))
CONF_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.80"))
LOCK_SECONDS = float(os.getenv("LOCK_SECONDS", "3.0"))
SPARK_HOST = os.getenv("SPARK_HOST")
SPARK_PORT = int(os.getenv("SPARK_PORT", "9999"))

TARGET_LABEL = "good"
LOG_NAMES = {"good": "Jeruk Bagus", "bad": "Jeruk Jelek"}


def send_log(label):
    """Kirim satu log JSON ke Spark (opsional)."""
    if not SPARK_HOST:
        return
    payload = json.dumps({"kategori": LOG_NAMES[label], "jumlah": 1}).encode("utf-8")
    try:
        with socket.create_connection((SPARK_HOST, SPARK_PORT), timeout=3) as s:
            s.sendall(payload)
    except OSError as exc:
        print(f"Gagal kirim log ke Spark: {exc}")


if not SPARK_HOST:
    print("Peringatan: SPARK_HOST belum diisi, log tidak dikirim ke Spark.")

try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
    time.sleep(2)  # tunggu koneksi serial stabil
    print("Koneksi Serial ke ESP32 Berhasil!")
except serial.SerialException:
    print("Gagal membuka Port Serial. Pastikan ESP32 terhubung dan port benar.")
    raise SystemExit(1)

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)

start_lock_time = None
action_triggered = False  # mencegah pengiriman perintah berulang

print(f"Sistem aktif - threshold {CONF_THRESHOLD * 100:.0f}% dengan timer {LOCK_SECONDS:.0f} detik")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    current_label = None
    current_conf = 0.0
    for r in results:
        probs = r.probs
        current_label = r.names[probs.top1]
        current_conf = probs.top1conf.item()

    if current_label and current_conf >= CONF_THRESHOLD:
        if current_label == TARGET_LABEL:
            if start_lock_time is None:
                start_lock_time = time.time()

            elapsed = time.time() - start_lock_time
            countdown = max(0, int(LOCK_SECONDS - elapsed))

            if elapsed >= LOCK_SECONDS:
                display_text = "CONFIRMED: GOOD! MEMPROSES..."
                color = (0, 255, 0)
                if not action_triggered:
                    ser.write(b"G")
                    send_log("good")
                    print("Mengirim perintah 'G' ke ESP32")
                    action_triggered = True
            else:
                display_text = f"LOCKING GOOD FRUIT... ({countdown}s)"
                color = (0, 255, 255)

        elif current_label == "bad":
            display_text = f"REJECT: BAD FRUIT ({current_conf * 100:.1f}%)"
            color = (0, 0, 255)
            start_lock_time = None
            if not action_triggered:
                ser.write(b"B")
                send_log("bad")
                print("Mengirim perintah 'B' ke ESP32")
                action_triggered = True
    else:
        display_text = "STANDBY: MENUNGGU OBJEK..."
        color = (255, 255, 255)
        start_lock_time = None
        if action_triggered:
            ser.write(b"N")  # status netral/standby
            action_triggered = False

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 70), (40, 40, 40), -1)
    cv2.putText(frame, display_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3)
    cv2.imshow("Fruit Sorting", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
