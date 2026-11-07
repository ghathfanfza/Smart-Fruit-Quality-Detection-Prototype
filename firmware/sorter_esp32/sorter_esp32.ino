// Firmware ESP32 - Smart Fruit Quality Sorter
// Menggerakkan 2 servo (gerbang dan pendorong) untuk memilah jeruk.
// Perintah diterima lewat:
//   - Serial (115200 baud) : 'G' = jeruk bagus, 'B' = jeruk jelek, 'N' = standby (diabaikan)
//   - HTTP (Wi-Fi)         : GET /good dan GET /bad
#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include "secrets.h"  // WIFI_SSID dan WIFI_PASSWORD (salin dari secrets.h.example)

WebServer server(80);

Servo servoPendorong;  // servo 1: mendorong buah
Servo servoGerbang;    // servo 2: mengarahkan jalur

const int PIN_PENDORONG = 25;
const int PIN_GERBANG = 26;

const int GERBANG_BAGUS = 90;  // posisi tengah (jalur jeruk bagus)
const int GERBANG_JELEK = 0;   // posisi jalur jeruk jelek

bool httpAktif = false;

void sortir(int posisiGerbang) {
  // 1. Gerbang bergerak dulu, beri jeda agar siap sebelum buah didorong
  servoGerbang.write(posisiGerbang);
  delay(600);
  // 2. Pendorong mendorong buah
  servoPendorong.write(180);
  delay(1000);
  // 3. Tarik kembali pendorong ke standby
  servoPendorong.write(0);
  delay(400);
}

void sortirBagus() {
  Serial.println("Aksi: Jeruk Bagus!");
  sortir(GERBANG_BAGUS);
  Serial.println("Proses sortir selesai. Kembali standby.");
}

void sortirJelek() {
  Serial.println("Aksi: Jeruk Jelek!");
  sortir(GERBANG_JELEK);
  Serial.println("Proses sortir selesai. Kembali standby.");
}

void handleGood() {
  server.send(200, "text/plain", "Perintah Jeruk Bagus Diterima");
  sortirBagus();
}

void handleBad() {
  server.send(200, "text/plain", "Perintah Jeruk Jelek Diterima");
  sortirJelek();
}

void setup() {
  Serial.begin(115200);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  servoPendorong.setPeriodHertz(50);
  servoGerbang.setPeriodHertz(50);
  servoPendorong.attach(PIN_PENDORONG, 500, 2400);
  servoGerbang.attach(PIN_GERBANG, 500, 2400);

  // Posisi awal standby
  servoPendorong.write(0);
  servoGerbang.write(90);

  // Wi-Fi (opsional): jika gagal terhubung dalam 15 detik, tetap jalan dengan mode serial
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Menghubungkan ke Wi-Fi");
  unsigned long mulai = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - mulai < 15000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi terhubung!");
    Serial.print("IP Address ESP32: ");
    Serial.println(WiFi.localIP());
    server.on("/good", handleGood);
    server.on("/bad", handleBad);
    server.begin();
    httpAktif = true;
  } else {
    Serial.println("\nWi-Fi tidak terhubung. Mode serial saja.");
  }
}

void loop() {
  if (httpAktif) {
    server.handleClient();
  }

  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'G') {
      sortirBagus();
    } else if (c == 'B') {
      sortirJelek();
    }
    // 'N' (netral/standby) dan karakter lain diabaikan
  }
}
