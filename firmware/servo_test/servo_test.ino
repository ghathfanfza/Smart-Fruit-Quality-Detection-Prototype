// Sketch uji dan kalibrasi servo (1 servo di GPIO27): bergerak 0 -> 90 -> 180 derajat.
// Memakai API ledcAttach, sehingga butuh Arduino-ESP32 core versi 3.x.
// PIN YANG DIGUNAKAN
const int pinServo = 27; 

void setup() {
  // Memulai PWM pada pin 27
  // Parameter: (pin, frekuensi, resolusi)
  // Frekuensi servo standar adalah 50Hz
  ledcAttach(pinServo, 50, 10); 
}

void loop() {
  // 1. Gerak ke 0 derajat
  // Nilai 26 adalah pulse width untuk 0 derajat pada resolusi 10-bit
  ledcWrite(pinServo, 26); 
  delay(2000); // Tunggu 2 detik

  // 2. Gerak ke 90 derajat
  // Nilai 77 adalah pulse width untuk 90 derajat
  ledcWrite(pinServo, 77); 
  delay(2000); // Tunggu 2 detik

  // 3. Gerak ke 180 derajat
  // Nilai 128 adalah pulse width untuk 180 derajat
  ledcWrite(pinServo, 128); 
  delay(2000); // Tunggu 2 detik
}