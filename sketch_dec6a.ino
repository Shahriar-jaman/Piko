#include <ESP32Servo.h>

Servo myServo;

int servoPin = 13;       // Change if needed
int ledPin = 14;         // LED pin
int angle = 0;
bool forwardDir = true;

void setup() {
  myServo.attach(servoPin);
  pinMode(ledPin, OUTPUT);
}

void loop() {

  // -------- Servo Slow Movement --------
  if (forwardDir) {
    angle++;
    if (angle >= 180) forwardDir = false;
  } else {
    angle--;
    if (angle <= 0) forwardDir = true;
  }

  myServo.write(angle);
  delay(15);  // slow movement

  // -------- LED Slow Blink (Fade) --------
  static int brightness = 0;
  static int fadeAmount = 5;

  brightness += fadeAmount;
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }

  analogWrite(ledPin, brightness);  
}
