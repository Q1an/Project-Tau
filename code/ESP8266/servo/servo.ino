#include <Servo.h>

Servo s;
int pos = 0;
int Servo_PIN = 12; //NodeMCU D6

void setup() {
  Serial.begin(9600);
  s.attach(Servo_PIN);
}

void loop() {
  Serial.println("1500");
  s.writeMicroseconds(1500);
  delay(5000);
  Serial.println("1000");
  s.writeMicroseconds(1000);
  delay(5000);
  Serial.println("2000");
  s.writeMicroseconds(2000);
  delay(5000);
  Serial.println("2300");
  s.writeMicroseconds(2300);
  delay(5000);
  Serial.println("700");
  s.writeMicroseconds(700);
  delay(5000);
}
