import math
import numpy
import globalvar
def twochartoint(twochar):
	if len(twochar)!=2:
		print("Not a uint16")
		return 0
	temp = ord(twochar[0])+(ord(twochar[1])<<8)
	if temp > 32767:
		temp = -65536 + temp
	return temp

def fourchartolong(fourchar):
	if len(fourchar) != 4:
		print "Not a uint32"
		return 0
	ulong = ord(fourchar[0]) + (ord(fourchar[1]) << 8) + (ord(fourchar[2]) << 16) + (ord(fourchar[3]) << 24)
	return ulong

def imuparser(data):
	if len(data)!=30:
		print("Not a valid IMU data")
		return
	dic = {}
	dic["gyro_x"]=twochartoint(data[0:2])/900.0
	dic["gyro_y"]=twochartoint(data[2:4])/900.0
	dic["gyro_z"]=twochartoint(data[4:6])/900.0
	dic["linearacc_x"]=twochartoint(data[6:8])/100.0
	dic["linearacc_y"]=twochartoint(data[8:10])/100.0
	dic["linearacc_z"]=twochartoint(data[10:12])/100.0
	dic["euler_x"]=twochartoint(data[12:14])/16.0
	dic["euler_y"]=twochartoint(data[14:16])/16.0
	dic["euler_z"]=twochartoint(data[16:18])/16.0
	dic["quaternion_w"] = twochartoint(data[18:20])/16384.0
	dic["quaternion_x"] = twochartoint(data[20:22])/16384.0
	dic["quaternion_y"] = twochartoint(data[22:24])/16384.0
	dic["quaternion_z"] = twochartoint(data[24:26])/16384.0
	globalvar.timeold = globalvar.timenew
	globalvar.timenew = fourchartolong(data[26:30])/1000000.0
	print (globalvar.timeold,globalvar.timenew)
	dic["current_time"] = fourchartolong(data[26:30])/1000000.0
	return dic

def quaternion_matrix(quaternion):
    q = numpy.array(quaternion[:4], dtype=numpy.float64, copy=True)
    nq = numpy.dot(q, q)
    q *= math.sqrt(2.0 / nq)
    q = numpy.outer(q, q)
    return numpy.array((
        (1.0-q[1, 1]-q[2, 2],     q[0, 1]-q[2, 3],     q[0, 2]+q[1, 3], 0.0),
        (    q[0, 1]+q[2, 3], 1.0-q[0, 0]-q[2, 2],     q[1, 2]-q[0, 3], 0.0),
        (    q[0, 2]-q[1, 3],     q[1, 2]+q[0, 3], 1.0-q[0, 0]-q[1, 1], 0.0),
        (                0.0,                 0.0,                 0.0, 1.0)
        ), dtype=numpy.float64)

def euler_from_quaternion(matrix):
    i = 0
    j = 1
    k = 2

    M = numpy.array(matrix, dtype=numpy.float64, copy=False)[:3, :3]
    cy = math.sqrt(M[i, i]*M[i, i] + M[j, i]*M[j, i])
    ax = math.atan2( M[k, j],  M[k, k])
    ay = math.atan2(-M[k, i],  cy)
    az = math.atan2( M[j, i],  M[i, i])

    ax, ay, az = -ax, -ay, -az
    ax, az = az, ax
    return ax, ay, az

def servomap(t,a,b,c,d):
	return (b-a)/(d-c)*(t-c)+a