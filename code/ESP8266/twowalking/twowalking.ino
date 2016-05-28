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

Servo s1;
Servo s2;

int Servo_PIN1 = 12; //NodeMCU D6
int Servo_PIN2 = 15; //NodeMCU D8

unsigned long prevTime = 0;
unsigned long currTime = 0;
unsigned long time1 = 0;
unsigned long time2 = 0;

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
	
	/* Initialise the sensor */
	Serial.println("IMU Initialization\n");
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

	// http.setTimeout(10);
	// http.setReuse(true);
	
	/* configure server and url */
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
	 */

	uint8_t datasent[30]; memset(datasent, 0, 30);

	currTime = micros();
	Serial.println(currTime - prevTime);
	prevTime = currTime;

	bno.getData(Adafruit_BNO055::VECTOR_GYROSCOPE, datasent);
	bno.getData(Adafruit_BNO055::VECTOR_LINEARACCEL, datasent + 6);
	bno.getData(Adafruit_BNO055::VECTOR_EULER, datasent + 12);
	bno.getQuat(datasent + 18);
	
	if((WiFiMulti.run() == WL_CONNECTED)) {

		HTTPClient http;
		http.begin("http://192.168.1.74:8000/");

		datasent[26] = (currTime & 0x000000ff);
		datasent[27] = (currTime & 0x0000ff00) >> 8;
		datasent[28] = (currTime & 0x00ff0000) >> 16;
		datasent[29] = (currTime & 0xff000000) >> 24;
		
		time1 = micros();
		int httpCode = http.POST(datasent, sizeof(datasent));
		time2 = micros();
		Serial.print("POST				");
		Serial.println(time2 - time1);

		if(httpCode > 0) {
			/* HTTP header has been send and Server response header has been handled */
			// USE_SERIAL.printf("[HTTP] POST... code: %d\n", httpCode);
		 
			/* file found at server */
			if(httpCode == HTTP_CODE_OK) {
				String payload = http.getString();
				int servo1 = payload.substring(0, 3).toInt();
				int servo2 = payload.substring(3, 6).toInt();
				int val1 = servo1 - 100;
				int val2 = servo2 - 100;      
				s1.write(val1);
				s2.write(val2);
               // USE_SERIAL.println(val1);
               // USE_SERIAL.println(val2);
			}
		} else {
			USE_SERIAL.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
		}

       http.end();
	}
}
