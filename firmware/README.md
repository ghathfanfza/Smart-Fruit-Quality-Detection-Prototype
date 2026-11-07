# Firmware ESP32

| Folder | Fungsi |
|---|---|
| `sorter_esp32/` | Firmware utama: menerima perintah dan menggerakkan servo pemilah |
| `servo_test/` | Sketch uji dan kalibrasi satu servo (GPIO27) |

## Perangkat keras

| Komponen | Keterangan |
|---|---|
| ESP32 | Board: ESP32 DevKit V1 |
| Servo 1 (pendorong) | GPIO 25, bergerak 0° ke 180° lalu kembali ke 0° |
| Servo 2 (gerbang) | GPIO 26, 90° untuk jalur bagus dan 0° untuk jalur jelek (standby 90°) |
| Kamera | Action Cam B-Pro , terhubung ke laptop |

## Perintah

| Jalur | Perintah | Aksi |
|---|---|---|
| Serial (115200 baud) | `G` | sortir jeruk bagus |
| Serial (115200 baud) | `B` | sortir jeruk jelek |
| Serial (115200 baud) | `N` | standby (diabaikan) |
| HTTP | `GET /good`, `GET /bad` | sortir bagus atau jelek |

Skrip laptop (`edge/sorter_edge.py`) memakai jalur serial. Jalur HTTP berguna untuk uji manual:
```bash
curl http://<IP-ESP32>/good
```

## Upload ke ESP32

1. Pasang library **ESP32Servo** (Arduino IDE: Library Manager) dan board package **ESP32**.
2. Di folder `sorter_esp32/`, salin `secrets.h.example` menjadi `secrets.h` dan isi Wi-Fi-mu.
3. Pilih board dan port, lalu upload. Buka Serial Monitor (115200) untuk melihat IP dan status.

Wi-Fi bersifat opsional: kalau gagal terhubung dalam 15 detik, ESP32 tetap berjalan dengan mode serial.
