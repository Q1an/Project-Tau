### Deliverable
##### ESP8266
servo: A simple program to control servo via servo.h  
BNO055: A program that read fusion and raw data from IMU  
Network: A simple http client that can post and get data  
Dataprocess: An integrated program that can send the data from IMU to the Host via HTTP POST and get data from the host to control servo  
##### host
simpleserver: A simple server program that can printout the HTTP GET and POST requests  
phase1: The program for phase 1, include a simple visualization using OPENGL  

### Communication Format
##### ESP8266 -> host
18bytes:  
6	GYROSCOPE(X,Y,Z)     - rad/s     - 1rps = 900 LSB  
6	LINEARACCEL(X,Y,Z)   - m/s^2 	 - 1m/s^2 = 100 LSB  
6	EULER(X,Y,Z)         - degrees   - 1 degree = 16 LSB  
where X,Y,Z are 16bits unsigned int  
##### host -> ESP8266
