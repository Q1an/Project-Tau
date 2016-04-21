#include <Wire.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <Servo.h>
#include "Adafruit_BNO055.h"
#include "imumaths.h"



#define USE_SERIAL Serial
#define BNO055_SAMPLERATE_DELAY_MS (100)

Adafruit_BNO055 bno = Adafruit_BNO055();
ESP8266WiFiMulti WiFiMulti;
Servo s;
int pos = 0;
int Servo_PIN = 12; //NodeMCU D6

void displaySensorStatus(void)
{
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
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
    s.attach(Servo_PIN);
}

void loop() {
    // wait for WiFi connection
    if((WiFiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        USE_SERIAL.print("[HTTP] begin...\n");

        // configure server and url
        http.begin("http://192.168.1.74:8000/");

        USE_SERIAL.print("[HTTP] POST...\n");
        
        // start connection and send HTTP header
        
        /*
         * get data from IMU and send
         *
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
        
//        imu::Vector<3> eul = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
//        
//        /* Display the floating point data */
//        Serial.println("Euler: ");
//        Serial.print("X: ");
//        Serial.print(eul.x());
//        Serial.print(" Y: ");
//        Serial.print(eul.y());
//        Serial.print(" Z: ");
//        Serial.print(eul.z());
//        Serial.println("\t");
//        
//        imu::Vector<3> lineacc = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
//        
//        Serial.println("Linear Acc: ");
//        Serial.print("X: ");
//        Serial.print(lineacc.x(), 4); 
//        Serial.print(" Y: ");
//        Serial.print(lineacc.y(), 4); 
//        Serial.print(" Z: ");
//        Serial.print(lineacc.z(), 4); 
//        Serial.println("\t");
//        
//        imu::Vector<3> anguvel = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
//      
//        /* Display the floating point data */
//        Serial.println("Angular velocity: ");
//        Serial.print("X: ");
//        Serial.print(anguvel.x());
//        Serial.print(" Y: ");
//        Serial.print(anguvel.y());
//        Serial.print(" Z: ");
//        Serial.print(anguvel.z());
//        Serial.println("\t");

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
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] POST... code: %d\n", httpCode);

            // file found at server
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                int servodata = payload.toInt();
                int val = map(servodata, 0, 360, 150, 30);     
                s.write(val);
                delay(50);
                USE_SERIAL.println(val);
            }
        } else {
            USE_SERIAL.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }

    delay(50);
}
