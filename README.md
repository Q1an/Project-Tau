#Project Tau
![blueprint](https://github.com/Q1an/Project-Tau/raw/master/source/Phase1_White.001.w.caption.jpg)

##Project Overview
This project is intended to build a group of simple robots that learns how to move cooperatively based on the way they are assembled. While each robot has only one leg which moves forward and backward, the system can support much more complicated moving strategies, such as walking, running and rotating.  

##Hardware Design
The mechanical structure of the robot consists of a 3D-printed, 70mm body frame and a servomotor driven leg. The main processor of the robot is ESP8266, a low-cost, Wi-Fi embedded board, connected with a BNO055 IMU. 

##Project Objectives
For the first two phases of the project, all robots will be connected to a host through a single, shared network. The IMU data sent from each robot will be handled by a server program, and then used to calculate an optimal moving strategy. Starting from the second phase, the system will attempt to move based on strategies learnt from real-time feedback and past experience. At the third phase, the host no longer oversees the whole process, rather, it will be split into a number of virtual simulators each corresponding to a robot. Every simulator only knows about the sensor data sent from its corresponding robot, and information exchanged with its nearby simulators. In the final phase of this project, the optimized, lightweight simulator will migrate to ESP8266 so that the distributive system can run without the host. 

####Phase 0 [Completed - Apr 05, 2016]

- settle down project topic;
- decide on project visions;

####Phase 1  [Completed - Apr 28, 2016]
![groupwalking](https://github.com/Q1an/Project-Tau/raw/master/source/walk.gif)    
**iteration 1**   

- design the mechanical structure of the robot; assemble prototypes;  
- setup local web server to receive IMU data sent from each robot;   
- send moving instructions through Wi-Fi to each robot based on a naive, deterministic algorithm;
- assemble a four-robot system; the system is able to move steadily;   

**iteration 2**

- use new stable servo
- standardize model:
	- easy to assemble
	- legs are of the same legnth
	- calibrate servo
- modify robot design to accommodate requirements of power supply; use flexible cable;
- check MCU code to solve occasional delays
- based on IMU to know directions
- work on the server programin preparation for phase 2; 


####Phase 2  [Ongoing]

- build a long-lasting and safe playground;
- optimaize the developed moving strategy based on ML algorithm;
- regulate the data received, establish the learnign model;
- build a database to store relevant info.
- try more advanced ML algorithmsto tune the robots;


####Phase 3

- realize simulators on the host;
- without prior knowledge of how it is assembled, the system is able to develop satisfying optimal stategies through learning; 
- support more interesting ways of assembling these robots;
- the system can move on different terrains;

####Phase 4

- optimize the algorithm of simulator; simulator migrates to ESP8266;
- realize communication between nearby robots;
- the system can move on various situations regardless of how it is assembled;

