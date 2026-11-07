# Pelatihan model

Model kualitas jeruk dilatih sebagai **klasifikasi citra** dengan **YOLOv8n-cls** untuk dua kelas: `good` dan `bad`.

**Dataset:** sekitar 2.000 gambar jeruk, dibagi 1.000 untuk training dan 1.000 untuk validasi.
Dataset tidak disimpan di repositori. Dataset diambil melalui pengambilan citra secara manual menggunakan skrip.

```
datasets/
  train/good/   train/bad/
  val/good/     val/bad/
```

**Konfigurasi (`train.py`):**

| Parameter | Nilai |
|---|---|
| Model dasar | `yolov8n-cls.pt` |
| Epoch | 100 (early stopping, patience 20) |
| Ukuran gambar / batch | 224 / 16 |
| Optimizer | AdamW, learning rate awal 0,001 |
| Augmentasi | rotasi 15°, flip vertikal dan horizontal 0,5, kecerahan (hsv_v) 0,4, saturasi (hsv_s) 0,7, shear 10° |

**Menjalankan** (dari root repositori):
```bash
pip install -r requirements.txt
python training/train.py
```
Bobot terbaik tersimpan di `runs/classify/train/weights/best.pt`. Salin ke `models/best.pt` untuk dipakai
skrip `edge/sorter_edge.py`.
