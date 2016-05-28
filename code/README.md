## Deliverable
### ESP8266
servo: A simple program to control servo via servo.h  
BNO055: A program that read fusion and raw data from IMU  
Network: A simple http client that can post and get data  
Dataprocess: An integrated program that can send the data from IMU to the Host via HTTP POST and get data from the host to control servo  
### HOST
simpleserver: A simple server program that can printout the HTTP GET and POST requests  
phase1: The program for phase 1, include a simple visualization using OPENGL    
phase2: Programs for phase 2, with framework as shown in the picture below:
![framework](https://github.com/Q1an/Project-Tau/raw/master/source/host.png)

## Communication Format
### ESP8266 → host
30 bytes:  
6	GYROSCOPE(X,Y,Z)     - rad/s     - 1rps = 900 LSB  
6	LINEARACCEL(X,Y,Z)   - m/s^2 	 - 1m/s^2 = 100 LSB  
6	EULER(X,Y,Z)         - degrees   - 1 degree = 16 LSB  
8	QUAT(W,X,Y,Z)			 - quat unit  - 1 Quaternion = 2^14 LSB     
4	TIME    
where X,Y,Z are 16bits unsigned int  
### host → ESP8266
servo control signals