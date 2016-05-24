#include <Wire.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <Servo.h>
#include "imumaths.h"
#include "Adafruit_BNO055.h"

#define USE_SERIAL Serial

Adafruit_BNO055 bno = Adafruit_BNO055();
ESP8266WiFiMulti WiFiMulti;

Servo s1;
Servo s2;

HTTPClient http;

int Servo_PIN1 = 12; //NodeMCU D6
int Servo_PIN2 = 15; //NodeMCU D8

long previousTime = 0;
long interval = 10000;
long counter = 0;

void displaySensorStatus(void)
{
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  // Display the results in the Serial Monitor
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(500);
}


void setup() {

  USE_SERIAL.begin(115200);
  // USE_SERIAL.setDebugOutput(true);

  USE_SERIAL.print("\n\n\n");

  for(uint8_t t = 5; t > 0; t--) {
      USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
      USE_SERIAL.flush();
      delay(1000);
  }

  WiFiMulti.addAP("Tau", "314159265358");

  Serial.println("IMU Initialization\n");
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);
  bno.setExtCrystalUse(true);
  displaySensorStatus();
  s1.attach(Servo_PIN1);
  s2.attach(Servo_PIN2);

  while ((WiFiMulti.run() != WL_CONNECTED))
  {
    Serial.println("Wait for Wi-Fi connection...");
    delay(100);
  }

//  http.setTimeout(10);
  http.setReuse(true);
  USE_SERIAL.print("[HTTP] begin...\n");
  
  /* configure server and url */
  http.begin("http://192.168.1.74:8000/");
}

void loop() {
                
  /* Get data from IMU and send
   * Possible vector values can be:
   * - VECTOR_ACCELEROMETER - m/s^2
   * - VECTOR_MAGNETOMETER  - uT
   * - VECTOR_GYROSCOPE     - rad/s     - 1rps = 900 LSB
   * - VECTOR_EULER         - degrees   - 1 degree = 16 LSB
   * - VECTOR_LINEARACCEL   - m/s^2     - 1m/s^2 = 100 LSB
   * - VECTOR_GRAVITY       - m/s^2
   * 
   */
   
  uint8_t gyro[6]; memset (gyro, 0, 6);
  uint8_t linearacc[6]; memset (linearacc, 0, 6);
  uint8_t euler[6]; memset (euler, 0, 6);

  bno.getData(Adafruit_BNO055::VECTOR_GYROSCOPE, gyro);
  bno.getData(Adafruit_BNO055::VECTOR_LINEARACCEL, linearacc);
  bno.getData(Adafruit_BNO055::VECTOR_EULER, euler);

  unsigned long currentTime = micros();
  if (currentTime - previousTime >= interval)
  {    
    Serial.println(currentTime - previousTime);
    previousTime = currentTime;
    counter += 1;
    
    if (counter >= 300) {
      counter = 0;
      Serial.println("*** http re-start ***");
      http.begin("http://192.168.1.74:8000/");
    }
    
    if((WiFiMulti.run() == WL_CONNECTED)) {
      
        // USE_SERIAL.print("[HTTP] POST...\n");
                
        uint8_t datasent[18];
        memset(datasent, 0, 18);
        for (int i = 0; i < 6; i++)
          datasent[i] = gyro[i];
        for (int i = 0; i < 6; i++)
          datasent[i + 6] = linearacc[i];
        for (int i = 0; i < 6; i++)
          datasent[i + 12] = euler[i];
        
        int httpCode = http.POST(datasent, sizeof(datasent));
       
        if(httpCode > 0) {
            /* HTTP header has been send and Server response header has been handled */
            // USE_SERIAL.printf("[HTTP] POST... code: %d\n", httpCode);
       
            /* file found at server */
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                int servo1 = payload.substring(0,3).toInt();
                int servo2 = payload.substring(3,6).toInt();
                int val1 = servo1-100;
                int val2 = servo2-100;      
                s1.write(val1);
                s2.write(val2);
//                USE_SERIAL.println(val1);
//                USE_SERIAL.println(val2);
            }
        } else {
            USE_SERIAL.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

//        http.end();
    }
  }
}
