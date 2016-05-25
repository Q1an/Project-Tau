#include "VarSpeedServo.h"

VarSpeedServo s;
int pos = 0;
int Servo_PIN = 12; //NodeMCU D6

void setup() {
  Serial.begin(9600);
  s.attach(Servo_PIN);
}

void loop() {
  Serial.println("1500");
  s.slowmove (90, 255);
  delay(1000);
}
