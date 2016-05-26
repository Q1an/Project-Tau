#include <Wire.h>
#include "Adafruit_BNO055.h"
#include "imumaths.h"
	
#define BNO055_SAMPLERATE_DELAY_MS (500)

Adafruit_BNO055 bno = Adafruit_BNO055();

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
/**************************************************************************/
/*
		Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
	Serial.begin(9600);
	Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");
	/* Initialise the sensor */
	if(!bno.begin())
	{
		/* There was a problem detecting the BNO055 ... check your connections */
		Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
		while(1);
	}

	delay(1000);
	bno.setExtCrystalUse(true);
	//displaySensorStatus();
}

/**************************************************************************/
/*
		Arduino loop function, called once 'setup' is complete (your own code
		should go here)
*/
/**************************************************************************/
void loop(void)
{
	// Possible vector values can be:
	// - VECTOR_ACCELEROMETER - m/s^2
	// - VECTOR_MAGNETOMETER  - uT
	// - VECTOR_GYROSCOPE     - rad/s
	// - VECTOR_EULER         - degrees
	// - VECTOR_LINEARACCEL   - m/s^2
	// - VECTOR_GRAVITY       - m/s^2
	imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

	/* Display the floating point data */
	Serial.println("Euler: ");
	Serial.print("X: ");
	Serial.print(euler.x());
	Serial.print(" Y: ");
	Serial.print(euler.y());
	Serial.print(" Z: ");
	Serial.print(euler.z());
	Serial.println("\t");
	
	// imu::Vector<3> lineacc = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
	
	// Serial.println("Linear Acc: ");
	// Serial.print("X: ");
	// Serial.print(lineacc.x(), 4); 
	// Serial.print(" Y: ");
	// Serial.print(lineacc.y(), 4); 
	// Serial.print(" Z: ");
	// Serial.print(lineacc.z(), 4); 
	// Serial.println("\t");
	
	// imu::Vector<3> anguvel = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);

	// /* Display the floating point data */
	// Serial.println("Angular velocity: ");
	// Serial.print("X: ");
	// Serial.print(anguvel.x());
	// Serial.print(" Y: ");
	// Serial.print(anguvel.y());
	// Serial.print(" Z: ");
	// Serial.print(anguvel.z());
	// Serial.println("\t");
	/*
	// Quaternion data
	imu::Quaternion quat = bno.getQuat();
	Serial.print("qW: ");
	Serial.print(quat.w(), 4);
	Serial.print(" qX: ");
	Serial.print(quat.y(), 4);
	Serial.print(" qY: ");
	Serial.print(quat.x(), 4);
	Serial.print(" qZ: ");
	Serial.print(quat.z(), 4);
	Serial.print("\t\t");
	*/
	//displaySensorStatus();

	delay(BNO055_SAMPLERATE_DELAY_MS);
}
